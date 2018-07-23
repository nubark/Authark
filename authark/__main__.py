"""
Authark entrypoint
"""
import sys
import argparse
from authark.infrastructure.web.base import create_app
from authark.infrastructure.web.server import Application
from authark.infrastructure.config.context import Context
from authark.infrastructure.config.config import (
    DevelopmentConfig, ProductionConfig)
from authark.infrastructure.config.registry import (
    MemoryJwtRegistry, JsonJwtRegistry)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-dev", "--developement", help="Development Mode.",
                        action="store_true")
    args = parser.parse_args()

    ConfigClass = ProductionConfig
    RegistryClass = JsonJwtRegistry

    if args.developement:
        ConfigClass = DevelopmentConfig
        RegistryClass = MemoryJwtRegistry

    try:
        config = ConfigClass()
        registry = RegistryClass(config)
        context = Context(config, registry)
        gunicorn_config = config['gunicorn']
    except Exception as e:
        sys.exit("Configuration loading error: {0} {1}".format(type(e), e))

    app = create_app(context)
    Application(app, gunicorn_config).run()


if __name__ == '__main__':
    main()
