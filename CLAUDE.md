# CLAUDE.md

Ten plik zawiera wytyczne dla Claude Code (claude.ai/code) przy pracy z kodem w tym repozytorium.

## Opis projektu

NexusLab to platforma SaaS do automatyzacji z AI. Główny produkt to **Gratka Alerts** — wielodostępowy system monitorowania ofert nieruchomości. Scrapuje Gratka.pl co godzinę przez n8n, dopasowuje oferty do kryteriów użytkownika i wysyła powiadomienia email.

Projekt jest na etapie wczesnego MVP. Infrastruktura działa. Aplikacja Django jest zbudowana z podstawowymi funkcjami.

## Architektura

Wszystkie usługi działają na jednym VPS-ie Hostinger (Ubuntu 22.04, IP: `72.62.115.222`):

- **Traefik v2.11** (Docker, porty 80/443) — główny reverse proxy + SSL (Let's Encrypt)
- **Django 5.0** (Gunicorn :8000) — aplikacja webowa, zarządzana przez Supervisor
- **PostgreSQL 16** (localhost:5432) — baza danych `nexuslab_db`, użytkownik `nexuslab_user`
- **n8n** (Docker, port 5678) — workflow automatyzacji (scraper Gratka co godzinę)
- **Redis** (localhost:6379) — broker wiadomości Celery
- **Supervisor** — zarządza gunicorn, celery worker, celery beat

### Routing (Traefik)

Konfiguracja Traefik w `/docker/n8n/docker-compose.yml`. Routing dynamiczny w `/docker/n8n/traefik-dynamic/django.yml`:
- `nexuslab.pl` / `www.nexuslab.pl` → Gunicorn :8000
- `gratka.nexuslab.pl` → Gunicorn :8000 (SubdomainMiddleware przekierowuje na `urls_gratka`)
- `n8n.nexuslab.pl` → n8n :5678 (przez Docker labels)

**Uwaga:** Nginx jest zainstalowany ale **nieużywany** do obsługi Django. Cały ruch HTTP/HTTPS obsługuje Traefik.

### Ścieżki na VPS-ie

- Projekt Django: `/var/www/nexuslab/`
- Venv: `/var/www/nexuslab/venv/`
- .env: `/var/www/nexuslab/.env`
- Deploy: `/var/www/nexuslab/deploy.sh`
- Traefik/n8n Docker: `/docker/n8n/`
- Traefik dynamic config: `/docker/n8n/traefik-dynamic/`

### Aplikacje Django (w katalogu `apps/`)

| Aplikacja | Cel | Status |
|-----------|-----|--------|
| `website` | Strona główna + cennik na nexuslab.pl | Gotowe |
| `accounts` | Autentykacja przez django-allauth | Gotowe |
| `gratka` | Panel Gratka Alerts na gratka.nexuslab.pl | Gotowe |
| `subscriptions` | Plany cenowe, trial 7 dni, blokada dostępu | Gotowe |
| `chatbot` | Integracja chatbota z Claude API | Placeholder |
| `dashboard` | Panel użytkownika | Placeholder |

Aplikacje są rejestrowane jako `apps.website`, `apps.accounts` itd. w ustawieniach.

### Przepływ danych — Gratka Alerts

1. **Użytkownik konfiguruje** kryteria wyszukiwania przez formularz Django → zapisane w `gratka_userconfig`
2. **n8n scrapuje** Gratka.pl co godzinę, odczytuje konfiguracje użytkowników z PostgreSQL, buduje URL-e, wyciąga oferty przez selektory CSS
3. **Deduplikacja** przez `INSERT ... ON CONFLICT (user_id, offer_id) DO NOTHING RETURNING *`
4. **Nowe oferty** wywołują powiadomienia email przez Gmail SMTP (przez Celery task lub bezpośrednio z n8n)

### System subskrypcji

- **Trial 7 dni** — startuje automatycznie przy rejestracji (sygnał `post_save` na User)
- **Model `UserSubscription`** — `has_access` = `is_active OR is_trial_active`
- **`SubscriptionMiddleware`** — blokuje dostęp do Gratka po wygaśnięciu trialu, pomija staff/admin
- **Blokada** → redirect na `/subskrypcja/wygaslo/` (strona "trial wygasł")
- **Aktywacja ręczna** — admin ustawia `is_active=True` w panelu admin (przyszłość: Stripe)
- **Plany:** Darmowy (0 zł, 7 dni) + Pro (49 zł/mies.)
- **Cennik:** `/cennik/` — strona z 2 planami

### Wielodostępność (Multi-Tenancy)

Izolacja na poziomie wierszy: każde zapytanie filtruje po `user_id = request.user.id`. `gratka_userconfig` ma relację one-to-one z User; `gratka_useroffer` ma klucz obcy do User z `unique_together = ['user', 'offer_id']`.

## Główne tabele bazy danych

- `gratka_userconfig` — kryteria wyszukiwania użytkownika (lokalizacja, cena_min/max, metraz, balkon, garaz, piwnica)
- `gratka_useroffer` — zescrapowane oferty użytkownika (offer_id, url, title, price, area, rooms, floor, sent_to_client)
- `subscriptions_plan` — plany cenowe (name, slug, price, features JSON, display_order)
- `subscriptions_usersubscription` — subskrypcja użytkownika (user 1:1, plan FK, trial_start, trial_end, is_active)
- `chatbot_conversation` — przyszła historia czatu

## Middleware

W `config/middleware.py`:
1. **`SubdomainMiddleware`** — routuje `gratka.*` na `config.urls_gratka`
2. **`SubscriptionMiddleware`** — blokuje Gratka po wygaśnięciu trialu (pomija staff, `/accounts/`, `/admin/`, `/cennik`, `/subskrypcja/`)

## Stack technologiczny

- **Backend:** Django 5.0, DRF, django-allauth, django-environ, celery, psycopg2-binary
- **Frontend:** HTMX + Alpine.js + Tailwind CSS CDN (renderowanie po stronie serwera, bez frameworków JS)
- **AI:** Anthropic Claude API (chatbot, przyszłe ocenianie ofert)
- **Email:** Gmail SMTP (hasło aplikacji, port 587 TLS). Szablony emaili po polsku w `templates/account/email/`
- **Automatyzacja:** n8n (self-hosted, Docker)
- **Reverse proxy:** Traefik v2.11 (Docker) z Let's Encrypt

## Komendy budowania i uruchamiania

```bash
# Środowisko wirtualne (lokalne)
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Django
python manage.py runserver                    # serwer deweloperski
python manage.py makemigrations              # tworzenie migracji
python manage.py migrate                     # stosowanie migracji
python manage.py createsuperuser             # tworzenie administratora
python manage.py collectstatic --noinput     # zbieranie plików statycznych
python manage.py backfill_subscriptions      # tworzenie subskrypcji dla istniejących userów

# Celery
celery -A config worker --loglevel=info      # worker
celery -A config beat --loglevel=info        # scheduler

# Produkcja (Gunicorn)
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4 --timeout 60

# Deployment (na VPS przez SSH)
ssh root@72.62.115.222
cd /var/www/nexuslab && ./deploy.sh
# deploy.sh: git pull → pip install → migrate → collectstatic → supervisorctl restart
```

## Ustawienia Django

Konfiguracja podzielona na pliki:
- `config/settings/base.py` — wspólne ustawienia, używa `django-environ` do odczytu `.env`
- `config/settings/production.py` — rozszerza base o zabezpieczenia produkcyjne (SSL redirect, secure cookies itd.)

Punkt wejścia WSGI: `config.wsgi:application`. Na produkcji ustaw `DJANGO_SETTINGS_MODULE=config.settings.production`.

## Zmienne środowiskowe (`.env`)

Wymagane: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `GMAIL_EMAIL`, `GMAIL_APP_PASSWORD`, `CLAUDE_API_KEY`.

Produkcja: `ALLOWED_HOSTS=nexuslab.pl,www.nexuslab.pl,gratka.nexuslab.pl`

## Styl kolorów (Dark Theme)

Strona używa ciemnego motywu z Tailwind CSS (CDN). Kolory zdefiniowane w `templates/base.html`:

### Paleta kolorów

| Token | Hex | Zastosowanie |
|-------|-----|--------------|
| `navy-900` | `#070d1a` | Tło strony (`body`) |
| `navy-800` | `#0b1628` | Tło kart, nawigacji, pól formularzy |
| `navy-700` | `#0f1f38` | Hover na kartach |
| `navy-600` | `#142a4a` | Ramki (zwykle z `/50` opacity) |
| `navy-500` | `#1a3558` | Jaśniejsze ramki |
| `gold-500` | `#f5a623` | Akcent główny — przyciski CTA, linki, nagłówki |
| `gold-400` | `#fbbf24` | Hover na przyciskach |
| `gold-600` | `#d4911e` | Ciemniejszy złoty |

### Zasady stosowania kolorów

- **Tekst główny:** `text-white` (domyślnie z `body`)
- **Tekst pomocniczy:** `text-gray-400`
- **Tekst przyciemniany:** `text-gray-500`
- **Linki:** `text-gold-500` z `hover:text-gold-400`
- **Przyciski główne (CTA):** `bg-gold-500 text-navy-900 font-bold hover:bg-gold-400`
- **Karty:** `bg-navy-800 border border-navy-600/50`
- **Hover na kartach:** `hover:border-gold-500/30`
- **Pola formularzy:** ciemne tło (`#0b1628`), jasny tekst (`#f1f5f9`), ramka (`#1a3558`), focus złoty (`#f5a623`). Globalne style CSS w `base.html`.
- **Alerty sukces:** `bg-green-900/30 text-green-400 border-green-800`
- **Alerty błąd:** `bg-red-900/30 text-red-400 border-red-800`
- **Badge/tagi:** `bg-gold-500/15 text-gold-400`

## Struktura szablonów

```
templates/
├── base.html                          # Bazowy layout (nav, footer, Tailwind config, globalne CSS)
├── website/
│   ├── index.html                     # Landing page
│   └── pricing.html                   # Strona cennika (/cennik/)
├── gratka/
│   ├── dashboard.html                 # Panel Gratka Alerts
│   └── partials/config_success.html   # HTMX partial
├── subscriptions/
│   └── trial_expired.html             # Strona "trial wygasł"
├── account/
│   ├── base.html                      # Layout formularzy auth
│   ├── login.html, signup.html, logout.html
│   ├── password_reset*.html
│   ├── email_confirm.html, verification_sent.html
│   └── email/                         # Szablony emaili (po polsku)
│       ├── base_message.txt
│       ├── email_confirmation_subject.txt
│       ├── email_confirmation_message.txt
│       ├── email_confirmation_signup_subject.txt
│       ├── email_confirmation_signup_message.txt
│       ├── password_reset_key_subject.txt
│       └── password_reset_key_message.txt
```

## Konwencje

- **Język:** Dokumentacja projektu i teksty UI są po **polsku**. Kod (zmienne, funkcje, komentarze) po angielsku, ale pola modeli domenowych używają polskich nazw zgodnych z terminologią Gratka.pl (np. `lokalizacja`, `cena_min`, `metraz_min`, `balkon`, `garaz`, `piwnica`).
- **Frontend:** HTMX do dynamicznych interakcji (`hx-post`, `hx-target`), Alpine.js do stanu po stronie klienta, Tailwind CSS do stylowania. Bez ciężkich frameworków JS.
- **Szablony** w `templates/`. Pliki statyczne w `static/`.
- **Aplikacje Django** w katalogu `apps/`.
- **Emaile:** Szablony po polsku w `templates/account/email/`. Nadpisują domyślne angielskie szablony allauth.
- **NIGDY nie udostępniaj** kluczy SSH, haseł ani tokenów w czacie.
