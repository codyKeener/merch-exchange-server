from django.db import migrations

def remove_price_currency(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("ALTER TABLE merchexchangeapi_listing DROP COLUMN price_currency;")

class Migration(migrations.Migration):

    dependencies = [
        ('merchexchangeapi', '0001_initial'),  # Update this with the correct app name and previous migration name
    ]

    operations = [
        migrations.RunPython(remove_price_currency),
    ]
