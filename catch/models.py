from django.conf import settings
from django.db import models

# choice lists for catch attributes
SPECIES_CHOICES = [
    ('trout', 'Trout'),
    ('salmon', 'Salmon'),
    ('bass', 'Bass'),
    ('pike', 'Pike'),
    # add more species as needed
]

VENUE_CHOICES = [
    ('river', 'River'),
    ('lake', 'Lake'),
    ('sea', 'Sea'),
    ('pond', 'Pond'),
]

METHOD_CHOICES = [
    ('fly', 'Fly fishing'),
    ('spin', 'Spinning'),
    ('bait', 'Bait fishing'),
    ('trolling', 'Trolling'),
]

BAIT_CHOICES = [
    ('worm', 'Worm'),
    ('insect', 'Insect'),
    ('artificial', 'Artificial lure'),
    ('livebait', 'Live bait'),
]

LENGTH_CHOICES = [
    ('short', 'Short (<10 in)'),
    ('medium', 'Medium (10-20 in)'),
    ('long', 'Long (>20 in)'),
]


class Catch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    venue = models.CharField(max_length=50, choices=VENUE_CHOICES)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    bait = models.CharField(max_length=50, choices=BAIT_CHOICES)
    length = models.CharField(max_length=20, choices=LENGTH_CHOICES, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.get_species_display()} on {self.date}"

    class Meta:
        ordering = ['-date']
