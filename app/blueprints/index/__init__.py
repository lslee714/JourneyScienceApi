from flask import Blueprint

from .urls import register

index = Blueprint('index', __name__)

register(index)