# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5200 available to the world outside this container
EXPOSE 5200

# Specify Gunicorn as the server
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5200", "app:app"]