from django.db import models


class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    population = models.PositiveIntegerField(null=True)
    cases = models.PositiveIntegerField()

    def __str__(self):
        return self.name + " #" + str(self.cases)
