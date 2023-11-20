import random
from django.core.management.base import BaseCommand
from socialnetwork.models import RequestData
from django.utils import timezone
import pytesseract

class Command(BaseCommand):
    help = 'Generate and add requests to the SQLite3 database'

    def handle(self, *args, **options):
        farmer_names = ["Ricky", "Jane", "Bennet", "Jack"]
        product_names = ["tomato", "apple", "banana", "cucumber"]
        expiry_dates = ["2025-01-01", "2026-05-05", "2027-07-07"]
        statuses = ['pending', 'delivered', 'shipped']
        quantities = [1000, 5000, 10000, 4000]
        for _ in range(100):  # Adjust the number of requests as needed
            RequestData.objects.create(
                timestamp=timezone.now(),
                farmer_name = random.choice(farmer_names),
                product_name = random.choice(product_names),
                expiry_date = random.choice(expiry_dates),
                quantity=random.choice(quantities),
                status = random.choice(statuses)
        )
        self.stdout.write(self.style.SUCCESS('Requests added successfully'))


