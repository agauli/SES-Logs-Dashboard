# SES Log Dashboard

SES Log Dashboard(SES Insights) is a web-based application designed to provide an intuitive interface for viewing and analyzing Amazon Simple Email Service (SES) logs. It allows users to monitor email delivery status, view bounces, troubleshoot issues, and gain insights into email campaigns with ease.

## Features

- **Log Visualization**: View detailed logs of SES emails, including delivery status, bounce details, and error messages.
- **Search and Filter**: Easily search and filter logs based on date range, event type, and other criteria.
- **Real-Time Data**: Monitor email delivery status and other metrics in real-time.
- **User-Friendly Interface**: Access and analyze logs through a clean, responsive web interface.

## Getting Started

To get started with Dashboard, follow these steps:

### Prerequisites

- Send SES events to cloudwatch log. 
- Docker and Docker Compose installed on your machine.
- Access to an Amazon SES account with SNS configured to forward logs.

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/agauli/SES-Logs-Dashboard.git
   cd SES-Logs-Dashboard
   ```
2. **Setup AWS credentials to read cloudwatch logs**:
   - Best practice is to assume IAM role.

    For local development, pass environment variables when you run the Docker container. 
    ```bash
		   docker run -e AWS_ACCESS_KEY_ID=your_access_key_id \
           -e AWS_SECRET_ACCESS_KEY=your_secret_access_key \
           -e AWS_DEFAULT_REGION=your_default_region \
           your_image_name
    ```

2. **Build and Run the Application**:
   ```bash
	docker-compose up --build
   ```
3. **Access the Dashboard**:
	Open your web browser and navigate to http://localhost:80 for the frontend.
	
	Ensure that the backend service is accessible on port 5000.
		Example Request:
   `curl "http://localhost:5000/api/get_ses_logs?log-group=/aws/ses/event_logs&start-date=2024/08/26&end-date=2024/08/31&event-type=bounce"`
   
	API Endpoints
	GET /api/get_ses_logs: Retrieve SES logs.

	Parameters:
	**log-group:** The log group name in SES.
	**start-date:** Start date for log retrieval (format: YYYY/MM/DD).
	**end-date:** End date for log retrieval (format: YYYY/MM/DD).
	**event-type:** Type of event to filter by (e.g., bounce, complaint, delivery).



## Contributing
Contributions are welcome! Please follow these guidelines:

 - Fork the repository and create a new branch for your changes.
 - Make your modifications and ensure tests pass.
 - Submit a pull request with a clear description of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or issues, please contact apps.ashu@gmail.com 



