# Use an official Python runtime as a parent image
FROM centos:latest

# Set the working directory to /app
#DEV: WORKDIR /inventorpy

COPY . /inventorpy

# Install any needed packages
RUN yum install -y python3 sqlite

RUN pip3 install flask-sqlalchemy flask-migrate flask-login flask-mail \
  flask-bootstrap flask-moment flask-babel python-dotenv jwt flask-wtf \
  WTForms-Components flask-httpauth rocketchat_API icalendar gunicorn \
  ipcalc

# Make port available to the world outside this container
EXPOSE 8080

ENV FLASK_APP=inventorpy.py

# Run flask when the container launches
CMD [ "/inventorpy/gunicorn-start.sh"]
