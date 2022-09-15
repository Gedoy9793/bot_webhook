bind = '0.0.0.0:18002'
workers = 1

loglevel = 'debug'

backlog = 2048
daemon = False
debug = True
proc_name = 'bot_webhook'
pidfile = './log/gunicorn.pid'
errorlog = './log/error.log'
accesslog = './log/access.log'
