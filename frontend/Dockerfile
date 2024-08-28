# Use an Nginx image from the Docker Hub
FROM nginx:alpine

# Copy the HTML and assets into the Nginx server directory
COPY index.html /usr/share/nginx/html/
COPY css/ /usr/share/nginx/html/css/
COPY js/ /usr/share/nginx/html/js/
COPY assets/ /usr/share/nginx/html/assets/

# Expose port 80
EXPOSE 80
