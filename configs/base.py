import os

class Config:
    """Base configuration settings for flask"""
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    CELERY_BROKER_URI = os.environ['CELERY_URI']
    CELERY_RESULT_BACKEND = os.environ['CELERY_BACKEND']
