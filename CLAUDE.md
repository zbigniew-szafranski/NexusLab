# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NexusLab is a SaaS platform for AI-powered automation, with the primary product being **Gratka Alerts** — a multi-tenant real estate offer monitoring system. It scrapes Gratka.pl hourly via n8n, matches offers to user-configured criteria, and sends email notifications.

The project is in early MVP stage. Infrastructure (VPS, PostgreSQL, n8n workflows) is operational. The Django application needs to be built.

## Architecture

All services run on a single Hostinger VPS (Ubuntu 22.04):

- **Django 5.0** (Gunicorn :8000) — main web app behind Nginx reverse proxy
- **PostgreSQL 16** (localhost:5432) — database `nexuslab_db`, user `nexuslab_user`
- **n8n** (localhost:5678) — automation workflows (Gratka scraper runs hourly)
- **Redis** (localhost:6379) — Celery message broker
- **Nginx** — reverse proxy + SSL termination for `nexuslab.pl`, `gratka.nexuslab.pl`, `n8n.nexuslab.pl`
- **Supervisor** — manages gunicorn, celery worker, celery beat

### Django Apps (planned under `apps/`)

| App | Purpose |
|-----|---------|
| `website` | Landing page at nexuslab.pl |
| `accounts` | Authentication via django-allauth |
| `gratka` | Gratka Alerts panel at gratka.nexuslab.pl |
| `chatbot` | Claude API chatbot integration |
| `dashboard` | User dashboard |

Apps are registered as `apps.website`, `apps.accounts`, etc. in settings.

### Data Flow — Gratka Alerts

1. **User configures** search criteria via Django form → saved to `gratka_userconfig`
2. **n8n scrapes** Gratka.pl hourly, reads all active user configs from PostgreSQL, builds per-user URLs, extracts offers via CSS selectors
3. **Deduplication** via `INSERT ... ON CONFLICT (user_id, offer_id) DO NOTHING RETURNING *`
4. **New offers** trigger email notifications via Gmail SMTP (through Django Celery task or directly from n8n)

### Multi-Tenancy

Row-level isolation: every query filters by `user_id = request.user.id`. `gratka_userconfig` has a one-to-one relationship with User; `gratka_useroffer` has a foreign key to User with `unique_together = ['user', 'offer_id']`.

## Key Database Tables

- `gratka_userconfig` — per-user search criteria (lokalizacja, cena_min/max, metraz, balkon, garaz, piwnica)
- `gratka_useroffer` — scraped offers per user (offer_id, url, title, price, area, rooms, floor, sent_to_client)
- `subscriptions_plan` / `subscriptions_usersubscription` — future subscription billing
- `chatbot_conversation` — future chat history

## Tech Stack

- **Backend:** Django 5.0, DRF, django-allauth, django-environ, celery, psycopg2-binary
- **Frontend:** HTMX + Alpine.js + Tailwind CSS (server-side rendered, no JS frameworks)
- **AI:** Anthropic Claude API (chatbot, future offer scoring)
- **Email:** Gmail SMTP (app password, port 587 TLS)
- **Automation:** n8n (self-hosted)

## Build & Run Commands

```bash
# Virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Django
python manage.py runserver                    # dev server
python manage.py makemigrations              # create migrations
python manage.py migrate                     # apply migrations
python manage.py createsuperuser             # create admin user
python manage.py collectstatic --noinput     # collect static files

# Celery
celery -A config worker --loglevel=info      # worker
celery -A config beat --loglevel=info        # scheduler

# Production (Gunicorn)
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4 --timeout 60

# Deployment (on VPS)
./deploy.sh    # pulls, installs deps, migrates, collects static, restarts services
```

## Django Settings

Settings use split configuration:
- `config/settings/base.py` — shared settings, uses `django-environ` to read `.env`
- `config/settings/production.py` — extends base with security hardening (SSL redirect, secure cookies, etc.)

The WSGI entry point is `config.wsgi:application`. Set `DJANGO_SETTINGS_MODULE=config.settings.production` for production.

## Environment Variables (`.env`)

Required variables: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `GMAIL_EMAIL`, `GMAIL_APP_PASSWORD`, `CLAUDE_API_KEY`.

## Conventions

- Language: Project documentation and UI copy are in **Polish**. Code (variables, functions, comments) should be in English, but domain-specific model fields use Polish names matching Gratka.pl terminology (e.g., `lokalizacja`, `cena_min`, `metraz_min`, `balkon`, `garaz`, `piwnica`).
- Frontend: Use HTMX for dynamic interactions (`hx-post`, `hx-target`), Alpine.js for client-side state, Tailwind CSS for styling. No heavy JS frameworks.
- Templates go in `templates/`. Static assets in `static/`.
- Django apps live under `apps/` directory.
