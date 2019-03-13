from app import create_app
from configs import get_config

from celery.bin import worker

if __name__ == '__main__':
    config = get_config('debug')

    app = create_app(config)

    #after creating app import celery
    from app import celery as celeryApp

    worker = worker.worker(app=celeryApp)
    options = {
        "loglevel": "info",
        "traceback": True
    }
    worker.run(**options)