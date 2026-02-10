# 🤖 n8n Workflow - Gratka Scraper

## Status: ✅ DZIAŁAJĄCY na n8n.nexuslab.pl

## Overview

Workflow scrapuje Gratka.pl co godzinę, wykrywa nowe oferty i wysyła emaile.

## Workflow Structure

```
Schedule Trigger (co 1h)
    ↓
Read Config (PostgreSQL) - odczytaj konfiguracje wszystkich userów
    ↓
Build URL (Code) - generuj URL dla każdego usera
    ↓
HTTP Request - pobierz HTML z Gratka.pl
    ↓
HTML Extract - wyciągnij dane (price, title, area, rooms, floor, url)
    ↓
Code in JavaScript - transform arrays → individual items
    ↓
Dodanie gratka.pl (Set) - dodaj pełny link
    ↓
Uzyskanie ID (Set) - extract offer_id z URL
    ↓
Execute SQL query - INSERT ... ON CONFLICT DO NOTHING RETURNING *
    ↓
Is new offer? (IF) - czy SQL zwrócił dane?
    ├─ TRUE → Send Email (Gmail)
    └─ FALSE → Duplicate - skip (NoOp)
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
    uc.piwnica,
    uc.email as notification_email
FROM gratka_userconfig uc
JOIN auth_user u ON uc.user_id = u.id
WHERE uc.is_active = TRUE
  AND u.is_active = TRUE;
```

Output: Array of user configs

### 3. Build URL
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

console.log('Generated URL:', url);

return {
  json: {
    url: url,
    user_id: config.user_id,
    notification_email: config.notification_email
  }
};
```

### 4. HTTP Request
```
Type: n8n-nodes-base.httpRequest
Method: GET
URL: ={{ $json.url }}
```

### 5. HTML Extract
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

### 6. Code in JavaScript
```
Type: n8n-nodes-base.code

JavaScript:
const data = $input.first().json;
const user_id = $('Build URL').first().json.user_id;

const length = data.url ? data.url.length : 0;

const items = [];
for (let i = 0; i < length; i++) {
  items.push({
    user_id: user_id,
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

### 7. Dodanie gratka.pl
```
Type: n8n-nodes-base.set

Assignments:
- fullink: =https://gratka.pl{{ $json.url }}

Include Other Fields: true
```

### 8. Uzyskanie ID
```
Type: n8n-nodes-base.set

Assignments:
- offerID: ={{ $json.url.split('/').pop() }}

Include Other Fields: true
```

### 9. Execute SQL query
```
Type: n8n-nodes-base.postgres
Operation: Execute Query

Query:
=INSERT INTO gratka_useroffer (
    user_id,
    offer_id,
    url,
    full_link,
    title,
    price,
    area,
    rooms,
    floor
) VALUES (
    {{ $json.user_id }},
    '{{ $json.offerID }}',
    '{{ $json.url }}',
    '{{ $json.fullink }}',
    '{{ $json.title }}',
    '{{ $json.price }}',
    '{{ $json.area }}',
    '{{ $json.rooms }}',
    '{{ $json.floor }}'
)
ON CONFLICT (user_id, offer_id) DO NOTHING
RETURNING *
```

**WAŻNE:** `ON CONFLICT DO NOTHING` zapobiega duplikatom!
**WAŻNE:** `RETURNING *` zwraca dane TYLKO dla nowych ofert!

### 10. Is new offer?
```
Type: n8n-nodes-base.if

Condition:
- {{ $json.offer_id }} exists (is not empty)

TRUE → Send Email
FALSE → Duplicate - skip
```

### 11. Send Email (Gmail)
```
Type: n8n-nodes-base.gmail
Operation: Send Email

Authentication: OAuth2 (Gmail credentials)

To: ={{ $('Build URL').first().json.notification_email }}
Subject: =🏠 Nowa oferta - {{ $json.title }}

Message (HTML):
=<h2>🏠 Nowa oferta z Gratka.pl</h2>
<p><strong>Tytuł:</strong> {{ $json.title }}</p>
<p><strong>💰 Cena:</strong> {{ $json.price }}</p>
<p><strong>📏 Metraż:</strong> {{ $json.area }}</p>
<p><strong>🚪 Pokoje:</strong> {{ $json.rooms }}</p>
<p><strong>🏢 Piętro:</strong> {{ $json.floor }}</p>
<p><a href="{{ $json.full_link }}">Zobacz ofertę</a></p>
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
To: ={{ $('Build URL').first().json.notification_email }}
Subject: (same as above)
HTML: (same as above)
```

### 12. Duplicate - skip
```
Type: n8n-nodes-base.noOp

Just ends the workflow for duplicates.
```

## Multi-User Support

**n8n automatycznie iteruje przez wszystkie wyniki z "Read Config"!**

Jeśli masz 3 userów:
1. Read Config zwraca 3 rows
2. n8n wykonuje cały workflow 3 razy (raz dla każdego usera)
3. Każdy user dostaje swoje oferty

**Nie potrzeba pętli - n8n robi to automatycznie!**

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

### 2. Gmail OAuth2 (opcja 1)
```
Name: Gmail OAuth2
Client ID: [from Google Cloud Console]
Client Secret: [from Google Cloud Console]
OAuth Redirect URL: [from n8n]
```

**Setup:**
1. Google Cloud Console → APIs & Services
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
1. Google Account → Security → 2FA (enable)
2. App Passwords → Generate for "n8n"
3. Copy 16-char password
4. Paste in n8n SMTP credentials

## Testing

### Manual Test:
1. n8n → Open workflow
2. Click "Execute Workflow"
3. Check output of each node
4. Verify email received

### Production Test:
1. Activate workflow (toggle ON)
2. Wait 1 hour OR
3. Click "Execute Workflow" manually
4. Check PostgreSQL for new offers:
```sql
SELECT * FROM gratka_useroffer ORDER BY date_added DESC LIMIT 10;
```

## Troubleshooting

### Problem: No emails sent
**Check:**
1. Executions → See workflow run
2. "Is new offer?" → TRUE or FALSE?
3. If FALSE → all duplicates (clear DB and test)
4. If TRUE but no email → check Gmail credentials

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
- user_id przekazywany poprawnie?
- Build URL używa odpowiedniej config?

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
   - Price per m² calculation

4. **Multiple sources:**
   - Duplicate workflow for OLX
   - Duplicate workflow for Otodom
   - Merge results

## Export/Backup

**Export workflow to JSON:**
1. n8n → Workflow → ... menu → Download
2. Save as `gratka-scraper-workflow.json`
3. Version in Git

**Import:**
1. n8n → Import from File
2. Select JSON
3. Adjust credentials if needed
