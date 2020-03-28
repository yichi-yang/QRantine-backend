from django.db import models
from community.models import Community


class Location(models.Model):
    plus_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    thumbnail = models.URLField(blank=True)
    community = models.ForeignKey(Community, models.PROTECT,
                                  "locations", null=True)
