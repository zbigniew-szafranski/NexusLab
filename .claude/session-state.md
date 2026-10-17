# Session State

> Plik do zachowywania kontekstu miedzy sesjami. Po `/clear` uzyj `/catchup` aby wczytac.
> Ostatnia aktualizacja: 2026-10-18

## Sesja 2 — 2026-10-18

### Co zrobiono

#### [Błąd 500 na gratka.nexuslab.pl] (GOTOWE)

- **`templates/base.html`, `templates/subscriptions/trial_expired.html`** — `{% url 'website:pricing' %}` → `https://nexuslab.pl/cennik/` (namespace `website` nie istnieje w `urls_gratka` → NoReverseMatch na każdej stronie gratki), commit `08de7fb`

#### [nexuslab.pl jako portfolio] (GOTOWE)

- **`templates/website/index.html`** — przebudowa na portfolio: hero z korzyścią + CTA, O mnie (zdjęcie), Projekty (Flowmail, Gratka Alerts, sprzedajm.pl), Opinie, Automatyzacje n8n (Sekretarka farmaceuty, Asystent wydatków, Lista zakupów), Czym się zajmuję, Jak wygląda współpraca, FAQ, Kontakt
- **`apps/website/views.py` `FAQ`, `TESTIMONIALS`, `_faq_schema`** — treści FAQ i opinii (z panelgw.com) + JSON-LD `FAQPage`; `ProfessionalService` JSON-LD w szablonie
- **`apps/website/forms.py` `ContactForm` + `views.contact` + `partials/contact_form.html`** — formularz kontaktowy HTMX → mail na `CONTACT_EMAIL` (reply-to nadawca), honeypot, limit 5/h na IP (cache Redis)
- **`config/settings/base.py` `CONTACT_EMAIL`** — nowe ustawienie (domyślnie kontakt@nexuslab.pl)
- **`config/settings/base.py` + `requirements.txt`** — WhiteNoise 6.6.0 (static zwracały 404 na produkcji — Traefik → Gunicorn, nginx nieużywany; naprawiło też CSS admina)
- **`templates/base.html`** — logo wektorowe (SVG atom + „Nexus” kursywa / „Lab” #e0501e), favicon SVG, blok `meta`, animacje `.reveal` (IntersectionObserver, prefers-reduced-motion), nav: „Kontakt” + „Gratka Alerts →” na nexuslab.pl, „Cennik” + logowanie tylko na `gratka.*`, link do polityki prywatności w stopce
- **`templates/website/privacy.html` + `views.privacy`** — `/polityka-prywatnosci/` (RODO) + klauzula pod formularzem
- **`apps/website/views.py` `robots_txt`, `sitemap_xml`** — `/robots.txt` i `/sitemap.xml`
- **`static/img/`** — zbigniew (zdjęcie bez EXIF), og-image (1200×630 z nowym logo), flowmail/gratka (zrzuty; z gratki usunięte „undefined”), sprzedajm.mp4 (wideo przewijania, lazy-load), mockupy telefonów: asystent-wydatkow, lista-zakupow, sekretarka (numery telefonów rozmyte)
- **Flowmail** — liczby: 23 doradców, 400+ maili i newsletterów; **sprzedajm.pl** — etykieta „W trakcie wdrożenia”

#### [GitHub] (GOTOWE)

- **`README.md`** — pełny README projektu (architektura Mermaid, stack, uruchomienie); Celery opisany jako skonfigurowany bez zadań
- **repo `zbigniew-szafranski/zbigniew-szafranski`** — profilowy README (lokalnie `/mnt/dane/Projekty/zbigniew-szafranski`), stare repo ustawione przez usera jako prywatne
- **`templates/website/index.html`** — link do GitHuba w sekcji O mnie

#### [Scraper Gratka — workflow n8n] (PRZYGOTOWANE, NIEWDROŻONE)

- **`~/Downloads/Agent Gratka - poprawiony.json`** — każda oferta parsowana z własnej karty `[data-cy="card"]` (fix „undefined”), pomijanie sekcji `.no-results` („podobne” oferty spoza budżetu), parametry SQL jako tablica (przecinki w tytułach), filtr subskrypcji w Read Config, piętro bez prefiksu „piętro”, nagłówki User-Agent
- **`GRATKA.md`** — checklista wdrożenia workflow + SQL do sprzątania starych danych (niezacommitowany, zawiera dane serwera)

### Następny krok

Wdrożyć poprawiony workflow scrapera według `GRATKA.md` (import do n8n, test ręczny, wyłączenie starego, sprzątanie bazy), a potem deploy nexuslab.pl i weryfikacja na produkcji: formularz kontaktowy (czy mail dochodzi), obrazki/wideo przez WhiteNoise, Search Console + sitemap.

---

## Sesja 1 — 2026-06-09

### Co zrobiono

#### [Atak email bombing — blokada] (GOTOWE)

- **`config/settings/base.py`** — dodano `CACHES` (Redis db 1) wymagany do działania rate limitingu allauth między workerami Gunicorn
- **`config/settings/base.py` `ACCOUNT_RATE_LIMITS`** — limit resetu hasła `3/h`, logowania `5/m`, rejestracji `5/m` (format poprawiony po błędzie deploy — allauth 0.57.x nie akceptuje `/ip` jako trzeci człon)
- **`config/settings/base.py` `ACCOUNT_PREVENT_ENUMERATION`** — ustawione na `False`, blokuje wysyłkę emaili do nieistniejących kont (root cause ataku)
- **`config/urls.py`** — dodano redirect `accounts/signup/` → `accounts/login/` przed include allauth
- **`config/urls_gratka.py`** — ta sama blokada signup na subdomenie gratka.nexuslab.pl
- **`templates/base.html`** — usunięto przycisk "Zarejestruj" z nawigacji
- **`templates/account/login.html`** — usunięto link "Nie masz konta? Zarejestruj się"
- **`templates/website/index.html`** — usunięto 2× przycisk CTA "Zarejestruj się za darmo"
- **`templates/website/pricing.html`** — usunięto 2× przyciski "Zacznij za darmo" i "Wybierz Pro"
- **`config/settings/base.py` `core.fileMode`** — git config `core.fileMode false` (pliki na NTFS /mnt/dane nie obsługują uprawnień Unix — 110 fałszywych zmian)

#### [gw-maile-python — rate limiting formularza kontaktowego] (GOTOWE)

- **`mailer/views/auth.py` `ZapytanieView`** — dodano rate limiting 3/h per IP przez Django cache (FileBasedCache), bez dodatkowych pakietów

### Następny krok

Wdrożyć gw-maile-python na VPS (git pull + docker compose build + up) — zmiana rate limitingu w `ZapytanieView` jest już na branchu `main`, commit `722340f`.

---

## Kluczowe wnioski

- NexusLab był używany jako spam relay przez formularz resetu hasła — allauth domyślnie wysyła email nawet dla nieistniejących kont (PREVENT_ENUMERATION)
- `core.fileMode false` wymagane globalnie dla tego repo (projekt na partycji NTFS /mnt/dane)
- allauth 0.57.x format rate limits: `"3/h"` nie `"3/h/ip"` (ValueError przy starcie)
- Pliki statyczne serwuje WhiteNoise — nginx nie obsługuje Django, Traefik kieruje wszystko do Gunicorna
- Szablony współdzielone przez obie domeny nie mogą używać `{% url 'website:...' %}` — gratka ma własny urlconf
- Gratka.pl przy braku wyników pokazuje „podobne” oferty w `.no-results` — scraper musi je pomijać
- Lokalnie brak PostgreSQL: testy przez `Client`/`render_to_string` bez DB, zrzuty przez headless Chrome z wyrenderowanego HTML

## Co zostalo zrobione

Zobacz sesje powyżej.

## Co jest w trakcie / nastepne kroki

Wdrożenie poprawionego workflow Gratka (`GRATKA.md`), deploy nexuslab.pl i weryfikacja na produkcji.

## Problemy i rozwiazania

- **allauth rate limit ValueError** — format `"3/h/ip"` nieprawidłowy dla 0.57.x, poprawny to `"3/h"`
- **110 plików w git status** — fałszywe zmiany uprawnień na NTFS, fix: `git config core.fileMode false`
- **SSH timeout** — VPS nieosiągalny z lokalnej maszyny przez SSH, deploy ręcznie z VPS

## Wazne decyzje

- Rejestracja zablokowana całkowicie (redirect + usunięte linki) — konta tworzone ręcznie przez admina
- `ACCOUNT_PREVENT_ENUMERATION = False` — akceptowalny kompromis (enumeration możliwy, ale spam zablokowany)
