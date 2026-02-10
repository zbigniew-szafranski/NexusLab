#!/bin/bash
# ============================================
# NexusLab - Skrypt deploymentu
# Uzycie: ./deploy.sh
# ============================================

set -e

PROJECT_DIR="/var/www/nexuslab"
VENV="$PROJECT_DIR/venv/bin"

echo "=========================================="
echo "  NexusLab - Deploy"
echo "=========================================="

cd "$PROJECT_DIR"

# 1. Pobierz najnowszy kod
echo "[1/6] Pobieranie zmian z repozytorium..."
git pull origin master

# 2. Instalacja zaleznosci
echo "[2/6] Instalacja zaleznosci Python..."
$VENV/pip install -r requirements.txt --quiet

# 3. Migracje bazy danych
echo "[3/6] Migracje bazy danych..."
$VENV/python manage.py migrate --noinput

# 4. Pliki statyczne
echo "[4/6] Zbieranie plikow statycznych..."
$VENV/python manage.py collectstatic --noinput --clear

# 5. Restart serwisow
echo "[5/6] Restart serwisow..."
sudo supervisorctl restart gunicorn
sudo supervisorctl restart celery-worker
sudo supervisorctl restart celery-beat

# 6. Sprawdzenie statusu
echo "[6/6] Status serwisow:"
sudo supervisorctl status

echo ""
echo "=========================================="
echo "  Deploy zakonczony pomyslnie!"
echo "=========================================="
