# Generated by Django 5.0 on 2023-12-24 10:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="end_time",
            field=models.TimeField(verbose_name="Время окончания брони"),
        ),
        migrations.AlterField(
            model_name="booking",
            name="start_time",
            field=models.TimeField(verbose_name="Время начала брони"),
        ),
    ]
