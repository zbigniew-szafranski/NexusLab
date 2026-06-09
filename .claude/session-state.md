# Session State

> Plik do zachowywania kontekstu miedzy sesjami. Po `/clear` uzyj `/catchup` aby wczytac.
> Ostatnia aktualizacja: 2026-06-09

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

## Co zostalo zrobione

Zobacz sesje powyżej.

## Co jest w trakcie / nastepne kroki

Deploy gw-maile-python na VPS.

## Problemy i rozwiazania

- **allauth rate limit ValueError** — format `"3/h/ip"` nieprawidłowy dla 0.57.x, poprawny to `"3/h"`
- **110 plików w git status** — fałszywe zmiany uprawnień na NTFS, fix: `git config core.fileMode false`
- **SSH timeout** — VPS nieosiągalny z lokalnej maszyny przez SSH, deploy ręcznie z VPS

## Wazne decyzje

- Rejestracja zablokowana całkowicie (redirect + usunięte linki) — konta tworzone ręcznie przez admina
- `ACCOUNT_PREVENT_ENUMERATION = False` — akceptowalny kompromis (enumeration możliwy, ale spam zablokowany)
