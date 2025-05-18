import logging
from logging.config import dictConfig

from src.core.settings import settings


def configure_logging():
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "maxBytes": 10_485_760,
                "backupCount": 5,
                "formatter": "standard"
            }
        },
        "loggers": {
            "app": {
                "handlers": ["console", "file"],
                "level": "DEBUG" if settings.DEBUG else "INFO",
                "propagate": False
            }
        }
    }

    dictConfig(logging_config)
    return logging.getLogger("app")


logger = configure_logging()
