# 🗄️ Database Schema

## Overview

Database: `nexuslab_db`
User: `nexuslab_user`
Host: `localhost:5432`

## Tables

### 1. auth_user (Django default)

Django's built-in User model.

```sql
CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254) UNIQUE NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP NOT NULL
);
```

**Indexes:**
- PRIMARY KEY (id)
- UNIQUE (username)
- UNIQUE (email)

### 2. gratka_userconfig

Personalizowane kryteria wyszukiwania dla każdego użytkownika.

```sql
CREATE TABLE gratka_userconfig (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    lokalizacja VARCHAR(100) DEFAULT 'lodz',
    cena_min INTEGER DEFAULT 100000,
    cena_max INTEGER DEFAULT 250000,
    metraz_min INTEGER,
    metraz_max INTEGER,
    balkon BOOLEAN DEFAULT TRUE,
    garaz BOOLEAN DEFAULT TRUE,
    piwnica BOOLEAN DEFAULT FALSE,
    email VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT unique_user_config UNIQUE(user_id)
);

CREATE INDEX idx_gratka_userconfig_user ON gratka_userconfig(user_id);
CREATE INDEX idx_gratka_userconfig_active ON gratka_userconfig(is_active) WHERE is_active = TRUE;
```

**Django Model:**
```python
from django.db import models
from django.contrib.auth.models import User

class UserConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lokalizacja = models.CharField(max_length=100, default='lodz')
    cena_min = models.IntegerField(default=100000)
    cena_max = models.IntegerField(default=250000)
    metraz_min = models.IntegerField(null=True, blank=True)
    metraz_max = models.IntegerField(null=True, blank=True)
    balkon = models.BooleanField(default=True)
    garaz = models.BooleanField(default=True)
    piwnica = models.BooleanField(default=False)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gratka_userconfig'
        verbose_name = 'User Config'
        verbose_name_plural = 'User Configs'
```

### 3. gratka_useroffer

Zapisane oferty dla każdego użytkownika.

```sql
CREATE TABLE gratka_useroffer (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    offer_id VARCHAR(50) NOT NULL,
    url TEXT NOT NULL,
    full_link TEXT NOT NULL,
    title TEXT NOT NULL,
    price VARCHAR(100),
    area VARCHAR(50),
    rooms VARCHAR(50),
    floor VARCHAR(50),
    date_added TIMESTAMP DEFAULT NOW(),
    date_scraped TIMESTAMP DEFAULT NOW(),
    sent_to_client BOOLEAN DEFAULT FALSE,
    
    CONSTRAINT unique_user_offer UNIQUE(user_id, offer_id)
);

CREATE INDEX idx_gratka_useroffer_user ON gratka_useroffer(user_id);
CREATE INDEX idx_gratka_useroffer_date ON gratka_useroffer(date_added DESC);
CREATE INDEX idx_gratka_useroffer_sent ON gratka_useroffer(sent_to_client) WHERE sent_to_client = FALSE;
CREATE INDEX idx_gratka_useroffer_composite ON gratka_useroffer(user_id, date_added DESC);
```

**Django Model:**
```python
class UserOffer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    offer_id = models.CharField(max_length=50)
    url = models.TextField()
    full_link = models.TextField()
    title = models.TextField()
    price = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=50, blank=True)
    rooms = models.CharField(max_length=50, blank=True)
    floor = models.CharField(max_length=50, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_scraped = models.DateTimeField(auto_now_add=True)
    sent_to_client = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'gratka_useroffer'
        verbose_name = 'User Offer'
        verbose_name_plural = 'User Offers'
        unique_together = ['user', 'offer_id']
        ordering = ['-date_added']
```

### 4. subscriptions_plan (przyszłość)

Plany subskrypcyjne.

```sql
CREATE TABLE subscriptions_plan (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    price_monthly DECIMAL(10, 2) NOT NULL,
    price_yearly DECIMAL(10, 2),
    features JSONB,
    max_locations INTEGER,
    max_sources INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO subscriptions_plan (name, slug, price_monthly, features, max_locations, max_sources) VALUES
('Basic', 'basic', 49.00, '{"email_alerts": true, "sms_alerts": false}', 1, 1),
('Pro', 'pro', 99.00, '{"email_alerts": true, "sms_alerts": true, "ai_scoring": true}', 3, 3),
('Business', 'business', 199.00, '{"email_alerts": true, "sms_alerts": true, "ai_scoring": true, "api_access": true}', 10, 5);
```

### 5. subscriptions_usersubscription (przyszłość)

Subskrypcje użytkowników.

```sql
CREATE TABLE subscriptions_usersubscription (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    plan_id INTEGER NOT NULL REFERENCES subscriptions_plan(id),
    status VARCHAR(20) DEFAULT 'active', -- active, canceled, expired
    stripe_subscription_id VARCHAR(100),
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT unique_active_subscription UNIQUE(user_id) WHERE status = 'active'
);

CREATE INDEX idx_subscription_user ON subscriptions_usersubscription(user_id);
CREATE INDEX idx_subscription_status ON subscriptions_usersubscription(status);
```

### 6. chatbot_conversation (przyszłość)

Historia konwersacji z chatbotem.

```sql
CREATE TABLE chatbot_conversation (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    user_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
    message JSONB NOT NULL, -- {role: "user/assistant", content: "..."}
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chatbot_session ON chatbot_conversation(session_id);
CREATE INDEX idx_chatbot_user ON chatbot_conversation(user_id);
CREATE INDEX idx_chatbot_date ON chatbot_conversation(created_at DESC);
```

## SQL Initialization Script

**`init_db.sql`:**

```sql
-- Create database
CREATE DATABASE nexuslab_db;

-- Create user
CREATE USER nexuslab_user WITH PASSWORD 'STRONG_PASSWORD_HERE';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE nexuslab_db TO nexuslab_user;

-- Connect to database
\c nexuslab_db

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO nexuslab_user;

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For text search

-- Django will create tables via migrations
-- But you can manually create tables if needed using the CREATE TABLE statements above
```

## Queries używane przez n8n

### 1. Odczytaj wszystkie aktywne konfiguracje:

```sql
SELECT 
    u.id as user_id,
    u.email as user_email,
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

### 2. Zapisz nową ofertę (deduplikacja):

```sql
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
    date_scraped
) VALUES (
    :user_id,
    :offer_id,
    :url,
    :full_link,
    :title,
    :price,
    :area,
    :rooms,
    :floor,
    NOW(),
    NOW()
)
ON CONFLICT (user_id, offer_id) DO NOTHING
RETURNING *;
```

### 3. Oznacz ofertę jako wysłaną:

```sql
UPDATE gratka_useroffer 
SET sent_to_client = TRUE
WHERE id = :offer_id;
```

### 4. Statystyki użytkownika:

```sql
SELECT 
    COUNT(*) as total_offers,
    COUNT(*) FILTER (WHERE sent_to_client = TRUE) as sent_offers,
    COUNT(*) FILTER (WHERE date_added > NOW() - INTERVAL '7 days') as offers_last_week,
    MIN(date_added) as first_offer_date,
    MAX(date_added) as last_offer_date
FROM gratka_useroffer
WHERE user_id = :user_id;
```

## Backup & Restore

### Backup:

```bash
pg_dump -U nexuslab_user -h localhost nexuslab_db > backup_$(date +%Y%m%d).sql
```

### Restore:

```bash
psql -U nexuslab_user -h localhost nexuslab_db < backup_20250103.sql
```

### Automated Daily Backup (cron):

```bash
# /etc/cron.daily/postgres-backup
#!/bin/bash
BACKUP_DIR="/var/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U nexuslab_user nexuslab_db | gzip > $BACKUP_DIR/nexuslab_$DATE.sql.gz
# Keep only last 7 days
find $BACKUP_DIR -name "nexuslab_*.sql.gz" -mtime +7 -delete
```

## Performance Tips

1. **Vacuum regularly:**
```sql
VACUUM ANALYZE gratka_useroffer;
```

2. **Monitor slow queries:**
```sql
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

3. **Connection pooling:**
Use PgBouncer if needed (not necessary at MVP stage).

4. **Partitioning (future):**
Partition `gratka_useroffer` by date_added when table grows > 1M rows.
