from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import users, errors, tokens, service, network, server, location, safe, hsmdomain, hsmped, hsmpin, hsmpcicard
