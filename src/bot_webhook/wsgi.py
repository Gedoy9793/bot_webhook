import logging
from .flask import app as application 

application.logger.handlers = logging.getLogger('gunicorn.error').handlers
application.logger.setLevel('INFO')