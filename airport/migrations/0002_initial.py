# Generated by Django 4.2.6 on 2023-10-20 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("airport", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="airplane",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="flights",
                to="airport.airplane",
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="crew",
            field=models.ManyToManyField(
                related_name="flights", to="airport.crew"
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="route",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="flights",
                to="airport.route",
            ),
        ),
        migrations.AddField(
            model_name="airplane",
            name="airplane_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="airplanes",
                to="airport.airplanetype",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("flight", "row", "seat")},
        ),
    ]
