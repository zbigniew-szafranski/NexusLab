# 🚀 NexusLab - Platforma Automatyzacji AI

## Opis Projektu

NexusLab to platforma SaaS oferująca:
- **Agentów AI** - chatboty, assistenty, automaty
- **Automatyzację procesów** - workflow'y w n8n
- **Scraping & Monitoring** - Gratka Alerts, OLX, Otodom

## Główny Produkt: Gratka Alerts

Multi-tenant system monitorowania ofert nieruchomości:
- Scraping Gratka.pl co godzinę (n8n)
- Personalizowane kryteria dla każdego użytkownika
- Powiadomienia email (Gmail SMTP)
- Panel webowy do konfiguracji

## Technologie

- **Backend:** Django 5.0 (Python)
- **Database:** PostgreSQL (localhost)
- **Automation:** n8n (localhost:5678)
- **Email:** Gmail SMTP
- **Frontend:** HTMX + Alpine.js + Tailwind CSS
- **AI:** Claude API (chatbot)
- **Server:** Nginx (reverse proxy, SSL)
- **Hosting:** Hostinger VPS (all-in-one)

## Domeny

- `nexuslab.pl` - strona główna (landing page)
- `gratka.nexuslab.pl` - panel Gratka Alerts
- `n8n.nexuslab.pl` - n8n UI (z auth)

## Status

✅ **Działające:**
- VPS Hostinger z PostgreSQL
- n8n workflow Gratka scraper
- Gmail SMTP (app password)
- Domena nexuslab.pl

⏳ **W budowie:**
- Django project structure
- User authentication
- Multi-tenant Gratka panel
- Chatbot integration
- Dashboard

## Klient

Mam już 1 klienta który będzie korzystał z Gratka Alerts - system można wdrożyć od razu po ukończeniu Django panelu.

## Twórca

Zbigniew Szafrański
- Email: zbigniew.szafranski@gmail.com
- Specjalizacja: Python, automatyzacja, AI agents
- Nauka: Django, HTMX
