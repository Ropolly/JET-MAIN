# Data migration to change cancelled quotes to lost
from django.db import migrations

def migrate_cancelled_to_lost(apps, schema_editor):
    Quote = apps.get_model('api', 'Quote')
    # Update all quotes with status 'cancelled' to 'lost'
    Quote.objects.filter(status='cancelled').update(status='lost')

def reverse_migration(apps, schema_editor):
    Quote = apps.get_model('api', 'Quote')
    # Reverse: change 'lost' back to 'cancelled' (if needed for rollback)
    Quote.objects.filter(status='lost').update(status='cancelled')

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_quote_status_lostreason_quote_lost_reason'),
    ]

    operations = [
        migrations.RunPython(migrate_cancelled_to_lost, reverse_migration),
    ]