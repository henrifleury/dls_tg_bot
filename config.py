import os
cwd = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(cwd, 'inputs')
RESULT_FOLDER = os.path.join(cwd, 'results')
API_URL = 'https://api.telegram.org/bot'
LOG_LEVEL = 'INFO'

SENDER_MAX_N_THREADS = 3
SENDER_DELAY = 3