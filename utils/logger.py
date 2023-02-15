import logging

# Create a custom logger
import os

from config import LOGS_DIR


def get_logger(name, file_name):
    _logger = logging.getLogger(name)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(os.path.join(LOGS_DIR, file_name))

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    _logger.addHandler(c_handler)
    _logger.addHandler(f_handler)

    _logger.setLevel(logging.DEBUG)

    return _logger


logger = get_logger('GeneralLogger', 'logs.log')
posts_logger = get_logger('PostLogger', 'post_logs.log')
accounts_logger = get_logger('AccountsLogger', 'accounts_logs.log')
