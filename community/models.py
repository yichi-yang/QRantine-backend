from django.db import models


class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    population = models.PositiveIntegerField()
    cases = models.PositiveIntegerField()
