from django.core.management.base import BaseCommand
from socialnetwork.models import Order
from socialnetwork.models import RequestData


class Command(BaseCommand):
    help = 'Update order statuses'

    def handle(self, *args, **options):
        # Your logic to update order statuses goes here
        orders_to_update = RequestData.objects.filter(status='pending')

        for order in orders_to_update:
            # Update the order status as needed
            order.status = 'shipped'
            order.save()

        self.stdout.write(self.style.SUCCESS('Order statuses updated successfully'))