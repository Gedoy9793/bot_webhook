pdm instsll
git pull
cat log/gunicorn.pid | awk '{print "kill "$1}' | sh
.venv/bin/gunicorn -c gunicorn.py bot_webhook.wsgi:application
