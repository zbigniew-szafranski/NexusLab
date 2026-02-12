# CLAUDE.md

Ten plik zawiera wytyczne dla Claude Code (claude.ai/code) przy pracy z kodem w tym repozytorium.

## Opis projektu

NexusLab to platforma SaaS do automatyzacji z AI. Główny produkt to **Gratka Alerts** — wielodostępowy system monitorowania ofert nieruchomości. Scrapuje Gratka.pl co godzinę przez n8n, dopasowuje oferty do kryteriów użytkownika i wysyła powiadomienia email.

Projekt jest na etapie wczesnego MVP. Infrastruktura (VPS, PostgreSQL, workflow n8n) działa. Aplikacja Django jest w trakcie budowy.

## Architektura

Wszystkie usługi działają na jednym VPS-ie Hostinger (Ubuntu 22.04):

- **Django 5.0** (Gunicorn :8000) — główna aplikacja webowa za reverse proxy Nginx
- **PostgreSQL 16** (localhost:5432) — baza danych `nexuslab_db`, użytkownik `nexuslab_user`
- **n8n** (localhost:5678) — workflow automatyzacji (scraper Gratka co godzinę)
- **Redis** (localhost:6379) — broker wiadomości Celery
- **Nginx** — reverse proxy + terminacja SSL dla `nexuslab.pl`, `gratka.nexuslab.pl`, `n8n.nexuslab.pl`
- **Supervisor** — zarządza gunicorn, celery worker, celery beat

### Aplikacje Django (w katalogu `apps/`)

| Aplikacja | Cel |
|-----------|-----|
| `website` | Strona główna na nexuslab.pl |
| `accounts` | Autentykacja przez django-allauth |
| `gratka` | Panel Gratka Alerts na gratka.nexuslab.pl |
| `chatbot` | Integracja chatbota z Claude API |
| `dashboard` | Panel użytkownika |

Aplikacje są rejestrowane jako `apps.website`, `apps.accounts` itd. w ustawieniach.

### Przepływ danych — Gratka Alerts

1. **Użytkownik konfiguruje** kryteria wyszukiwania przez formularz Django → zapisane w `gratka_userconfig`
2. **n8n scrapuje** Gratka.pl co godzinę, odczytuje konfiguracje użytkowników z PostgreSQL, buduje URL-e, wyciąga oferty przez selektory CSS
3. **Deduplikacja** przez `INSERT ... ON CONFLICT (user_id, offer_id) DO NOTHING RETURNING *`
4. **Nowe oferty** wywołują powiadomienia email przez Gmail SMTP (przez Celery task lub bezpośrednio z n8n)

### Wielodostępność (Multi-Tenancy)

Izolacja na poziomie wierszy: każde zapytanie filtruje po `user_id = request.user.id`. `gratka_userconfig` ma relację one-to-one z User; `gratka_useroffer` ma klucz obcy do User z `unique_together = ['user', 'offer_id']`.

## Główne tabele bazy danych

- `gratka_userconfig` — kryteria wyszukiwania użytkownika (lokalizacja, cena_min/max, metraz, balkon, garaz, piwnica)
- `gratka_useroffer` — zescrapowane oferty użytkownika (offer_id, url, title, price, area, rooms, floor, sent_to_client)
- `subscriptions_plan` / `subscriptions_usersubscription` — przyszłe rozliczenia subskrypcji
- `chatbot_conversation` — przyszła historia czatu

## Stack technologiczny

- **Backend:** Django 5.0, DRF, django-allauth, django-environ, celery, psycopg2-binary
- **Frontend:** HTMX + Alpine.js + Tailwind CSS (renderowanie po stronie serwera, bez frameworków JS)
- **AI:** Anthropic Claude API (chatbot, przyszłe ocenianie ofert)
- **Email:** Gmail SMTP (hasło aplikacji, port 587 TLS)
- **Automatyzacja:** n8n (self-hosted)

## Komendy budowania i uruchamiania

```bash
# Środowisko wirtualne
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Django
python manage.py runserver                    # serwer deweloperski
python manage.py makemigrations              # tworzenie migracji
python manage.py migrate                     # stosowanie migracji
python manage.py createsuperuser             # tworzenie administratora
python manage.py collectstatic --noinput     # zbieranie plików statycznych

# Celery
celery -A config worker --loglevel=info      # worker
celery -A config beat --loglevel=info        # scheduler

# Produkcja (Gunicorn)
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4 --timeout 60

# Deployment (na VPS)
./deploy.sh    # pull, instalacja zależności, migracje, collectstatic, restart usług
```

## Ustawienia Django

Konfiguracja podzielona na pliki:
- `config/settings/base.py` — wspólne ustawienia, używa `django-environ` do odczytu `.env`
- `config/settings/production.py` — rozszerza base o zabezpieczenia produkcyjne (SSL redirect, secure cookies itd.)

Punkt wejścia WSGI: `config.wsgi:application`. Na produkcji ustaw `DJANGO_SETTINGS_MODULE=config.settings.production`.

## Zmienne środowiskowe (`.env`)

Wymagane: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `GMAIL_EMAIL`, `GMAIL_APP_PASSWORD`, `CLAUDE_API_KEY`.

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
- **Pola formularzy:** ciemne tło (`#0b1628`), jasny tekst (`#f1f5f9`), ramka (`#1a3558`), focus złoty (`#f5a623`)
- **Alerty sukces:** `bg-green-900/30 text-green-400 border-green-800`
- **Alerty błąd:** `bg-red-900/30 text-red-400 border-red-800`
- **Badge/tagi:** `bg-gold-500/15 text-gold-400`

## Konwencje

- **Język:** Dokumentacja projektu i teksty UI są po **polsku**. Kod (zmienne, funkcje, komentarze) po angielsku, ale pola modeli domenowych używają polskich nazw zgodnych z terminologią Gratka.pl (np. `lokalizacja`, `cena_min`, `metraz_min`, `balkon`, `garaz`, `piwnica`).
- **Frontend:** HTMX do dynamicznych interakcji (`hx-post`, `hx-target`), Alpine.js do stanu po stronie klienta, Tailwind CSS do stylowania. Bez ciężkich frameworków JS.
- **Szablony** w `templates/`. Pliki statyczne w `static/`.
- **Aplikacje Django** w katalogu `apps/`.
