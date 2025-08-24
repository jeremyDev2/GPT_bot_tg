import logging
from settings import config

def get_logger():

    logging_config = {
        "version": 1,

        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "basic",
                "filename": str(config.LOGS_PATH),
                "maxBytes": 1024,
                "backupCount": 3,
                "encoding": "utf-8"
            }
        },

        "formatters": {
            "basic": {
                "format": "%(levelname)s: %(message)s"
            },
        },

        "root": {
            "handlers": ["file"],
            "level": "INFO"
        }
    }

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)

    return logger
