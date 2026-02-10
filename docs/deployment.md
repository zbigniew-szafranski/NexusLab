# 🚀 Deployment Guide - Hostinger VPS

## Prerequisites

- Hostinger VPS z Ubuntu 22.04+
- Domena nexuslab.pl (DNS skonfigurowane)
- Root access (SSH)
- Min 4GB RAM, 2 CPU cores

## Initial Server Setup

### 1. SSH Connection
```bash
ssh root@twoj-vps-ip
```

### 2. Update System
```bash
apt update && apt upgrade -y
```

### 3. Create Deploy User
```bash
adduser deploy
usermod -aG sudo deploy
su - deploy
```

### 4. Install Dependencies
```bash
# Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Nginx
sudo apt install nginx -y

# Redis
sudo apt install redis-server -y

# Supervisor
sudo apt install supervisor -y

# Git
sudo apt install git -y

# Certbot (SSL)
sudo apt install certbot python3-certbot-nginx -y
```

## PostgreSQL Setup

### 1. Create Database & User
```bash
sudo -u postgres psql

CREATE DATABASE nexuslab_db;
CREATE USER nexuslab_user WITH PASSWORD 'STRONG_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON DATABASE nexuslab_db TO nexuslab_user;
ALTER DATABASE nexuslab_db OWNER TO nexuslab_user;
\q
```

### 2. Configure PostgreSQL
```bash
sudo nano /etc/postgresql/*/main/postgresql.conf
```

Uncomment and set:
```
listen_addresses = 'localhost'
```

Restart:
```bash
sudo systemctl restart postgresql
```

## Django Project Deployment

### 1. Clone Repository (lub utwórz projekt)
```bash
cd /var/www
sudo mkdir nexuslab
sudo chown deploy:deploy nexuslab
cd nexuslab

# Jeśli masz repo:
git clone https://github.com/twoj-user/nexuslab.git .

# Jeśli nie:
django-admin startproject config .
```

### 2. Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements
```bash
pip install --upgrade pip

# requirements.txt:
pip install Django==5.0.1
pip install djangorestframework==3.14.0
pip install django-allauth==0.57.2
pip install django-cors-headers==4.3.1
pip install django-environ==0.11.2
pip install celery==5.3.4
pip install redis==5.0.1
pip install gunicorn==21.2.0
pip install psycopg2-binary==2.9.9
pip install anthropic==0.8.0
pip install pillow==10.1.0
```

### 4. Environment Variables
```bash
nano .env
```

```.env
DEBUG=False
SECRET_KEY=your-super-secret-key-here-generate-new
ALLOWED_HOSTS=nexuslab.pl,www.nexuslab.pl,gratka.nexuslab.pl

DB_NAME=nexuslab_db
DB_USER=nexuslab_user
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432

GMAIL_EMAIL=twoj@gmail.com
GMAIL_APP_PASSWORD=16-char-app-password

CLAUDE_API_KEY=sk-ant-api...

DJANGO_SETTINGS_MODULE=config.settings.production
```

### 5. Django Settings

**config/settings/base.py:**
```python
import environ
from pathlib import Path

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'corsheaders',
    'allauth',
    'allauth.account',
    
    # Local apps
    'apps.website',
    'apps.accounts',
    'apps.gratka',
    'apps.chatbot',
    'apps.dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('GMAIL_EMAIL')
EMAIL_HOST_PASSWORD = env('GMAIL_APP_PASSWORD')

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**config/settings/production.py:**
```python
from .base import *

DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### 6. Create Django Apps
```bash
python manage.py startapp website apps/website
python manage.py startapp accounts apps/accounts
python manage.py startapp gratka apps/gratka
python manage.py startapp chatbot apps/chatbot
python manage.py startapp dashboard apps/dashboard
```

### 7. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Superuser
```bash
python manage.py createsuperuser
```

### 9. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

## Gunicorn Setup

### 1. Create Gunicorn Config
```bash
nano /var/www/nexuslab/gunicorn_config.py
```

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 60
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
```

### 2. Create Log Directory
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown deploy:deploy /var/log/gunicorn
```

### 3. Test Gunicorn
```bash
cd /var/www/nexuslab
source venv/bin/activate
gunicorn config.wsgi:application --config gunicorn_config.py
```

## Supervisor Setup

### 1. Gunicorn Service
```bash
sudo nano /etc/supervisor/conf.d/gunicorn.conf
```

```ini
[program:gunicorn]
command=/var/www/nexuslab/venv/bin/gunicorn config.wsgi:application --config /var/www/nexuslab/gunicorn_config.py
directory=/var/www/nexuslab
user=deploy
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/gunicorn.log
```

### 2. Celery Worker
```bash
sudo nano /etc/supervisor/conf.d/celery-worker.conf
```

```ini
[program:celery-worker]
command=/var/www/nexuslab/venv/bin/celery -A config worker --loglevel=info
directory=/var/www/nexuslab
user=deploy
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/celery-worker.log
```

### 3. Celery Beat
```bash
sudo nano /etc/supervisor/conf.d/celery-beat.conf
```

```ini
[program:celery-beat]
command=/var/www/nexuslab/venv/bin/celery -A config beat --loglevel=info
directory=/var/www/nexuslab
user=deploy
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/celery-beat.log
```

### 4. Reload Supervisor
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
```

## Nginx Configuration

### 1. Create Nginx Config
```bash
sudo nano /etc/nginx/sites-available/nexuslab
```

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name nexuslab.pl www.nexuslab.pl gratka.nexuslab.pl;
    return 301 https://$server_name$request_uri;
}

# Main site
server {
    listen 443 ssl http2;
    server_name nexuslab.pl www.nexuslab.pl;

    # SSL certificates (will be added by certbot)
    ssl_certificate /etc/letsencrypt/live/nexuslab.pl/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nexuslab.pl/privkey.pem;
    
    # SSL config
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /var/www/nexuslab/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/nexuslab/media/;
        expires 7d;
    }

    # Security headers
    add_header X-Frame-Options "DENY";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
}

# Gratka subdomain
server {
    listen 443 ssl http2;
    server_name gratka.nexuslab.pl;

    ssl_certificate /etc/letsencrypt/live/nexuslab.pl/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nexuslab.pl/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# n8n subdomain (if n8n on same server)
server {
    listen 443 ssl http2;
    server_name n8n.nexuslab.pl;

    ssl_certificate /etc/letsencrypt/live/nexuslab.pl/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nexuslab.pl/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 2. Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/nexuslab /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL Certificate (Let's Encrypt)

```bash
sudo certbot --nginx -d nexuslab.pl -d www.nexuslab.pl -d gratka.nexuslab.pl -d n8n.nexuslab.pl
```

Follow prompts. Certificates auto-renew via cron.

## Post-Deployment

### 1. Test Django
```
https://nexuslab.pl/admin
```

### 2. Test Gratka Panel
```
https://gratka.nexuslab.pl
```

### 3. Test n8n
```
https://n8n.nexuslab.pl
```

## Updating Django Code

### Quick update script
```bash
nano /var/www/nexuslab/deploy.sh
```

```bash
#!/bin/bash
cd /var/www/nexuslab
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart gunicorn
sudo supervisorctl restart celery-worker
sudo supervisorctl restart celery-beat
echo "Deployment complete!"
```

```bash
chmod +x /var/www/nexuslab/deploy.sh
```

Usage:
```bash
./deploy.sh
```

## Monitoring

### View Logs
```bash
# Gunicorn
tail -f /var/log/supervisor/gunicorn.log

# Celery
tail -f /var/log/supervisor/celery-worker.log

# Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Django
tail -f /var/log/django/error.log
```

### Check Services
```bash
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis
sudo supervisorctl status
```

## Troubleshooting

### Django not loading
1. Check gunicorn logs
2. Verify .env file
3. Test: `python manage.py runserver`

### Static files not loading
```bash
python manage.py collectstatic --noinput
sudo chown -R deploy:www-data /var/www/nexuslab/staticfiles
```

### Celery not working
```bash
sudo supervisorctl restart celery-worker
sudo supervisorctl tail celery-worker
```

### PostgreSQL connection error
```bash
sudo -u postgres psql
\l  # list databases
\du # list users
```

## Backup

### Database Backup (daily cron)
```bash
sudo nano /etc/cron.daily/postgres-backup
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
sudo -u postgres pg_dump nexuslab_db | gzip > $BACKUP_DIR/nexuslab_$DATE.sql.gz
find $BACKUP_DIR -name "nexuslab_*.sql.gz" -mtime +7 -delete
```

```bash
sudo chmod +x /etc/cron.daily/postgres-backup
```

### Code Backup
```bash
cd /var/www/nexuslab
git add .
git commit -m "Backup $(date)"
git push
```
