command = '/home/ubuntu/pinker-learn-cooking-backend/venv/bin/gunicorn'
pythonpath = '/home/ubuntu/pinker-learn-cooking-backend'
bind = '127.0.0.1:8001'
workers = 3
user = 'ubuntu'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=pinker_backend.settings'
