# About

Inventory management (or cmdb) service for multiple teams.

Also can announce new/changes to Rocket.Chat

REST API for automatic management is on the agenda but not finished

Very early version but working software.

Author: https://github.com/henrik-andreasson/

Heavily based on the excellent tutorial  [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinberg.

Big Thanks to Miguel!

# Run on CentOS

Install python3 and sqlite

    yum install -y python3 sqlite

Used modules

    pip3 install flask-sqlalchemy flask-migrate flask-login flask-mail \
      flask-bootstrap flask-moment flask-babel python-dotenv jwt flask-wtf \
      WTForms-Components flask-httpauth rocketchat_API

install source

    mkdir /opt/inventorpy
    cd /opt/inventorpy
    unzip inventorpy-x.y.z.zip

start
    export FLASK_APP=inventorpy.py
    cd /opt/inventorpy
    flask run --host=0.0.0.0

See also the systemd service file inventorpy.service to run with gunicorn

# Run in Docker

build docker:

    docker build -t inventorpy  .

Run bash in docker:

    docker run -p5000:5000 -it  --mount type=bind,source="$(pwd)",target=/inventorpy inventorpy bash

Run flask

    docker run -p5000:5000 -it  --mount type=bind,source="$(pwd)",target=/inventorpy inventorpy flask run --host=0.0.0.0 --reload


# Modules in inventorpy


## Server


```

class Server(db.Model):
    __tablename__ = "server"
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(140), unique=True)
    role = db.Column(db.String(140))
    status = db.Column(db.String(140))
    ipaddress = db.Column(db.String(140))
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    network = db.relationship('Network')
    memory = db.Column(db.String(140))
    cpu = db.Column(db.String(140))
    psu = db.Column(db.String(140))
    hd = db.Column(db.String(140))
    serial = db.Column(db.String(140))
    model = db.Column(db.String(140))
    os_name = db.Column(db.String(140))
    os_version = db.Column(db.String(140))
    manufacturer = db.Column(db.String(140))
    rack_id = db.Column(db.Integer, db.ForeignKey('rack.id'))
    rack = db.relationship('Rack')
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')
    comment = db.Column(db.String(2000))
    support_start = db.Column(db.DateTime)
    support_end = db.Column(db.DateTime)
    rack_position = db.Column(db.String(10))
    environment = db.Column(db.String(140))
    switch_ports = db.relationship("SwitchPort", back_populates="server")
    virtual_guests = db.relationship("VirtualServer", back_populates="hosting_server")
    virtual_host = db.Column(db.String(10))
```
