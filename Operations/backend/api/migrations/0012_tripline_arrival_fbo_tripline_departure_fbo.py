# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_airport_id_tripevent_airport_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripline',
            name='departure_fbo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departure_trip_lines', to='api.fbo'),
        ),
        migrations.AddField(
            model_name='tripline',
            name='arrival_fbo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arrival_trip_lines', to='api.fbo'),
        ),
    ]