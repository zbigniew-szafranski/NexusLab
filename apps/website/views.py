import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST

from apps.subscriptions.models import Plan

from .forms import ContactForm

logger = logging.getLogger(__name__)

CONTACT_RATE_LIMIT = 5  # submissions per IP per hour


FAQ = [
    {
        'q': 'Ile trwa wdrożenie?',
        'a': 'Prosta automatyzacja, np. bot na Telegramie albo workflow w n8n, to zwykle kilka dni. '
             'Aplikacja z panelem i kontami użytkowników to kilka tygodni. Dokładny termin podaję '
             'w wycenie, po rozmowie.',
    },
    {
        'q': 'Ile to kosztuje?',
        'a': 'Zależy od zakresu — dlatego zaczynamy od bezpłatnej rozmowy. Po niej dostajesz '
             'konkretną wycenę za cały projekt, bez niespodzianek w trakcie.',
    },
    {
        'q': 'Kto płaci za AI, SMS-y i serwer?',
        'a': 'Usługi takie jak OpenAI, Claude czy Twilio rozliczane są według zużycia, zwykle na '
             'Twoim koncie — masz pełną kontrolę nad kosztami. Przy prostych automatyzacjach to '
             'często kilka–kilkanaście złotych miesięcznie. Szacunek kosztów stałych jest częścią wyceny.',
    },
    {
        'q': 'Muszę znać się na technologii?',
        'a': 'Nie. Rozwiązanie działa w narzędziach, których już używasz — mailu, Telegramie, '
             'arkuszu Google czy telefonie. Pokazuję, jak z niego korzystać, i zostawiam krótką instrukcję.',
    },
    {
        'q': 'Co jeśli coś przestanie działać?',
        'a': 'Monitoruję wdrożone automatyzacje i naprawiam błędy. Gdy zmieni się np. strona, z której '
             'pobierane są dane, albo API dostawcy, dostosowuję rozwiązanie.',
    },
    {
        'q': 'Czy pracujesz zdalnie?',
        'a': 'Tak — rozmowy, wdrożenie i wsparcie prowadzę zdalnie, dla klientów z całej Polski.',
    },
]


def _faq_schema():
    schema = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {'@type': 'Question', 'name': item['q'],
             'acceptedAnswer': {'@type': 'Answer', 'text': item['a']}}
            for item in FAQ
        ],
    }
    # Escape "<" so the JSON can't close the surrounding <script> tag
    return mark_safe(json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c'))


def home(request):
    return render(request, 'website/index.html', {
        'contact_form': ContactForm(),
        'faq': FAQ,
        'faq_schema': _faq_schema(),
    })


def pricing(request):
    plans = Plan.objects.filter(is_active=True)
    return render(request, 'website/pricing.html', {'plans': plans})


def _client_ip(request):
    # Traefik appends the real client IP as the last X-Forwarded-For entry
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[-1].strip()
    return request.META.get('REMOTE_ADDR', '')


@require_POST
def contact(request):
    form = ContactForm(request.POST)
    template = 'website/partials/contact_form.html'

    if not form.is_valid():
        return render(request, template, {'contact_form': form})

    # Bot filled the honeypot: pretend success, send nothing
    if form.cleaned_data['website']:
        return render(request, template, {'success': True})

    rate_key = f'contact_rate:{_client_ip(request)}'
    attempts = cache.get(rate_key, 0)
    if attempts >= CONTACT_RATE_LIMIT:
        return render(request, template, {
            'contact_form': form,
            'error': 'Za dużo wiadomości w krótkim czasie. Spróbuj ponownie za godzinę.',
        })

    data = form.cleaned_data
    body = (
        f"Imię i nazwisko: {data['imie']}\n"
        f"Email: {data['email']}\n"
        f"Telefon: {data['telefon'] or '—'}\n\n"
        f"{data['wiadomosc']}\n"
    )
    message = EmailMessage(
        subject=f"[nexuslab.pl] Zgłoszenie od {data['imie']}",
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_EMAIL],
        reply_to=[data['email']],
    )

    try:
        message.send()
    except Exception:
        logger.exception('Contact form email failed')
        return render(request, template, {
            'contact_form': form,
            'error': 'Nie udało się wysłać wiadomości. Napisz bezpośrednio na kontakt@nexuslab.pl.',
        })

    cache.set(rate_key, attempts + 1, 60 * 60)
    return render(request, template, {'success': True})
