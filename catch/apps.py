from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CatchConfig(AppConfig):
    name = 'catch'

    def ready(self):
        # after migrations run, ensure the lookup tables contain the
        # default values from the original choice lists.
        post_migrate.connect(populate_lookups, sender=self)
        import catch.signals


def populate_lookups(sender, **kwargs):
    # import inside function to avoid circular imports
    from django.db import connection
    from .models import Species, Venue, Method, Bait

    # if migrations haven't yet created the lookup tables we just bail out
    if 'catch_species' not in connection.introspection.table_names():
        return

    defaults = {
        'species': ['Trout', 'Salmon', 'Bass', 'Pike'],
        'venue': ['River', 'Lake', 'Sea', 'Pond'],
        'method': ['Fly fishing', 'Spinning', 'Bait fishing', 'Trolling'],
        'bait': ['Worm', 'Insect', 'Artificial lure', 'Live bait'],
    }

    # for each model, bulk create missing names
    for model_name, names in defaults.items():
        model = {'species': Species, 'venue': Venue, 'method': Method, 'bait': Bait}[model_name]
        for name in names:
            model.objects.get_or_create(name=name)
