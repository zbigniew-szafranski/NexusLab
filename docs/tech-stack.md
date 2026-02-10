# 💻 Tech Stack - Szczegóły

## Backend

### Django 5.0
**Dlaczego:**
- ✅ Znam Python
- ✅ Batteries included (admin, auth, ORM)
- ✅ Django AllAuth (social login ready)
- ✅ Świetne dla SaaS (multi-tenancy)
- ✅ Duża społeczność

**Kluczowe pakiety:**
```
Django==5.0
djangorestframework==3.14.0
django-allauth==0.57.0
django-cors-headers==4.3.0
django-environ==0.11.2
celery==5.3.4
redis==5.0.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
anthropic==0.8.0
```

### PostgreSQL 16
**Dlaczego:**
- ✅ Już zainstalowany na VPS
- ✅ Localhost = zero network latency
- ✅ n8n już połączony
- ✅ JSONB dla flexible data
- ✅ Row Level Security (multi-tenancy)

**Connection:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nexuslab_db',
        'USER': 'nexuslab_user',
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Celery + Redis
**Dlaczego:**
- ✅ Background tasks (email sending)
- ✅ Scheduled tasks (periodic checks)
- ✅ Async processing (heavy operations)

**Use cases:**
- Email notifications (async)
- Data exports (long-running)
- Periodic cleanup (scheduled)

## Frontend

### HTMX + Alpine.js + Tailwind
**Dlaczego NIE React/Vue:**
- ❌ Nie znam JS frameworks
- ❌ Dodatkowa złożoność
- ❌ SEO trudniejsze
- ❌ Więcej kodu

**Dlaczego HTMX:**
- ✅ HTML-first (znam HTML)
- ✅ Zero JavaScript do nauki (prawie)
- ✅ SSR = świetne SEO
- ✅ Progressive enhancement
- ✅ Szybki development

**Przykład HTMX:**
```html
<!-- Formularz bez page reload -->
<form hx-post="/api/save-config/" hx-target="#result">
  <input name="cena_min" value="100000">
  <button type="submit">Zapisz</button>
</form>
<div id="result"></div>
```

**Alpine.js:**
Minimalistyczny JS dla prostych interakcji:
```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open">Content</div>
</div>
```

**Tailwind CSS:**
- Utility-first
- No custom CSS needed
- Responsive built-in
- Dark mode ready

## Automation

### n8n
**Dlaczego:**
- ✅ Już działa na VPS
- ✅ Visual workflow builder
- ✅ 400+ integrations ready
- ✅ Self-hosted (kontrola + tanie)
- ✅ PostgreSQL connector

**Hosting:**
- localhost:5678
- Proxy przez nginx (n8n.nexuslab.pl)
- Auth przez proxy (opcjonalnie SSO w przyszłości)

**Workflows:**
1. **Gratka Scraper** - główny workflow (co 1h)
2. **Config Manager** - webhook do zapisywania konfiguracji
3. **(Przyszłość)** OLX Scraper, Otodom Scraper, Facebook Monitor

## AI/ML

### Claude API (Anthropic)
**Dlaczego NIE OpenAI:**
- ✅ 200k context window (vs 128k GPT-4)
- ✅ Lepszy dla długich dokumentów
- ✅ Świetny follow-up (Projects feature)
- ✅ Bardziej "bezpieczny" (less hallucinations)

**Use cases:**
- Chatbot na stronie (pre-sales support)
- Email content generation
- Offer scoring (przyszłość)
- Data extraction improvements

**Koszt:**
- ~$3 / 1M input tokens
- ~$15 / 1M output tokens
- Realnie: ~10-30 PLN/mies dla chatbota

## Email

### Gmail SMTP
**Dlaczego NIE Brevo/SendGrid:**
- ✅ Już mam Gmail
- ✅ 500 emails/dzień FREE
- ✅ Zero setup (app password)
- ✅ Wysoka deliverability
- ✅ Zaufana domena

**Dlaczego NIE własny SMTP:**
- ❌ Spam issues
- ❌ Blacklist risk
- ❌ Setup complexity

**Config:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'twoj@gmail.com'
EMAIL_HOST_PASSWORD = env('GMAIL_APP_PASSWORD')
```

## Server

### Nginx
**Dlaczego:**
- ✅ Industry standard
- ✅ Reverse proxy (Django, n8n)
- ✅ Static files serving
- ✅ SSL termination
- ✅ Load balancing (przyszłość)

### Gunicorn
**WSGI server dla Django:**
- ✅ Production-ready
- ✅ Worker processes
- ✅ Graceful restarts

**Config:**
```bash
gunicorn config.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 4 \
  --timeout 60
```

### Supervisor
**Process manager:**
- Automatyczny restart przy crash
- Logs management
- Start on boot

**Procesy:**
- gunicorn (Django)
- celery worker
- celery beat

## Hosting

### Hostinger VPS
**Dlaczego:**
- ✅ Już mam
- ✅ Wszystko w jednym miejscu
- ✅ Root access (pełna kontrola)
- ✅ Tanie (~50-100 PLN/mies)
- ✅ Polska lokalizacja

**Specs (minimum):**
- CPU: 2 cores
- RAM: 4GB
- Storage: 50GB SSD
- Bandwidth: unlimited

**Dlaczego NIE cloud (AWS/Azure/GCP):**
- ❌ Droższe
- ❌ Bardziej złożone
- ❌ Overkill dla MVP

**Dlaczego NIE managed platforms (Heroku/Railway):**
- ❌ Droższe przy skalowaniu
- ❌ Mniej kontroli
- ❌ Vendor lock-in

## Development Tools

### Claude Code
**CLI tool do coding z AI:**
- Bezpośrednie edytowanie plików
- Git integration
- Terminal w context

### Windsurf (Codeium IDE)
**AI-powered IDE:**
- Claude integration
- Code completion
- Refactoring suggestions

### Git + GitHub
**Version control:**
- Private repo dla kodu
- Public repo dla docs (opcjonalnie)
- Issues tracking
- CI/CD (przyszłość)

## Security

### Django Security Features
```python
DEBUG = False  # W produkcji!
SECRET_KEY = env('SECRET_KEY')  # Z .env
ALLOWED_HOSTS = ['nexuslab.pl', 'gratka.nexuslab.pl']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
```

### PostgreSQL
- Strong passwords
- Limited user permissions
- Localhost only (no external access)

### Nginx
- Rate limiting
- DDoS protection (Cloudflare opcjonalnie)
- SSL/TLS 1.3

## Monitoring & Logging

### Django Logging
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### Nginx Access Logs
```
/var/log/nginx/access.log
/var/log/nginx/error.log
```

### Supervisor Logs
```
/var/log/supervisor/gunicorn.log
/var/log/supervisor/celery.log
```

## Przyszłe rozszerzenia

**Gdy skala urośnie:**
- **Load Balancer:** Nginx → multiple Django instances
- **Database:** PostgreSQL read replicas
- **Cache:** Redis/Memcached dla queries
- **CDN:** Cloudflare dla static files
- **Monitoring:** Sentry, Prometheus
- **CI/CD:** GitHub Actions → auto-deploy
