from django.db import models

class Location(models.Model):
    plus_code = models.CharField(max_length=50)
    name = models.CharField(max_length=100, blank=True, default="")
