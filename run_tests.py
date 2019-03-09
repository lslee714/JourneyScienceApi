#Since flask requires the application context, run unittest inside the context of it
from unittest import defaultTestLoader, TextTestRunner

from configs import get_config

from app import create_app_context

if __name__ == '__main__':
    import argparse

    argParser = argparse.ArgumentParser(description='Run all/some unittests within an app context')

    argParser.add_argument('--app-config', dest='config', nargs='?', choices=('debug', 'live'), default='debug',
                        help='The type of app config to run')
    args = argParser.parse_args()

    verbosity = 1 #default verbosity of unittest

    appConfig = get_config(args.config)
    with create_app_context(config=appConfig) as app:
        discoveredTests = defaultTestLoader.discover('.', top_level_dir='.')
        runner = TextTestRunner(verbosity=verbosity)
        runner.run(discoveredTests)