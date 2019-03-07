import os

from .base import Config


class ProductionConfig(Config):
    """Configuration settings to add if this rolls out to Production"""
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']