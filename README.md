# About

Inventory management (or cmdb) service for multiple teams.

Also can announce new/changes to Rocket.Chat

REST API for automatic management is on the agenda but not finished

Very early version but working software.

Author: https://github.com/henrik-andreasson/

Heavily based on the excellent tutorial  [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinberg.

Big Thanks to Miguel!

# demo

login with:

    user: admin
    pass: foo123

[inventorpy demo](https://inventorpydemo-hlvrh7b52a-lz.a.run.app/)

# Running

## Running on CentOS

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

## Running in Docker

build docker:

    docker build -t inventorpy  .

Run bash in docker:

    docker run -p5000:5000 -it  --mount type=bind,source="$(pwd)",target=/inventorpy inventorpy bash

Run flask

    docker run -p5000:5000 -it  --mount type=bind,source="$(pwd)",target=/inventorpy inventorpy flask run --host=0.0.0.0 --reload


# Getting started

* Start as described above.
* Register first user (currently there is no admin, all users can to everything, but everything is logged through audit log)
* Optionally turn off Open registration (then an existing user must create new users)
* First create the objects used by lots of other objects
  * Services
  * Locations
  * Racks
  * Network
* Now regular object can be creates, such as:
  * servers
  * firewalls
  * switches
* Optionally create physical security objects:
  * Safe
  * Compartment (locked box dedicated to one person inside a safe)
* Hardware Security Modules (HSMs)
  * HSM Domain a virtual object but all other objects belong to one of these
  * HSM PCI Card
  * HSM Backup Unit
  * HSM PED Key
  * HSM PIN


## turn off open registration

Inventorpy needs to be configured whether to allow open registration.
The default is in config.py and the setting can be changed via environment variables.

Eg, in bash:

    export OPEN_REGISTRATION = "False"



## All config

```
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    POSTS_PER_PAGE = 25
    ROCKET_ENABLED = os.environ.get('ROCKET_ENABLED') or False
    ROCKET_USER = os.environ.get('ROCKET_USER') or 'inventory'
    ROCKET_PASS = os.environ.get('ROCKET_PASS') or 'foo123'
    ROCKET_URL = os.environ.get('ROCKET_URL') or 'http://172.17.0.4:3000'
    ROCKET_CHANNEL = os.environ.get('ROCKET_CHANNEL') or 'general'
    OPEN_REGISTRATION = os.environ.get('OPEN_REGISTRATION') or True
    INVENTORPY_TZ = os.environ.get('TEAMPLAN_TZ') or "Europe/Stockholm"
```


# Modules in inventorpy

![module overview](doc/module_overview.png)


## server

![class server](doc/classes_server.png)

![add server](doc/server_add.png)


## main - service, location, user and audit

![class service](doc/classes_main.png)

**service**

![add service](doc/service_add.png)

**location**

![add location](doc/location_add.png)

**user**

![add user](doc/user_add.png)


## network

![class network](doc/classes_network.png)

![add network](doc/network_add.png)

## switch / port

![class switch](doc/classes_switch.png)

**switch**

![add switch](doc/switch_add.png)

**switch port**

![add switch port](doc/switch_port_add.png)

## firewall / port

![class firewall](doc/classes_firewall.png)

**fireall**

![add firewall](doc/firewall_add.png)

**firewall port**

![add firewall port](doc/firewall_port_add.png)


## rack

![class rack](doc/classes_rack.png)

![add rack](doc/rack_add.png)


## safe / compartment

![class rack](doc/classes_safe.png)

**safe**

![add safe](doc/safe_add.png)

**compartment**

![add compartment](doc/compartment_add.png)


## HSM

![class hsm domain](doc/classes_hsm.png)

**HSM Domain**

![add hsm domain](doc/hsm_domain_add.png)

**HSM PCI Card**

![add hsm pci card](doc/hsm_pci_card_add.png)

**HSM Backup Unit**

![add hsm backup unit](doc/hsm_backup_unit_add.png)

**HSM PED**

![add hsm ped](doc/hsm_ped_add.png)

**HSM PIN**

![add hsm backup unit](doc/hsm_pin_add.png)

# REST API

to use the REST API there is new login step, get a jwt token first

```
token=$(http --verify cacerts.pem --auth "$username:$password" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')
```

then you can create a new service:

```
http --verify cacerts.pem --verbose POST "${API_URL}/service" \
  "name=${name}" \
  "color=${color}" \
  "Authorization:Bearer $token"
```

to help with getting started with the REST API there are scripts for all API:s in utils/
