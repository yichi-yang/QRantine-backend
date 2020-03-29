from django.db import models
from django.contrib.auth.models import AbstractUser
from location.models import Location


class User(AbstractUser):
    pass


class Record(models.Model):
    user = models.ForeignKey(User, models.CASCADE, "records")
    location = models.ForeignKey(Location, models.PROTECT, "records")
    visited_at = models.DateTimeField(auto_now_add=True)
    community_cases = models.PositiveIntegerField(null=True)

