from django.contrib import admin
from .models import Catch

# Register your models here.

@admin.register(Catch)
class CatchAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'species', 'venue', 'method', 'bait', 'length', 'weight')
    list_filter = ('species', 'venue', 'method', 'bait', 'length', 'user')
    search_fields = ('user__username',)
