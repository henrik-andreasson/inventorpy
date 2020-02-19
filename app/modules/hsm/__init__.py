from flask import Blueprint

bp = Blueprint('hsm', __name__)

from app.modules.hsm import routes
 
