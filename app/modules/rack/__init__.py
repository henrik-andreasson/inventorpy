from flask import Blueprint

bp = Blueprint('rack', __name__)

from app.modules.rack import routes
