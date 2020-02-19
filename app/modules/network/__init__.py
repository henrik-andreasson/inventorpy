from flask import Blueprint

bp = Blueprint('network', __name__)

from app.modules.network import routes
