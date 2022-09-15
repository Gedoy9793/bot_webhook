from dotenv import load_dotenv
import os

load_dotenv(verbose=True)


URL = os.getenv('URL')
VERIFY = os.getenv('VERIFY')
QQ_GROUP = os.getenv('QQ_GROUP')
BOT = os.getenv('BOT')
ADMIN_QQ = os.getenv('ADMIN_QQ')

