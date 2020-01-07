import uuid

from django.db import models

# Create your models here.

# class Venue(models.Model):
    # name = models.CharField(max_length=255)
    # address = models.TextField()
    # description = models.TextField()

# class Link(models.Model):
    # name = models.CharField(max_length=255)
    # url = models.URLField(max_length=1024)

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateTimeField()
    # image = models.ImageField()
    # venue = models.ForeignKey(Venue, on_delete=models.PROTECT)

