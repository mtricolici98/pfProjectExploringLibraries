import os

BASE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

LOGS_DIR = os.path.join(BASE_PATH, 'logs')

if not os.path.isdir(LOGS_DIR):
    os.mkdir(LOGS_DIR)
