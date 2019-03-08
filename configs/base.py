import os

class Config:
    """Base configuration settings for flask"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///:memory')