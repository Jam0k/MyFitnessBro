# Use an official Python runtime as a parent image
FROM python:3.9

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y nodejs npm

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Navigate to static directory and install npm packages
WORKDIR /app/static
RUN npm install

# Return to the app directory
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
