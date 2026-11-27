import json
import logging
import os
from datetime import datetime, timezone

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST

from apps.subscriptions.models import Plan

from .forms import ContactForm

logger = logging.getLogger(__name__)

CONTACT_RATE_LIMIT = 5  # submissions per IP per hour


FAQ = [
    {
        'q': 'Ile trwa wdrożenie?',
        'a': 'Zależy od zakresu. Prosta automatyzacja, np. bot w komunikatorze albo przekazywanie '
             'danych do arkusza, to zwykle kilka dni. Aplikacja z kontami użytkowników to kilka '
             'tygodni. Dokładny termin podaję w wycenie, po rozmowie.',
    },
    {
        'q': 'Ile to kosztuje?',
        'a': 'Zależy od zakresu, dlatego zaczynamy od bezpłatnej rozmowy. Po niej dostajesz '
             'konkretną wycenę za cały projekt, bez niespodzianek w trakcie.',
    },
    {
        'q': 'Kto płaci za AI, SMS-y i serwer?',
        'a': 'Te usługi są rozliczane według zużycia, zwykle bezpośrednio na Twoim koncie u dostawcy, '
             'więc masz pełną kontrolę nad kosztami. Przy prostych automatyzacjach to często '
             'kilka–kilkanaście złotych miesięcznie. Szacunek kosztów stałych jest częścią wyceny.',
    },
    {
        'q': 'Czy AI może się pomylić?',
        'a': 'Tak, dlatego tam, gdzie AI pisze tekst albo odczytuje dane, ostatnie słowo ma człowiek. '
             'Na przykład we Flowmail doradca sprawdza i zatwierdza każdy mail przed wysłaniem.',
    },
    {
        'q': 'Muszę znać się na technologii?',
        'a': 'Nie. Rozwiązanie działa w narzędziach, których już używasz: mailu, komunikatorze, '
             'arkuszu Google czy telefonie. Pokazuję, jak z niego korzystać, i zostawiam krótką instrukcję.',
    },
    {
        'q': 'Co jeśli coś przestanie działać?',
        'a': 'Monitoruję wdrożone rozwiązania i naprawiam błędy. Część automatyzacji zależy od '
             'zewnętrznych serwisów: gdy zmieni się np. strona, z której pobierane są dane, albo '
             'usługa dostawcy, trzeba rozwiązanie dostosować i ja to robię.',
    },
    {
        'q': 'Czy pracujesz zdalnie?',
        'a': 'Tak. Rozmowy, wdrożenie i wsparcie prowadzę zdalnie, dla klientów z całej Polski.',
    },
]


# Quoted from the Flowmail landing page (panelgw.com)
TESTIMONIALS = [
    {
        'quote': 'Ta aplikacja jest po prostu rewelacyjna: wszystkie potrzebne informacje w jednym '
                 'miejscu, generowanie maili nieprawdopodobnie usprawnione, a oszczędność czasu — '
                 'bezcenna. Szczerze polecam i dziękuję, bo już widzę, jak bardzo mi to pomoże.',
        'name': 'Agnieszka',
        'role': 'Doradczyni Green Ways · użytkowniczka Flowmail',
    },
    {
        'quote': 'Polecam wszystkim, aplikacja jest super ułatwieniem pracy. Dziękuję za możliwość '
                 'korzystania z niej.',
        'name': 'Danuta',
        'role': 'Doradczyni Green Ways · użytkowniczka Flowmail',
    },
]


# Parents' reviews of the meal ordering app, as written in the app (spelling fixes only).
# All 9 ratings: 8 x 5 stars + 1 x 4 stars; 7 with a comment. One commented review is
# deliberately not published, two ratings have no comment.
MEAL_REVIEWS = [
    {'quote': 'Bardzo przejrzysty i intuicyjny interfejs, zaoszczędziłem masę czasu w porównaniu '
              'do poprzedniego sposobu z Excelem', 'name': 'Tomasz'},
    {'quote': 'Prosta, intuicyjna, przejrzysta, spełniająca swoją funkcję - po prostu idealna! '
              'Do tego ciągle rozwijana :)', 'name': 'Maciej'},
    {'quote': 'Jestem Ci bardzo wdzięczna za tę stronę. Takiej organizacji w tej szkole potrzebujemy!',
     'name': 'Kamila'},
    {'quote': 'Świetna aplikacja! Bardzo instynktowna i mega pomocna! Dzięki!', 'name': 'Marta'},
    {'quote': 'Intuicyjna, funkcjonalna, prosta.', 'name': 'Paulina'},
    {'quote': 'Wszystko bardzo przejrzyste', 'name': 'Katarzyna'},
]
MEAL_RATING = {'average': '4,9', 'count': 9, 'with_comment': 7}


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
        'testimonials': TESTIMONIALS,
        'meal_reviews': MEAL_REVIEWS,
        'meal_rating': MEAL_RATING,
    })


def privacy(request):
    return render(request, 'website/privacy.html', {'updated': '18 października 2026'})


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /accounts/',
        '',
        'Sitemap: https://nexuslab.pl/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines) + '\n', content_type='text/plain')


SITEMAP_PAGES = [
    ('/', 'website/index.html'),
    ('/cennik/', 'website/pricing.html'),
    ('/polityka-prywatnosci/', 'website/privacy.html'),
]


def _template_lastmod(template_name):
    """Last modification date of a template file (updated by git pull on deploy)."""
    try:
        origin = get_template(template_name).origin.name
        return datetime.fromtimestamp(os.path.getmtime(origin), tz=timezone.utc).date().isoformat()
    except Exception:
        return None


def sitemap_xml(request):
    urls = ''
    for path, template_name in SITEMAP_PAGES:
        lastmod = _template_lastmod(template_name)
        lastmod_tag = f'<lastmod>{lastmod}</lastmod>' if lastmod else ''
        urls += f'<url><loc>https://nexuslab.pl{path}</loc>{lastmod_tag}</url>'
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    )
    return HttpResponse(xml, content_type='application/xml')


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
