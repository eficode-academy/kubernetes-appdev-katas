# The base image
FROM ubuntu:latest

# Install python and pip
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

# Install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# Copy files required for the app to run
COPY app.py /usr/src/app/

# Declare the port number the container should expose
EXPOSE 5000

# Run the application
ENTRYPOINT ["python", "/usr/src/app/app.py"]
CMD ["--mode", "age"]
