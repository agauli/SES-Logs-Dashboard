from flask import Flask, request, jsonify
import boto3
import json
from datetime import datetime
from collections import defaultdict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS if needed

client = boto3.client('logs', region_name='us-east-1')

def format_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')

def get_log_streams(log_group, start_date, end_date):
    start_ts = int(datetime.strptime(start_date, '%Y/%m/%d').timestamp() * 1000)
    end_ts = int(datetime.strptime(end_date, '%Y/%m/%d').timestamp() * 1000)

    response = client.describe_log_streams(
        logGroupName=log_group,
        orderBy='LogStreamName',
        descending=True
    )
    
    log_streams = [
        stream['logStreamName']
        for stream in response['logStreams']
        if start_date <= stream['logStreamName'].split('-')[0] <= end_date
    ]
    
    return log_streams

def get_logs(log_group, log_streams):
    logs = []
    for log_stream in log_streams:
        next_token = None
        while True:
            try:
                params = {
                    'logGroupName': log_group,
                    'logStreamName': log_stream,
                    'startFromHead': True,
                    'limit': 10000
                }
                
                if next_token:
                    params['nextToken'] = next_token
                
                response = client.get_log_events(**params)
                logs.extend(response.get('events', []))
                
                new_next_token = response.get('nextForwardToken')
                if new_next_token == next_token:
                    break
                
                next_token = new_next_token
                
                if len(logs) >= 10000:
                    break
                
            except client.exceptions.ResourceNotFoundException:
                break
            except Exception as e:
                break
    return logs

def process_logs(logs, event_type):
    bounce_data = []
    delivery_data = []
    complaint_data = []
    open_data = []
    send_data = []

    for event in logs:
        try:
            message = json.loads(event['message'])
            caller_identity = message['mail']['tags'].get('ses:caller-identity', ['Unknown'])[0]

            if message.get('eventType') == 'Bounce' and event_type == 'bounce':
                if 'bounce' in message:
                    bounced_recipients = message['bounce']['bouncedRecipients']
                    bounce_type = message['bounce']['bounceType']
                    timestamp = message['bounce']['timestamp']
                    source_email = message['mail']['source'] 

                    for recipient in bounced_recipients:
                        bounced_email = recipient['emailAddress']
                        bounce_data.append({
                            'timestamp': timestamp,
                            'source_email': source_email,
                            'bounced_email': bounced_email,
                            'bounce_type': bounce_type,
                            'ses_caller_identity': caller_identity
                        })

            if message.get('eventType') == 'Delivery' and event_type == 'delivery':
                if 'delivery' in message:
                    destinations = message['delivery']['recipients']
                    source_email = message['mail']['source']
                    timestamp = message['mail']['timestamp']
                    for destination in destinations:
                        delivery_data.append({
                            'timestamp': timestamp,
                            'source_email': source_email,
                            'destination': destination,
                            'ses_caller_identity': caller_identity
                        })

            if message.get('eventType') == 'Complaint' and event_type == 'complaint':
                if 'complaint' in message:
                    complaint_source = message['mail']['source']
                    complaint_date = message['complaint']['timestamp']
                    complaint_data.append({
                        'date': complaint_date,
                        'complaint_source': complaint_source,
                        'ses_caller_identity': caller_identity
                    })

            if message.get('eventType') == 'Open' and event_type == 'open':
                if 'open' in message:
                    open_source = message['mail']['source']
                    open_date = message['open']['timestamp']
                    open_data.append({
                        'date': open_date,
                        'open_source': open_source
                    })

            if message.get('eventType') == 'Send' and event_type == 'send':
                if 'send' in message:
                    send_source = message['mail']['source']
                    send_date = message['mail']['timestamp']
                    destinations = message['mail']['destination']
                    for destination in destinations:
                        send_data.append({
                            'date': send_date,
                            'source_email': send_source,
                            'destination': destination,
                            'ses_caller_identity': caller_identity
                        })

        except json.JSONDecodeError:
            continue

    return {
        'bounce_data': bounce_data,
        'delivery_data': delivery_data,
        'complaint_data': complaint_data,
        'open_data': open_data,
        'send_data': send_data
    }

def convert_date_format(date_str):
    # Parse the date in 'yyyy-mm-dd' format
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    # Format the date in 'yyyy/mm/dd' format
    return date_obj.strftime('%Y/%m/%d')

@app.route('/api/get_ses_logs', methods=['GET'])
def get_ses_logs():
    log_group = request.args.get('log-group')
    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')
    event_type = request.args.get('event-type')
    print(start_date)

    if not all([log_group, start_date, end_date, event_type]):
        return jsonify({'error': 'Missing required parameters'}), 400

    log_streams = get_log_streams(log_group, start_date, end_date)
    logs = get_logs(log_group, log_streams)
    processed_logs = process_logs(logs, event_type)

    return jsonify(processed_logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
