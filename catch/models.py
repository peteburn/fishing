from django.conf import settings
from django.db import models


# These tables back the dropdowns used by catches.  They allow the
# options to be managed via the admin site (or any other UI) and also
# make it possible to add new values without editing Python code.
class Species(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Method(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Bait(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# length choices remain in code since they are unlikely to change often
LENGTH_CHOICES = [
    ('short', 'Short (<10 in)'),
    ('medium', 'Medium (10-20 in)'),
    ('long', 'Long (>20 in)'),
]


class Catch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    method = models.ForeignKey(Method, on_delete=models.PROTECT)
    bait = models.ForeignKey(Bait, on_delete=models.PROTECT)
    length = models.CharField(max_length=20, choices=LENGTH_CHOICES, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        # species is a foreign key now
        return f"{self.species.name} on {self.date}"

    class Meta:
        ordering = ['-date']
