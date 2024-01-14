# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory inside the container
WORKDIR /usr/src/app

# Prevent Python from writing pyc files and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements file into the container at /usr/src/app/
COPY ./requirements.txt /usr/src/app/

# Install dependencies defined in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app/
COPY . /usr/src/app/
