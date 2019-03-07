import os

class Config:
    """Base configuration settings for flask"""
    DEBUG = False
    DATABASE_URI = 'sqlite3:///:memory'

class ProductionConfig(Config):
    """Configuration settings to add if this rolls out to Production"""
    DATABASE_URI = os.environ['DATABASE_URI']

class DebugConfig(Config):
    DEBUG = True
