from django.contrib import admin
from .models import Catch, Species, Venue, Method, Bait, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'picture')

# Register your models here.

@admin.register(Catch)
class CatchAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'species', 'venue', 'method', 'bait', 'length', 'weight')
    list_filter = ('species', 'venue', 'method', 'bait', 'length', 'user')
    search_fields = ('user__username',)


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Bait)
class BaitAdmin(admin.ModelAdmin):
    search_fields = ('name',)
