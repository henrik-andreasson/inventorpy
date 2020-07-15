from flask import Blueprint

bp = Blueprint('firewall', __name__)

from app.modules.firewall import routes
