# Use the official Ubuntu base image
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev libpq-dev

# Create and set the working directory
RUN mkdir /code
WORKDIR /code

# Copy the requirements file into the image
COPY requirements.txt /code/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the image
COPY . /code/

# Expose the port that the app runs on
EXPOSE 8000

# Command to run tests
CMD ["python3", "manage.py", "test"]

# Command to run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
