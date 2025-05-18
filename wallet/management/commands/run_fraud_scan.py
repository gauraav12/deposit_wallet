from django.core.management.base import BaseCommand
from wallet.models import Transaction
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Run daily fraud scan and list flagged transactions'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        recent_flags = Transaction.objects.filter(
            timestamp__gte=now - timedelta(days=1),
            is_flagged=True
        )
        self.stdout.write(self.style.SUCCESS(
            f"Fraud scan complete. {recent_flags.count()} suspicious transactions found."
        ))
