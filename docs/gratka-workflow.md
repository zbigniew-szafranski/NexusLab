# n8n Workflow - Gratka Scraper

## Status: AKTYWNY na n8n.nexuslab.pl

## Overview

Workflow scrapuje Gratka.pl co godzinę, wykrywa nowe oferty i wysyła emaile.
Konfiguracja użytkowników jest zarządzana przez Django (dashboard na gratka.nexuslab.pl),
n8n tylko odczytuje konfiguracje z bazy i wykonuje scraping.

## Architektura

### Przepływ danych
1. Użytkownik konfiguruje kryteria przez Django dashboard (gratka.nexuslab.pl)
2. Django zapisuje konfigurację do tabeli `gratka_userconfig`
3. n8n co godzinę odczytuje aktywne konfiguracje z PostgreSQL
4. Dla każdego użytkownika: buduje URL, scrapuje Gratka.pl, zapisuje nowe oferty
5. Nowe oferty widoczne na dashboardzie + email do użytkownika

### Stary workflow "Gratka - Config Manager"
Webhook do zapisu konfiguracji przez n8n - **WYŁĄCZONY/DO USUNIĘCIA**.
Django teraz obsługuje zapis konfiguracji bezpośrednio do bazy.

## Workflow Structure

```
Schedule Trigger (co 1h)
    |
Read Config (PostgreSQL) - odczytaj konfiguracje wszystkich aktywnych userów
    |
SplitInBatches (batch size: 1) - przetwarzaj jednego usera naraz
    |
Build URL (Code) - generuj URL Gratka.pl z kryteriów usera
    |
HTTP Request - pobierz HTML z Gratka.pl
    |
HTML Extract - wyciagnij dane (price, title, area, rooms, floor, url)
    |
Code in JavaScript - transform arrays -> individual items + dopisz user_id/email
    |
Dodanie gratka.pl (Set) - dodaj pelny link
    |
Uzyskanie ID (Set) - extract offer_id z URL
    |
Execute SQL query - INSERT INTO gratka_useroffer ... ON CONFLICT DO NOTHING RETURNING *
    |
Is new offer? (IF) - czy SQL zwrocil dane?
    |-- TRUE -> Send Email (Gmail)
    |-- FALSE -> Duplicate - skip (NoOp)
    |
(loop wraca do SplitInBatches dla kolejnego usera)
```

## Node Details

### 1. Schedule Trigger
```
Type: n8n-nodes-base.scheduleTrigger
Interval: 1 hour
```

### 2. Read Config
```
Type: n8n-nodes-base.postgres
Operation: Execute Query
Credential: Postgres account (nexuslab_db)

Query:
SELECT
    u.id as user_id,
    u.email,
    uc.lokalizacja,
    uc.cena_min,
    uc.cena_max,
    uc.metraz_min,
    uc.metraz_max,
    uc.balkon,
    uc.garaz,
    uc.piwnica
FROM gratka_userconfig uc
JOIN auth_user u ON uc.user_id = u.id
WHERE uc.is_active = TRUE
  AND u.is_active = TRUE;
```

Output: Array of user configs (jeden wiersz per aktywny user)

**WAZNE:** Email do powiadomien pobierany z `auth_user.email` (konto Django),
nie z osobnego pola - pole email w UserConfig ustawiane automatycznie z konta.

### 3. SplitInBatches
```
Type: n8n-nodes-base.splitInBatches
Batch Size: 1
```

Przetwarza jednego usera naraz. Zapobiega:
- mieszaniu ofert miedzy userami
- rate limitingowi z Gratka.pl (sekwencyjne requesty)
- problemom z referencjami $('Build URL').first()

Drugie wyjscie (po przetworzeniu wszystkich) -> koniec workflow.

### 4. Build URL
```
Type: n8n-nodes-base.code

JavaScript:
const config = $input.first().json;

let url = `https://gratka.pl/nieruchomosci/mieszkania/`;

if (config.balkon) {
  url += 'z-balkonem/';
}

url += `${config.lokalizacja}/wtorny?`;
url += `cena-calkowita:max=${config.cena_max}&cena-calkowita:min=${config.cena_min}&`;

if (config.garaz) {
  url += 'miejsce-parkingowe[0]=garaz-parking&';
}

url += 'ogloszenie-zawiera[0]=cena';

if (config.metraz_min) {
  url += `&powierzchnia:min=${config.metraz_min}`;
}
if (config.metraz_max) {
  url += `&powierzchnia:max=${config.metraz_max}`;
}

return {
  json: {
    url: url,
    user_id: config.user_id,
    email: config.email
  }
};
```

### 5. HTTP Request
```
Type: n8n-nodes-base.httpRequest
Method: GET
URL: ={{ $json.url }}
```

### 6. HTML Extract
```
Type: n8n-nodes-base.html
Operation: Extract HTML Content

CSS Selectors:
- price: div[data-cy="cardPropertyOfferPrice"] (array)
- title: div[data-cy="propertyCardTitle"] (array)
- url: a.property-card__link (attribute: href, array)
- area: span[data-cy="cardPropertyInfoArea"] (array)
- rooms: span[data-cy="cardPropertyInfoRooms"] (array)
- floor: span[data-cy="cardPropertyInfoFloor"] (array)
```

### 7. Code in JavaScript
```
Type: n8n-nodes-base.code

JavaScript:
const data = $input.first().json;
const buildUrl = $('Build URL').first().json;

const length = data.url ? data.url.length : 0;

const items = [];
for (let i = 0; i < length; i++) {
  items.push({
    user_id: buildUrl.user_id,
    email: buildUrl.email,
    url: data.url[i],
    price: data.price[i],
    title: data.title[i],
    area: data.area[i],
    rooms: data.rooms[i],
    floor: data.floor[i]
  });
}

return items.map(item => ({ json: item }));
```

**WAZNE:** user_id i email sa pobierane z node'a Build URL przez referencje
`$('Build URL').first().json`, poniewaz HTTP Request zastepuje dane HTMLem.
Dzieki SplitInBatches `.first()` zawsze wskazuje na aktualnie przetwarzanego usera.

### 8. Dodanie gratka.pl
```
Type: n8n-nodes-base.set

Assignments:
- fullink: =https://gratka.pl{{ $json.url }}

Include Other Fields: true
```

### 9. Uzyskanie ID
```
Type: n8n-nodes-base.set

Assignments:
- offerID: ={{ $json.url.split('/').pop() }}

Include Other Fields: true
```

### 10. Execute SQL query (INSERT)
```
Type: n8n-nodes-base.postgres
Operation: Execute Query
Credential: Postgres account (nexuslab_db)

Query:
INSERT INTO gratka_useroffer (
    user_id,
    offer_id,
    url,
    full_link,
    title,
    price,
    area,
    rooms,
    floor,
    date_added,
    date_scraped,
    sent_to_client
) VALUES (
    {{ $json.user_id }},
    '{{ $json.offerID }}',
    '{{ $json.url }}',
    '{{ $json.fullink }}',
    '{{ $json.title }}',
    '{{ $json.price }}',
    '{{ $json.area }}',
    '{{ $json.rooms }}',
    '{{ $json.floor }}',
    NOW(),
    NOW(),
    false
)
ON CONFLICT (user_id, offer_id) DO NOTHING
RETURNING *
```

**WAZNE:** `ON CONFLICT (user_id, offer_id) DO NOTHING` - deduplikacja per user!
**WAZNE:** `RETURNING *` zwraca dane TYLKO dla nowych ofert (duplikaty zwracaja pusty wynik).

### 11. Is new offer?
```
Type: n8n-nodes-base.if

Condition:
- {{ $json.offer_id }} exists (is not empty)

TRUE -> Send Email
FALSE -> Duplicate - skip
```

### 12. Send Email (Gmail)
```
Type: n8n-nodes-base.gmail
Operation: Send Email

Authentication: OAuth2 (Gmail credentials)

To: ={{ $json.email }}
Subject: =Nowa oferta - {{ $json.title }}

Message (HTML):
=<h2>Nowa oferta z Gratka.pl</h2>
<p><strong>Tytul:</strong> {{ $json.title }}</p>
<p><strong>Cena:</strong> {{ $json.price }}</p>
<p><strong>Metraz:</strong> {{ $json.area }}</p>
<p><strong>Pokoje:</strong> {{ $json.rooms }}</p>
<p><strong>Pietro:</strong> {{ $json.floor }}</p>
<p><a href="{{ $json.full_link }}">Zobacz oferte</a></p>
<p><small>ID: {{ $json.offer_id }}</small></p>
```

**Alternatywa - Email Send (SMTP):**
```
Type: n8n-nodes-base.emailSend

SMTP Credentials:
- Host: smtp.gmail.com
- Port: 587
- User: twoj@gmail.com
- Password: [App Password 16-char]
- Secure: true (TLS)

From: NexusLab Alerts <twoj@gmail.com>
To: ={{ $json.email }}
Subject: (jak wyzej)
HTML: (jak wyzej)
```

### 13. Duplicate - skip
```
Type: n8n-nodes-base.noOp

Konczy workflow dla duplikatow.
```

## Multi-User Support

Workflow obsluguje wielu uzytkownikow dzieki **SplitInBatches**:

1. Read Config zwraca N wierszy (N aktywnych userow)
2. SplitInBatches podaje jednego usera naraz do Build URL
3. Caly lancuch (Build URL -> ... -> Send Email) wykonuje sie dla jednego usera
4. Po zakonczeniu SplitInBatches podaje kolejnego usera
5. Powtarza az do przetworzenia wszystkich

### Skalowanie

| Userow | Czas ~1 cykl | Status |
|--------|-------------|--------|
| 1-10 | kilka-kilkanascie sekund | OK |
| 10-50 | 1-3 minuty | OK |
| 50-100 | 3-10 minut | Gratka moze rate-limitowac |
| 100+ | rozwazyc Celery w Django | za duzo na n8n |

Na etapie MVP z kilkoma-kilkunastoma userami SplitInBatches wystarczy.

## Credentials Required

### 1. PostgreSQL
```
Name: Postgres account
Host: localhost
Port: 5432
Database: nexuslab_db
User: nexuslab_user
Password: [from .env]
SSL: disable (localhost)
```

**WAZNE:** Baza to `nexuslab_db` (Django), NIE stara `gratka_db`.

### 2. Gmail OAuth2 (opcja 1)
```
Name: Gmail OAuth2
Client ID: [from Google Cloud Console]
Client Secret: [from Google Cloud Console]
OAuth Redirect URL: [from n8n]
```

**Setup:**
1. Google Cloud Console -> APIs & Services
2. Enable Gmail API
3. Create OAuth 2.0 Client ID
4. Add redirect URI from n8n
5. Connect in n8n credentials

### 3. Gmail SMTP (opcja 2 - PROSTSZE!)
```
Name: SMTP Gmail
Host: smtp.gmail.com
Port: 587
User: twoj@gmail.com
Password: [App Password - 16 chars]
Secure: true
```

**Setup:**
1. Google Account -> Security -> 2FA (enable)
2. App Passwords -> Generate for "n8n"
3. Copy 16-char password
4. Paste in n8n SMTP credentials

## Testing

### Manual Test:
1. n8n -> Open workflow
2. Click "Execute Workflow"
3. Check output of each node
4. Verify email received

### Production Test:
1. Activate workflow (toggle ON)
2. Wait 1 hour OR click "Execute Workflow" manually
3. Check PostgreSQL for new offers:
```sql
SELECT * FROM gratka_useroffer ORDER BY date_added DESC LIMIT 10;
```
4. Check Django dashboard (gratka.nexuslab.pl) - oferty powinny byc widoczne

## Troubleshooting

### Problem: No emails sent
**Check:**
1. Executions -> See workflow run
2. "Is new offer?" -> TRUE or FALSE?
3. If FALSE -> all duplicates (clear DB and test)
4. If TRUE but no email -> check Gmail credentials

### Problem: "Unable to sign without access token"
**Solution:**
- Gmail OAuth2 not configured
- Use SMTP instead (easier!)

### Problem: Wszystkie oferty duplikaty
**Solution:**
```sql
DELETE FROM gratka_useroffer WHERE user_id = 1;
```
Run workflow again - should send emails.

### Problem: Wrong offers for user
**Check:**
- user_id przekazywany poprawnie przez caly lancuch?
- Build URL uzywa odpowiedniej config?
- SplitInBatches ustawiony na batch size 1?

### Problem: relation "gratka_userconfig" does not exist
**Solution:**
Credential PostgreSQL wskazuje na zla baze. Zmien Database z `gratka_db` na `nexuslab_db`.

## Future Improvements

1. **Error handling:**
   - Add Error Trigger node
   - Send admin notification on failure

2. **Metrics:**
   - Count offers scraped
   - Track success/failure rate
   - Store in metrics table

3. **Advanced filtering:**
   - AI scoring (Claude API)
   - Keyword matching
   - Price per m2 calculation

4. **Multiple sources:**
   - Duplicate workflow for OLX
   - Duplicate workflow for Otodom
   - Merge results

## Export/Backup

**Export workflow to JSON:**
1. n8n -> Workflow -> ... menu -> Download
2. Save as `gratka-scraper-workflow.json`
3. Version in Git

**Import:**
1. n8n -> Import from File
2. Select JSON
3. Adjust credentials if needed
