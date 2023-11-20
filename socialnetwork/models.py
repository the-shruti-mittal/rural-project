from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#post model
class Post(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    text = models.CharField(max_length = 160)
    date_time = models.DateTimeField()

    def __unicode__(self):
        return 'id = ' + str(self.id) + 'post=' + str(self.text)


class RequestData(models.Model):
    timestamp = models.DateTimeField()
    farmer_name = models.CharField(max_length = 160)
    product_name = models.CharField(max_length = 160)
    expiry_date  = models.DateField()
    quantity = models.IntegerField()
    status = models.CharField(max_length = 160, default="pending")

    def __unicode__(self):
        return 'id = ' + str(self.id) + 'post=' + str(self.product_name)
    
class Order(models.Model):
    timestamp = models.DateTimeField()
    farmer_name = models.CharField(max_length = 160)
    product_name = models.CharField(max_length = 160)
    expiry_date  = models.DateField()
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






