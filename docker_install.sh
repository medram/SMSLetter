#!/bin/sh

set -e

cd /app

# Applying migrations
python3 manage.py migrate

echo "Applying seeds..."
python3 manage.py loaddata app/dumps/extra_settings.json
python3 manage.py loaddata app/dumps/subscription.json

echo "Handling assets/static files..."
python3 manage.py collectstatic --no-input --skip-checks

echo "Installation completed successfully."
# container restart is required!
