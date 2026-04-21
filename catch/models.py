# Patch User model to always return a Profile, creating one if needed
from django.contrib.auth.models import User
def get_or_create_profile(self):
    profile, created = Profile.objects.get_or_create(user=self)
    return profile
User.add_to_class('profile', property(get_or_create_profile))
from django.db import models
from django.contrib.auth.models import User

# User profile extension for profile picture
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
from django.conf import settings
from django.db import models
from decimal import InvalidOperation


class TolerantDecimalField(models.DecimalField):
    """DecimalField that safely converts non-numeric database values.

    During the migration from a CharField to DecimalField some existing rows
    may still contain values like 'short' or 'medium'.  SQLite's normal
    converter raises a ``TypeError`` when it encounters those strings which
    bubbles up as the "argument must be int or float" exception.  This field
    swallows that error and returns ``None`` instead, allowing the ORM to
    continue working and the form to render without crashing.
    """

    def from_db_value(self, value, expression, connection):
        # value is the raw value returned by the database driver
        if value is None:
            return None
        try:
            # DecimalField doesn't implement its own from_db_value, so
            # fall back to converting via ``to_python`` which performs
            # the normal decimal parsing.  If the stored value can't be
            # interpreted we'll catch the error and return ``None``.
            return self.to_python(value)
        except (TypeError, InvalidOperation, ValueError):
            # non-numeric value stored previously, treat as missing
            return None


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


# length_choices kept for reference but no longer used in the model
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
    length = TolerantDecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    picture = models.ImageField(upload_to='catch_pics/', blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        # species is a foreign key now
        return f"{self.species.name} on {self.date}"

    class Meta:
        ordering = ['-date']
