# TODO

## Portfolio nexuslab.pl

- [x] Naprawa 500 na gratka.nexuslab.pl (NoReverseMatch `website:pricing`)
- [x] Strona główna jako portfolio (projekty, automatyzacje n8n, O mnie, opinie, FAQ, współpraca)
- [x] Sekcja kontakt + formularz zgłoszeniowy (mail, honeypot, rate limit)
- [x] WhiteNoise — pliki statyczne na produkcji
- [x] Zrzuty / mockupy / wideo projektów
- [x] Logo wektorowe + favicon
- [x] SEO: meta, Open Graph, JSON-LD, robots.txt, sitemap.xml
- [x] Polityka prywatności + klauzula przy formularzu
- [x] Liczby Flowmail, status sprzedajm.pl „W trakcie wdrożenia”
- [x] Deploy i weryfikacja na produkcji (logo, obrazki, wideo, formularz) (26.11)
- [ ] Test formularza — czy mail dochodzi na kontakt@nexuslab.pl (testowa wiadomość wysłana 26.11, potwierdzić odbiór)
- [ ] Google Search Console: domena + `sitemap.xml`
- [ ] Facebook Sharing Debugger — odświeżyć podgląd linku
- [ ] Polityka prywatności: adres / NIP administratora
- [ ] Sekretarka: rozmyć nazwisko „Jozef Owicz”, jeśli to prawdziwa osoba
- [ ] Tailwind z CDN → zbudowany CSS (wydajność) — strona główna już na `site.css`, zostały panel Gratka, logowanie, cennik, polityka
- [ ] Lokalne zmiany na serwerze (`config/settings/production.py`, `gunicorn_config.py`) przenieść do repo albo .env
- [ ] Analityka bez cookies (Plausible / Umami)
- [ ] Link do LinkedIna, case study Flowmail
- [x] Zamazane nazwy botów w makietach (asystent wydatków, lista zakupów) (18.11)
- [x] „O mnie” o korzyściach dla klienta, technologie w pasku na dole, teksty bez długich myślników (18.11)
- [x] Projekt „Zamawianie obiadów” w portfolio, bez nazwy szkoły, nowy film z danymi demo (23.11)
- [x] Projekt „PDF do Worda” w portfolio: film z prawdziwego programu (pismo demo), przycisk „Chcę mieć” (23.11)
- [x] Opinie rodziców z aplikacji obiadów (panel /admin/opinie, tylko ze zgodą) dodać do sekcji „Opinie” (26.11)
- [x] Nowa odsłona strony głównej: jasny motyw, case study, Yango anonimowo, fonty lokalnie (26.11, commit `40471f5`)
- [ ] Etap 2: cennik i polityka prywatności na `base_site.html` w jasnym stylu
- [ ] Nowy og-image w jasnych kolorach (obecny jest ciemny)
- [ ] CLAUDE.md: SSH na porcie 2222 (`ssh nexuslab`), opis `base_site.html` i `site.css`
- [ ] Zdjęcie ze spotkania biznesowego do sekcji „O mnie” (portret przejdzie do kontaktu)

## GitHub

- [x] Profilowy README (`zbigniew-szafranski/zbigniew-szafranski`)
- [x] README repo NexusLab
- [x] Stare repozytoria → prywatne
- [ ] Bio + link nexuslab.pl w profilu
- [ ] Opis + topics repo NexusLab

## Gratka Alerts — scraper n8n

- [x] Diagnoza i poprawiony workflow (`~/Downloads/Agent Gratka - poprawiony.json`)
- [ ] Import do n8n, test ręczny, wyłączenie starego workflow (checklista w `GRATKA.md`)
- [ ] Sprzątanie bazy: „undefined”, prefiks „piętro”, oferty spoza budżetu
- [ ] Zdecydować: `GRATKA.md` do `.gitignore` (repo publiczne)
