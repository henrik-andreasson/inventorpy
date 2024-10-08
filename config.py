import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('INVENTORPY_SECRET_KEY') or 'you-will-never-guess'
    PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME') or 'http'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
#    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#        'mysql+pymysql://inventorpy:foo123@172.21.0.2/inventorpy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    POSTS_PER_PAGE = 25
    LANGUAGES = ['en', 'es']
    ROCKET_ENABLED = os.environ.get('ROCKET_ENABLED') or False
    ROCKET_USER = os.environ.get('ROCKET_USER') or 'inventory'
    ROCKET_PASS = os.environ.get('ROCKET_PASS') or 'foo123'
    ROCKET_URL = os.environ.get('ROCKET_URL') or 'http://172.17.0.4:3000'
    ROCKET_CHANNEL = os.environ.get('ROCKET_CHANNEL') or 'general'
    OPEN_REGISTRATION = os.environ.get('OPEN_REGISTRATION') or True
    INVENTORPY_TZ = os.environ.get('TEAMPLAN_TZ') or "Europe/Stockholm"
    CERT_LOGIN = os.environ.get('CERT_LOGIN') or False
    CERT_DN_COMP_IS_USERNAME = os.environ.get('CERT_DN_COMP_IS_USERNAME') or "CN"
    PROXY_FIX = os.environ.get('PROXY_FIX') or 0

    # Force approval of PED key handover
    PED_HANDOVER_MUST_BE_APPROVED = True
