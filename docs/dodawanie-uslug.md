# Jak dodać nową usługę na nexuslab.pl

Strony usług (`/uslugi/...`) nie mają osobnych szablonów. Cała treść jest w jednym pliku:
**`apps/website/services.py`**, w liście `SERVICES`. Jeden słownik = jedna usługa.

Po dodaniu słownika **automatycznie** pojawia się:
- strona `https://nexuslab.pl/uslugi/<slug>/`
- kafelek na stronie zbiorczej `/uslugi/`
- link w stopce (kolumna „Usługi”) i w sekcji „Inne usługi” na pozostałych stronach usług
- wpis w `sitemap.xml`
- dane strukturalne dla Google: `Service`, `FAQPage`, `BreadcrumbList`

Nie trzeba ruszać szablonów, `urls.py` ani `views.py`.

---

## Krok po kroku

### 1. Skopiuj szablon na koniec listy `SERVICES`

Wklej go przed zamykającym `]` listy i uzupełnij:

```python
    {
        'slug': 'chatbot-ai',                      # adres: /uslugi/chatbot-ai/ (małe litery, bez polskich znaków, myślniki)
        'nav': 'Chatbot AI',                       # krótka nazwa: menu w stopce, okruszki, kafelek
        'head_title': 'Chatbot AI dla firmy',      # tytuł w Google (dopisuje się „| NexusLab”); fraza, którą wpisują klienci
        'title': 'Chatbot AI: ...',                # nagłówek H1 na stronie
        'description': '...',                      # opis w wynikach Google, ok. 140–160 znaków
        'eyebrow': 'Usługa · Chatboty',            # mały pomarańczowy napis nad H1 (bez „Usługa · ” na kafelku)
        'lead': '...',                             # 2–3 zdania pod nagłówkiem
        'card': '...',                             # 1 zdanie na kafelku na /uslugi/
        'pains': [                                 # „Brzmi znajomo?” – 4 problemy słowami klienta
            '...',
            '...',
            '...',
            '...',
        ],
        'offer_title': 'Co może robić chatbot',    # nagłówek listy funkcji
        'offer': [                                 # 4–6 par: (tytuł, opis)
            ('Tytuł', 'opis małą literą, bez kropki na końcu'),
            ('Tytuł', 'opis'),
        ],
        'why': [                                   # dokładnie 2 ciemne kafelki z argumentami
            ('Argument 1', 'Pełne zdania z kropką.'),
            ('Argument 2', 'Pełne zdania z kropką.'),
        ],
        'examples': [                              # min. 1 PRAWDZIWY projekt
            {'title': 'Nazwa projektu',
             'text': 'Co robi i dla kogo.',
             'url': '/realizacje/flowmail/',       # case study, '/#wiecej-realizacji' albo pełny adres https://
             'label': 'Case study: Flowmail'},     # tekst linku (strzałka → dodaje się sama)
        ],
        'faq': [                                   # 3–5 pytań; trafiają też do Google jako FAQ
            ('Pytanie?', 'Odpowiedź.'),
        ],
        'cta_title': 'Pytanie do klienta?',        # nagłówek ciemnego banera na dole
        'cta_text': 'Jedno, dwa zdania zachęty do rozmowy.',
    },
```

Wszystkie pola są wymagane. Kolejność na liście = kolejność kafelków i linków w stopce.

### 2. Sprawdź lokalnie

```bash
python3 -m py_compile apps/website/services.py     # literówka w nawiasach/przecinkach wyjdzie tutaj
```

Najczęstszy błąd: brak przecinka po `}` albo po elemencie listy.

### 3. Wdróż

```bash
git add apps/website/services.py
git commit -m "website: service page <nazwa>"
git push
ssh nexuslab 'cd /var/www/nexuslab && ./deploy.sh'
```

### 4. Sprawdź na produkcji

- `https://nexuslab.pl/uslugi/<slug>/` otwiera się (200),
- nowa usługa jest na `https://nexuslab.pl/uslugi/` i w stopce,
- `https://nexuslab.pl/sitemap.xml` zawiera nowy adres,
- opcjonalnie: [Rich Results Test](https://search.google.com/test/rich-results) wykrywa FAQ bez błędów.

### 5. Google Search Console

Sprawdzanie adresu URL → wklej adres nowej usługi → **„Poproś o zindeksowanie”**.

---

## Zasady pisania treści

1. **Tylko prawdziwe fakty i liczby.** Liczby bierz ze strony głównej, case studies albo dokumentacji projektu. Nie dopisuj statystyk, których nie da się pokazać.
2. **Każda usługa ma prawdziwy przykład** w `examples`. Jeśli projekt jest w trakcie albo w pilotażu, napisz to wprost (jak przy asystencie głosowym).
3. **Anonimowość klientów.** Nie podawaj nazw firm, marek ani szkół, jeśli klient się na to nie zgodził (zamówienia B2B i system posiłków są anonimowe).
4. **Fraza z Google w `head_title` i `title`.** Pisz tak, jak klient szuka, np. „chatbot AI dla firmy”, a nie „rozwiązania konwersacyjne”.
5. **Problemy słowami klienta.** `pains` to zdania, które klient mógłby powiedzieć sam, np. „Ten sam mail piszę po raz dziesiąty”.
6. **Bez cen, o ile nie są ustalone.** W FAQ o koszcie pisz „zależy od zakresu, wycena po rozmowie” albo podawaj tylko koszty, które już są na stronie (np. „kilka–kilkanaście zł miesięcznie” przy prostych automatyzacjach).

## Zmiana lub usunięcie usługi

- **Zmiana treści:** edytuj słownik w `services.py`, potem kroki 2–4.
- **Zmiana `slug`:** zmienia adres strony. Stary adres przestanie działać (404), więc dodaj przekierowanie w `apps/website/urls.py`, np.
  `path('uslugi/stary-slug/', RedirectView.as_view(url='/uslugi/nowy-slug/', permanent=True)),`
  **przed** linią `path('uslugi/<slug:slug>/', ...)`.
- **Usunięcie:** usuń słownik i też dodaj przekierowanie, np. na `/uslugi/`.

## Gdzie co jest

| Co | Plik |
|---|---|
| Treść usług, kroki współpracy (`PROCESS`) | `apps/website/services.py` |
| Wygląd strony usługi | `templates/website/service_detail.html` |
| Strona zbiorcza `/uslugi/` | `templates/website/services.html` |
| Widoki, dane strukturalne, sitemap | `apps/website/views.py` (`services`, `service_detail`, `_sitemap_entries`) |
| Link w stopce | `apps/website/context_processors.py` + `templates/website/base_site.html` |
| Style | `static/css/site.css`, sekcja „Service pages (/uslugi/)” |
