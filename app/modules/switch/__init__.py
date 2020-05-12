from flask import Blueprint

bp = Blueprint('switch', __name__)

from app.modules.switch import routes
