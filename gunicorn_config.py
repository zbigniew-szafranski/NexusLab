"""Gunicorn configuration for NexusLab production."""

import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 60
keepalive = 5

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = "nexuslab"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
