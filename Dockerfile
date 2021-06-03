# Use an official Python runtime as a parent image
FROM debian:latest

# Set the working directory to /app
#DEV:
# WORKDIR /inventorpy

COPY . /inventorpy

# Install any needed packages
RUN apt-get update
RUN apt-get install --no-install-recommends -y python3.7 \
        sqlite3 mariadb-client python3-pip \
        python3-flask-sqlalchemy python3-flask-migrate \
        python3-flask-login python3-flask-mail \
        python3-dotenv python3-jwt \
        python3-flaskext.wtf python3-flask-httpauth \
        gunicorn3 python3-pymysql jq

RUN pip3 install werkzeug==0.16.0

RUN pip3 install  flask-bootstrap  WTForms-Components rocketchat_API \
  ipcalc email_validator Flask-Moment Flask-Babel werkzeug httpie

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Make port available to the world outside this container
EXPOSE 8080

ENV FLASK_APP=/inventorpy/inventorpy.py

# Run flask when the container launches
CMD [ "/inventorpy/gunicorn-start.sh"]
