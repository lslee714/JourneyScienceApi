from app import create_app

from configs import get_config

if __name__ == '__main__':
    import argparse

    argParser = argparse.ArgumentParser(description='Run the Journey Science API')

    argParser.add_argument('--config', dest='config', nargs='?', choices=('debug', 'live'), default=None,
                           help='The type of configuration to run the service in')

    args = argParser.parse_args()

    appConfig = get_config(args.config)
    app = create_app(config=appConfig)
    app.run()