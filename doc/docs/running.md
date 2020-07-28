
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
