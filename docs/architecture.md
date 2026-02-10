# 🏗️ Architektura Techniczna NexusLab

## Overview

Wszystko hostowane na **jednym Hostinger VPS** - zero zewnętrznych zależności!

```
┌─────────────────────────────────────────────────┐
│  HOSTINGER VPS (nexuslab.pl)                    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  NGINX (port 80/443)                    │    │
│  │  ├─ nexuslab.pl → Django :8000         │    │
│  │  ├─ gratka.nexuslab.pl → Django :8000  │    │
│  │  └─ n8n.nexuslab.pl → n8n :5678        │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  Django App (Gunicorn :8000)            │    │
│  │  ├─ website (landing page)             │    │
│  │  ├─ accounts (auth)                     │    │
│  │  ├─ gratka (alerts panel)              │    │
│  │  ├─ chatbot (Claude API)               │    │
│  │  └─ dashboard (user panel)             │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  PostgreSQL (localhost:5432)            │    │
│  │  ├─ auth_user                           │    │
│  │  ├─ gratka_userconfig                   │    │
│  │  ├─ gratka_useroffer                    │    │
│  │  └─ subscriptions                       │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  n8n (localhost:5678)                   │    │
│  │  ├─ Workflow: Gratka Scraper            │    │
│  │  ├─ Webhook: Config Manager             │    │
│  │  └─ PostgreSQL connector (localhost)    │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  Redis (localhost:6379)                 │    │
│  │  └─ Celery message broker               │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  Supervisor                             │    │
│  │  ├─ gunicorn (Django)                   │    │
│  │  ├─ celery worker                       │    │
│  │  └─ celery beat (scheduler)             │    │
│  └────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

## Data Flow - Gratka Alerts

### 1. Konfiguracja (User → Django → PostgreSQL)
```
User wypełnia formularz (gratka.nexuslab.pl)
    ↓
Django view zapisuje do gratka_userconfig
    ↓
PostgreSQL przechowuje config
```

### 2. Scraping (n8n → Gratka.pl → PostgreSQL)
```
n8n Schedule Trigger (co godzinę)
    ↓
Read all user configs z PostgreSQL
    ↓
FOR EACH user config:
    ├─ Build dynamic URL
    ├─ HTTP Request → Gratka.pl
    ├─ HTML Extract (price, title, area, etc.)
    ├─ Transform arrays → individual items
    ├─ INSERT into gratka_useroffer (ON CONFLICT DO NOTHING)
    └─ IF new offer → Send email via Django API
```

### 3. Email Notification (n8n → Django → Gmail)
```
n8n wykrywa nową ofertę
    ↓
HTTP POST → Django API endpoint
    ↓
Django Celery task: send_new_offer_alert()
    ↓
Gmail SMTP wysyła email do użytkownika
```

## Multi-Tenancy

**PostgreSQL Row Level Security (RLS):**

Każdy user widzi TYLKO swoje dane:
- `gratka_userconfig.user_id = current_user.id`
- `gratka_useroffer.user_id = current_user.id`

**Django middleware:**
```python
request.user → automatyczne filtrowanie queries
User.objects.filter(user=request.user)
```

## Authentication Flow

```
1. User → /login
2. Django AllAuth (email/password)
3. Session cookie set
4. Redirect → /dashboard
5. Dashboard sprawdza auth (LoginRequiredMixin)
6. Render user-specific data
```

## SSL/HTTPS

**Let's Encrypt (certbot):**
```bash
certbot --nginx -d nexuslab.pl -d www.nexuslab.pl -d gratka.nexuslab.pl -d n8n.nexuslab.pl
```

Auto-renewal przez cron.

## Backup Strategy

**PostgreSQL:**
- Daily backup (pg_dump)
- Retention: 7 days local + S3 (opcjonalnie)

**Django media/static:**
- Git dla static
- S3 dla user uploads (przyszłość)

**n8n workflows:**
- Export JSON co tydzień
- Git versioning

## Monitoring

**Opcjonalnie (przyszłość):**
- Sentry (error tracking)
- Prometheus + Grafana (metrics)
- Uptime Robot (availability)

**Teraz:**
- Nginx access logs
- Django logs
- Supervisor logs
