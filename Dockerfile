# Use an official Python runtime as a parent image
FROM debian:latest

# Set the working directory to /app
#DEV:
WORKDIR /inventorpy

COPY . /inventorpy

# Install any needed packages
RUN apt-get update
RUN apt-get install --no-install-recommends -y python3.7 \
        sqlite3 jq python3-pip python3-setuptools rustc cargo \
        python3-dev libssl-dev python3-wheel gunicorn3

RUN pip3 install -r requirements.txt

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Make port available to the world outside this container
EXPOSE 8080

ENV FLASK_APP=/inventorpy/inventorpy.py

# Run flask when the container launches
CMD [ "/inventorpy/gunicorn-start.sh"]
