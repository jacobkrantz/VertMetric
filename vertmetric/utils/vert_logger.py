import logging

def setup_custom_logger(name, level=logging.INFO):
    """
    Only set the logger once.
    If called again, will only return logger.
    """
    logger = logging.getLogger(name)
    if not len(logger.handlers):
        formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s: %(message)s',
            datefmt='%X'
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.setLevel(level)
        logger.addHandler(handler)

    return logger
