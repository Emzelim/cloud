# Pull base image
FROM python:3.5

ENV PYTHONUNBUFFERED 1
EXPOSE 8000


# RUN apt-get update && apt-get install --yes nginx redis-server supervisor

RUN mkdir /armin_cloud-app
WORKDIR /armin_cloud-app


# Add requirements.txt file to container
ADD requirements.txt /armin_cloud-app

# Install requirements
RUN pip install --upgrade pip
RUN pip install -r /armin_cloud-app/requirements.txt

# Add the current directory(the web folder) to Docker container
ADD armin_cloud /armin_cloud-app

