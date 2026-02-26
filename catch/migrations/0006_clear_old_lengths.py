from django.db import migrations


def clear_bad_lengths(apps, schema_editor):
    # remove any stored length values that contain non-numeric characters
    # this will catch the previous 'short', 'medium', 'long' entries and
    # any other stray strings left over from the old CharField.
    sql = (
        "UPDATE catch_catch "
        "SET length=NULL "
        "WHERE length IS NOT NULL AND length <> '' AND length GLOB '*[^0-9.]*'"
    )
    cursor = schema_editor.connection.cursor()
    cursor.execute(sql)


def noop(apps, schema_editor):
    # nothing to reverse; leave values as-is
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catch', '0005_alter_catch_length'),
    ]

    operations = [
        migrations.RunPython(clear_bad_lengths, noop),
    ]
