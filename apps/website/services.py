"""Service landing pages (/uslugi/...): content as data, rendered by templates/website/service_detail.html.

Only real facts here: every example must point to a project that exists (case study or homepage card).
Numbers come from the homepage / case studies; do not invent new ones.
"""

PROCESS = [
    ('Bezpłatna rozmowa', 'Opowiadasz, co zajmuje najwięcej czasu. Mówię wprost, co warto zautomatyzować, a co nie ma sensu.'),
    ('Propozycja i wycena', 'Dostajesz opis rozwiązania, zakres, termin i cenę. Wiesz, za co płacisz, zanim zaczniemy.'),
    ('Wdrożenie', 'Buduję, testuję na Twoich danych i podłączam do narzędzi, których już używasz.'),
    ('Wsparcie i rozwój', 'Pilnuję, żeby działało. Gdy pojawią się nowe potrzeby, rozbudowujemy system krok po kroku.'),
]

SERVICES = [
    {
        'slug': 'automatyzacje-n8n',
        'nav': 'Automatyzacje n8n',
        'head_title': 'Automatyzacje n8n i wdrożenie n8n dla firm',
        'title': 'Automatyzacje n8n: powtarzalna praca robi się sama',
        'description': 'Wdrożenie n8n i automatyzacje procesów w firmie: przepisywanie danych, powiadomienia, '
                       'boty w komunikatorach, integracje z arkuszem Google, mailem i CRM. Od rozmowy do wdrożenia.',
        'eyebrow': 'Usługa · Automatyzacje',
        'lead': 'Przepisywanie danych z maila do arkusza, ręczne sprawdzanie stron, przypominanie klientom, '
                'kopiowanie informacji między programami. Takie zadania łączę w automatyczne przepływy w n8n, '
                'które działają w tle, w narzędziach, których już używasz.',
        'card': 'Przepływy, które przenoszą dane, wysyłają powiadomienia i odpowiadają w komunikatorze, bez ręcznej roboty.',
        'pains': [
            'Te same dane przepisujesz z maila do arkusza albo CRM',
            'Codziennie ręcznie sprawdzasz, czy coś nowego pojawiło się na stronie lub w skrzynce',
            'Informacja od klienta ginie, bo nikt nie przekazał jej dalej',
            'Raport albo zestawienie składasz co tydzień z kilku miejsc',
        ],
        'offer_title': 'Co mogę zautomatyzować',
        'offer': [
            ('Przepływ danych', 'z formularzy, maili i arkuszy do miejsca, w którym są potrzebne, np. Google Sheets albo CRM'),
            ('Powiadomienia', 'mail, SMS albo wiadomość w komunikatorze, gdy dzieje się coś ważnego'),
            ('Boty w komunikatorach', 'np. w Telegramie: przyjmują tekst, głosówkę albo zdjęcie i zapisują to, co trzeba'),
            ('Monitorowanie stron', 'cykliczne sprawdzanie ogłoszeń lub ofert i wysyłka tylko tego, co pasuje'),
            ('AI w przepływie', 'odczytanie danych z wiadomości, transkrypcja nagrania, przygotowanie odpowiedzi'),
            ('Integracje', 'połączenie narzędzi, które same ze sobą nie rozmawiają'),
        ],
        'why': [
            ('Dlaczego n8n', 'To narzędzie do automatyzacji, które może działać na Twoim własnym serwerze. '
                             'Dane nie muszą przechodzić przez zewnętrzną platformę, a koszt nie rośnie z każdą wykonaną operacją.'),
            ('Najpierw prototyp', 'Często zaczynam od szybkiego przepływu w n8n, żeby sprawdzić pomysł w praktyce. '
                                  'Tak powstał Flowmail: najpierw kilka workflowów w n8n, potem pełna aplikacja.'),
        ],
        'examples': [
            {'title': 'Asystent telefoniczny apteki', 'text': 'Asystent głosowy odbiera telefon, rozmowa trafia do arkusza, a gdy trzeba oddzwonić, farmaceuta dostaje SMS z imieniem, numerem i sprawą. Przepływ zbudowany w n8n.', 'url': '/uslugi/asystent-glosowy-ai/', 'label': 'Więcej o asystencie głosowym'},
            {'title': 'Asystent wydatków', 'text': 'Bot w Telegramie: głosówka, zdjęcie paragonu albo krótka wiadomość wystarczy, żeby wydatek trafił do arkusza. Komenda zwraca sumę w kategorii. Projekt własny.', 'url': '/#wiecej-realizacji', 'label': 'Zobacz w realizacjach'},
            {'title': 'Gratka Alerts', 'text': 'System co godzinę sprawdza nowe ogłoszenia mieszkań i wysyła maila o ofertach pasujących do kryteriów. Własny produkt.', 'url': 'https://gratka.nexuslab.pl/', 'label': 'Otwórz aplikację'},
        ],
        'faq': [
            ('Ile trwa wdrożenie automatyzacji?', 'Prosta automatyzacja, np. bot w komunikatorze albo przekazywanie danych do arkusza, to zwykle kilka dni. Dokładny termin podaję w wycenie, po rozmowie.'),
            ('Ile kosztuje utrzymanie?', 'Usługi takie jak AI, SMS-y czy serwer są rozliczane według zużycia, zwykle bezpośrednio na Twoim koncie u dostawcy. Przy prostych automatyzacjach to często kilka–kilkanaście złotych miesięcznie. Szacunek kosztów stałych jest częścią wyceny.'),
            ('Czy muszę umieć obsługiwać n8n?', 'Nie. Automatyzacja działa w tle, a Ty korzystasz z narzędzi, których już używasz: maila, arkusza, komunikatora. Jeśli chcesz zaglądać do n8n, pokażę, jak to robić.'),
            ('Co jeśli coś przestanie działać?', 'Monitoruję wdrożone rozwiązania i naprawiam błędy. Gdy zmieni się np. strona, z której pobierane są dane, dostosowuję przepływ.'),
        ],
        'cta_title': 'Masz zadanie, które robisz ręcznie co tydzień?',
        'cta_text': 'Opisz je w kilku zdaniach. Powiem wprost, czy warto je zautomatyzować i ile to zajmie.',
    },
    {
        'slug': 'ai-dla-sprzedazy',
        'nav': 'AI dla sprzedaży',
        'head_title': 'AI dla działu sprzedaży: asystent maili i obsługi klienta',
        'title': 'AI dla sprzedaży: maile do klientów w kilkadziesiąt sekund, a nie w kwadrans',
        'description': 'Asystent AI dla handlowców i doradców: pisze spersonalizowane maile na podstawie historii klienta '
                       'i Twoich materiałów, podpowiada odpowiedzi, przygotowuje newslettery. Człowiek zatwierdza każdy tekst.',
        'eyebrow': 'Usługa · AI w sprzedaży i obsłudze klienta',
        'lead': 'Przez 25 lat pracowałem w sprzedaży, z czego 15 w Key Account Management. Wiem, ile czasu zabierają maile, '
                'oferty i odpowiedzi na pytania klientów. Buduję asystentów AI, którzy znają Twoich klientów i Twoje '
                'materiały, a handlowiec tylko sprawdza i wysyła.',
        'card': 'Asystent, który pisze maile i odpowiedzi na podstawie historii klienta i Twoich materiałów. Ty zatwierdzasz.',
        'pains': [
            'Ten sam mail piszesz po raz dziesiąty, za każdym razem trochę inaczej',
            'Szukanie materiałów do odpowiedzi zajmuje więcej czasu niż samo pisanie',
            'Kontakt z częścią klientów się urywa, bo nie ma kiedy do nich napisać',
            'Ogólny czat AI nie zna Twoich produktów i potrafi zmyślać',
        ],
        'offer_title': 'Co może robić asystent',
        'offer': [
            ('Maile do klientów', 'z krótkiej notatki albo nagrania głosowego powstaje gotowy, spersonalizowany mail'),
            ('Baza wiedzy', 'asystent korzysta z Twoich materiałów: opisów produktów, badań, historii klientów'),
            ('Kontrola treści', 'drugi model AI sprawdza tekst, a człowiek zatwierdza go przed wysłaniem'),
            ('Podpowiedzi odpowiedzi', 'jak odpowiedzieć klientowi na konkretne pytanie, z historią porad'),
            ('Newslettery', 'do wybranej grupy klientów, przygotowane z pomocą AI'),
            ('Baza klientów', 'historia kontaktów, grupy, przypomnienia i zaplanowane wysyłki w jednym miejscu'),
        ],
        'why': [
            ('Człowiek ma ostatnie słowo', 'AI może się pomylić, dlatego nic nie wychodzi bez akceptacji handlowca. '
                                          'Mail wysyła się z jego adresu, jego słowami po poprawkach.'),
            ('Twoje materiały, nie internet', 'Asystent pisze na podstawie Twojej bazy wiedzy i historii klienta, '
                                              'a nie ogólnej wiedzy modelu. To ogranicza ryzyko zmyślania.'),
        ],
        'examples': [
            {'title': 'Flowmail', 'text': 'Aplikacja dla doradców sprzedaży: spersonalizowany mail do klienta w około 30 sekund, na podstawie notatki, historii klienta i ponad 3 700 materiałów branżowych. 23 doradców używa jej na co dzień.', 'url': '/realizacje/flowmail/', 'label': 'Case study: Flowmail'},
        ],
        'faq': [
            ('Czy AI może się pomylić?', 'Tak, dlatego tam, gdzie AI pisze tekst, ostatnie słowo ma człowiek. We Flowmail doradca sprawdza i zatwierdza każdy mail przed wysłaniem.'),
            ('Skąd asystent wie, co napisać?', 'Korzysta z bazy wiedzy zbudowanej z Twoich materiałów i z historii klienta. Na tej podstawie dobiera treść do konkretnej osoby.'),
            ('Czy maile wychodzą z mojego adresu?', 'Tak. Klient dostaje wiadomość od swojego handlowca, a nie od systemu.'),
            ('Ile to kosztuje?', 'Zależy od zakresu, dlatego zaczynamy od bezpłatnej rozmowy. Po niej dostajesz konkretną wycenę za cały projekt.'),
        ],
        'cta_title': 'Twoi handlowcy piszą maile od zera?',
        'cta_text': 'Porozmawiajmy, jak mógłby wyglądać asystent zbudowany na Twoich materiałach i Twoim sposobie pracy z klientami.',
    },
    {
        'slug': 'aplikacje-do-zamowien',
        'nav': 'Aplikacje do zamówień',
        'head_title': 'Aplikacja do zamówień B2B i zamówień online dla firm',
        'title': 'Aplikacje do zamówień: zamiast Excela, ankiet i telefonów',
        'description': 'Aplikacje do zamówień na telefon: zamówienia B2B do hurtowni z rabatami i promocjami, '
                       'zamawianie posiłków z saldem i listą porcji. Zamiast arkusza Excel, ankiet Google i liczenia ręcznie.',
        'eyebrow': 'Usługa · Aplikacje webowe',
        'lead': 'Zamówienia zbierane w Excelu, ankietą albo przez telefon to dużo ręcznego liczenia i łatwe pomyłki. '
                'Buduję aplikacje, w których klient albo handlowiec zamawia z telefonu, a reszta liczy się sama: '
                'rabaty, promocje, minimum, saldo, podsumowania.',
        'card': 'Zamówienia z telefonu zamiast Excela i ankiet. Rabaty, promocje, saldo i podsumowania liczą się same.',
        'pains': [
            'Zamówienia składacie w arkuszu Excel z setkami pozycji',
            'Handlowiec w trasie musi zatrzymać się i otworzyć laptopa, żeby przyjąć zamówienie',
            'Zamówienia zbieracie ankietą Google i liczycie ręcznie',
            'Ktoś musi pilnować rabatów, promocji i rozliczeń',
        ],
        'offer_title': 'Co może mieć aplikacja',
        'offer': [
            ('Zamawianie z telefonu', 'aplikacja w przeglądarce z ikoną na ekranie, bez instalowania ze sklepu'),
            ('Cennik i rabaty', 'rabat klienta, promocje od ilości, minimum logistyczne naliczane automatycznie'),
            ('Wyszukiwarka i filtry', 'np. lista najczęściej zamawianych produktów, krótkie daty, promocje'),
            ('Wysyłka zamówienia', 'mail z tabelą i gotowym plikiem Excel do hurtowni lub kuchni'),
            ('Konta i role', 'osobne widoki dla klienta, handlowca, kuchni czy administratora'),
            ('Zestawienia', 'historia zamówień, podsumowania miesięczne, eksport do Excela'),
        ],
        'why': [
            ('Działa na telefonie', 'Aplikacja otwiera się w przeglądarce i dodaje jako ikona na ekran główny. '
                                    'Nie trzeba publikować jej w sklepie ani niczego instalować.'),
            ('Excel zostaje tam, gdzie się przydaje', 'Cennik możesz dalej wgrywać z pliku Excel, a hurtownia '
                                                      'dostaje zamówienie w formacie, który zna.'),
        ],
        'examples': [
            {'title': 'Zamówienia B2B w branży farmaceutycznej', 'text': 'Handlowiec składa zamówienie do hurtowni z telefonu, nawet na poboczu drogi. Ponad 400 produktów, TOP 50, krótkie daty, ceny netto i sugerowane ceny detaliczne. Z 6 kroków w Excelu zrobiły się 4.', 'url': '/realizacje/zamowienia-b2b/', 'label': 'Case study: Zamówienia B2B'},
            {'title': 'System zamawiania posiłków', 'text': 'Rodzice zamawiają obiady z telefonu na cały tydzień, saldo odlicza się samo, a kuchnia ma listę porcji i wydaje posiłki z tabletu. Ocena rodziców: 4,9 / 5.', 'url': '/realizacje/zamawianie-posilkow/', 'label': 'Case study: Zamawianie posiłków'},
        ],
        'faq': [
            ('Ile trwa zbudowanie aplikacji?', 'Aplikacja z kontami użytkowników to zwykle kilka tygodni. Dokładny termin podaję w wycenie, po rozmowie.'),
            ('Czy klient musi instalować aplikację?', 'Nie. Otwiera link w przeglądarce telefonu i może dodać ikonę na ekran główny.'),
            ('Czy mogę dalej korzystać z Excela?', 'Tak. Cennik czy listę produktów można wgrywać z pliku Excel, a zestawienia eksportować do Excela.'),
            ('Co jeśli będę potrzebować nowych funkcji?', 'Aplikacja jest zbudowana pod Twoją firmę, więc rozbudowujemy ją krok po kroku, np. o stany magazynowe czy integrację z systemem hurtowni.'),
        ],
        'cta_title': 'Zbieracie zamówienia w Excelu albo ankietą?',
        'cta_text': 'Pokaż mi, jak to wygląda dziś. Powiem, jak mogłaby wyglądać aplikacja dla Twojej firmy.',
    },
    {
        'slug': 'asystent-glosowy-ai',
        'nav': 'Asystent głosowy AI',
        'head_title': 'Asystent głosowy AI: automatyczne odbieranie telefonów w firmie',
        'title': 'Asystent głosowy AI: telefon odebrany, sprawa zapisana, nikt nie odchodzi z niczym',
        'description': 'Asystent głosowy AI odbiera telefony, gdy nie możesz: rozmawia z klientem, zapisuje sprawę '
                       'w arkuszu i wysyła SMS, do kogo oddzwonić. Dla aptek, gabinetów, sklepów i firm usługowych.',
        'eyebrow': 'Usługa · Asystent telefoniczny AI',
        'lead': 'Telefon dzwoni akurat wtedy, gdy obsługujesz klienta na miejscu. Asystent głosowy odbiera połączenie, '
                'rozmawia naturalnym głosem, przyjmuje wiadomość, a gdy trzeba oddzwonić, '
                'wysyła Ci SMS z imieniem, numerem i tematem.',
        'card': 'Odbiera telefon, gdy nie możesz, zapisuje sprawę i wysyła SMS, do kogo oddzwonić.',
        'pains': [
            'Telefon dzwoni, kiedy obsługujesz klienta przy ladzie lub w gabinecie',
            'Nieodebrane połączenia to klienci, którzy dzwonią do konkurencji',
            'Dzwonią nie tylko klienci, ale też dostawcy i przedstawiciele, a każda rozmowa odrywa od pracy',
            'Kartka z numerem do oddzwonienia gubi się w ciągu dnia',
        ],
        'offer_title': 'Co robi asystent',
        'offer': [
            ('Odbiera połączenia', 'gdy nikt nie odbierze, albo zawsze, w zależności od ustawień przekierowania'),
            ('Rozmawia z klientem', 'naturalnym głosem, po polsku, uprzejmie i krótko, jedno pytanie naraz'),
            ('Rozpoznaje, kto dzwoni', 'klient, dostawca, przedstawiciel czy inna firma, bez wypytywania wprost'),
            ('Dba o szczegóły', 'powtarza numer cyfra po cyfrze, a trudne nazwy produktów i firm potwierdza, literując'),
            ('Zapisuje sprawę', 'każda rozmowa trafia do arkusza: kto dzwonił, numer, czego dotyczyła'),
            ('Wysyła SMS', 'gdy trzeba oddzwonić, dostajesz wiadomość z imieniem, numerem i sprawą'),
            ('Zna swoje granice', 'nie doradza, niczego nie obiecuje i nie zgaduje, tylko przekazuje sprawę Tobie'),
        ],
        'why': [
            ('Działa z Twoim numerem', 'Klienci dzwonią na ten sam numer co zawsze. Połączenie trafia do asystenta '
                                       'przez przekierowanie u operatora, np. gdy nikt nie odbierze.'),
            ('Arkusz i SMS zamiast nowego programu', 'Nie musisz uczyć się nowego systemu. '
                                                     'Rozmowy lądują w arkuszu Google, a pilne sprawy w SMS-ie.'),
        ],
        'examples': [
            {'title': 'Asystent telefoniczny apteki', 'text': 'Asystent głosowy dla apteki: odbiera telefon, rozmowa trafia do arkusza, a gdy trzeba oddzwonić, farmaceuta dostaje SMS z imieniem, numerem i sprawą. Projekt w fazie pilotażu.', 'url': '/#wiecej-realizacji', 'label': 'Zobacz w realizacjach'},
        ],
        'faq': [
            ('Czy klienci muszą dzwonić na inny numer?', 'Nie. Ustawia się przekierowanie u operatora, np. gdy nikt nie odbierze po kilku sygnałach. Klient dzwoni na ten sam numer co zawsze.'),
            ('Czy asystent mówi po polsku?', 'Tak, rozmawia po polsku naturalnym głosem.'),
            ('Co się dzieje z nagraniami i danymi?', 'Zapisywane są tylko informacje potrzebne do obsługi sprawy, np. imię, numer i temat rozmowy. Zakres danych ustalamy na początku, zgodnie z RODO.'),
            ('Ile to kosztuje?', 'Rozmowy i SMS-y są rozliczane według zużycia u dostawców. Szacunek kosztów miesięcznych dostajesz w wycenie, razem z ceną wdrożenia.'),
        ],
        'cta_title': 'Ile telefonów nie odbierasz w ciągu dnia?',
        'cta_text': 'Porozmawiajmy, czy asystent głosowy ma sens w Twojej firmie. Jeśli nie, powiem to wprost.',
    },
]

SERVICES_BY_SLUG = {s['slug']: s for s in SERVICES}
