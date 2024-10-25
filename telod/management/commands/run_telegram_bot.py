from django.core.management.base import BaseCommand
from telod.bot import run_bot  # Import the bot function


class Command(BaseCommand):
    help = "Run the Telegram bot"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting the Telegram bot...")
        run_bot()
