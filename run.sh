#!/bin/bash
git pull
pdm install
cat log/gunicorn.pid | awk '{print "kill "$1}' | sh
exec .venv/bin/gunicorn -c gunicorn.py bot_webhook.wsgi:application