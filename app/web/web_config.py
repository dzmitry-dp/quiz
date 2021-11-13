import sys
import os.path


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import config

_port = config.PORT

class FlaskConfiguration:
    DEBUG = True
    # TEMPLATE_FOLDER = './web/templates'
    # STATIC_FOLDER = '/static'
    # UPLOAD_FOLDER = './web/'
