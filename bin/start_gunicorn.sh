#!/bin/bash
source /home/ubuntu/pinker-learn-cooking-backend/venv/bin/activate
exec gunicorn -c "/home/ubuntu/pinker-learn-cooking-backend/gunicorn_config.py" pinker_backend.wsgi
