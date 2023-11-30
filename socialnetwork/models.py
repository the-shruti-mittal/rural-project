from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime




#availability (bool to 0 when quantity becomes 0)
#customer requests pictures

# Create your models here.
#post model
class InventoryItem(models.Model):
    product_name = models.CharField(max_length=255)
    farmer_name = models.CharField(max_length=255, default='Rachana')
    quantity = models.PositiveIntegerField(default=0)
    expiry_date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)
    availability = models.BooleanField(default = True)


class Order(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    farmer_name = models.CharField(max_length=255, default='Rachana')
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    expiry_date  = models.DateField(default=0)
    status = models.CharField(max_length=255, choices=[('pending', 'Pending'), ('delivered', 'Delivered'), ('shipped', 'Shipped')])
    # Add a foreign key to link each order to an InventoryItem
    inventory_item = models.ForeignKey(InventoryItem, default=None, on_delete=models.CASCADE)
    def __unicode__(self):
        return 'id = ' + str(self.id) + 'post=' + str(self.product_name)

class Post(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    text = models.CharField(max_length = 160)
    expiry_date = models.DateTimeField('expiration time (of ad)', default=timezone.now() + datetime.timedelta(days=30))

    def __unicode__(self):
        return 'id = ' + str(self.id) + 'post=' + str(self.text)


class RequestData(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    farmer_name = models.CharField(max_length = 160)
    product_name = models.CharField(max_length = 160)
    expiry_date  = models.DateTimeField('expiration time (of ad)', default=timezone.now() + datetime.timedelta(days=30))
    quantity = models.IntegerField()
    status = models.CharField(max_length = 160, default="pending")

    def __unicode__(self):
        return 'id = ' + str(self.id) + 'post=' + str(self.product_name)
    

class Comment(models.Model):
    text = models.CharField(max_length = 160)
    creation_time = models.DateTimeField()
    creator = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, default=None, on_delete=models.PROTECT)
class Profile(models.Model):
    bio = models.CharField(max_length = 200)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    following = models.ManyToManyField(User, related_name="followers")
    def __str__(self):
        return 'picture=' + str(self.picture) + ',bio="' + self.bio + '"'






