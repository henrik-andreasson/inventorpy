from flask import Blueprint

bp = Blueprint('server', __name__)

from app.modules.server import routes
