#!/bin/sh

# Start the Django development server in the background
poetry run python manage.py runserver 0.0.0.0:8000 &

# Start the Telegram bot
poetry run python manage.py run_telegram_bot
