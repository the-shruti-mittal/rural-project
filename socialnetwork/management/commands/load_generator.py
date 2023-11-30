import random
from django.core.management.base import BaseCommand
from socialnetwork.models import RequestData, Order, InventoryItem
from django.utils import timezone
import pytesseract

class Command(BaseCommand):
    help = 'Generate and add requests to the SQLite3 database'

    def handle(self, *args, **options):
        farmer_names = ["Ricky", "Jane", "Bennet", "Jack", "Rachana"]
        product_names = ["tomato", "apple", "banana", "cucumber"]
        expiry_dates = ["2025-01-01", "2026-05-05", "2027-07-07"]
        statuses = ['pending', 'delivered', 'shipped']
        quantities = [1000, 5000, 10000, 4000]

        # Create inventory items
        for product_name in product_names:
            existing_item = InventoryItem.objects.filter(product_name=product_name).first()

            if existing_item:
                # Update quantity and timestamp for existing item
                existing_item.quantity += random.choice(quantities)
                existing_item.timestamp = timezone.now()
                existing_item.save()
            else:
                # Create a new inventory item
                InventoryItem.objects.create(
                    product_name=product_name,
                    quantity=random.choice(quantities),
                    expiry_date=random.choice(expiry_dates),
                    availability=True,
                    farmer_name=random.choice(farmer_names),
                    timestamp=timezone.now()
                )

        # Generate orders based on available inventory
'''         for _ in range(10):  # Adjust the number of requests as needed
            product_name = random.choice(product_names)
            inventory_item = InventoryItem.objects.get(product_name=product_name)
            

            if inventory_item.quantity_available > 0:
                Order.objects.create(
                    timestamp=timezone.now(),
                    farmer_name=random.choice(farmer_names),
                    product_name=product_name,
                    quantity=random.choice(quantities),
                    status=random.choice(statuses),
                    inventory_item=inventory_item,
                )
                # Decrease the quantity in the inventory
                inventory_item.quantity_available -= 1
                inventory_item.save() self.stdout.write(self.style.SUCCESS('Requests added successfully'))'''

