from importlib import import_module
import sys
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)


URL = os.getenv('URL')
VERIFY = os.getenv('VERIFY')
QQ_GROUP = os.getenv('QQ_GROUP')
BOT = os.getenv('BOT')
ADMIN_QQ = os.getenv('ADMIN_QQ')

RESOURCE_FILE = os.path.abspath(os.getenv('RESOURCE_FILE'))

if RESOURCE_FILE:
    sys.path.append(os.path.dirname(RESOURCE_FILE))
    RESOURCE = import_module(os.path.splitext(os.path.basename(RESOURCE_FILE))[0])