from flask import Blueprint

bp = Blueprint('pc', __name__)

from app.modules.pc import routes
