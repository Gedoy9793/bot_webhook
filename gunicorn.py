import multiprocessing

bind = '18002'
workers = multiprocessing.cpu_count() * 2 + 1

loglevel = 'debug'

backlog = 2048
daemon = False
debug = True
proc_name = 'bot_webhook'
pidfile = './log/gunicorn.pid'
errorlog = './log/error.log'
accesslog = './log/access.log'
