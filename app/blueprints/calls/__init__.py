from flask import Blueprint

from .urls import register

calls = Blueprint('calls', __name__, url_prefix='/calls', template_folder='templates')

register(calls)