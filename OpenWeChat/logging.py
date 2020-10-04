import logging
import sys

default_handler = logging.StreamHandler(sys.stderr)


def has_level_handler(logger):
    level = logger.getEffectiveLevel()
    current = logger

    while current:
        for handler in current.handlers:
            if handler.level <= level:
                return True
        if not current.propagate:
            break
        current = current.parent
    return False


def create_logger(app=None):
    prefix = 'OpenWeChat'
    if app:
        logger = logging.getLogger('{}.{}'.format(prefix, app.name))

        if app.debug and not logger.level:
            logger.setLevel(logging.DEBUG)
    else:
        logger = logging.getLogger(prefix)

    if not has_level_handler(logger):
        logger.addHandler(default_handler)
    return logger
