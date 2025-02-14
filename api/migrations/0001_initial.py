# Generated by Django 5.1.6 on 2025-02-05 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_common', models.CharField(max_length=255)),
                ('name_official', models.CharField(max_length=255)),
                ('name_native', models.JSONField()),
                ('capital', models.JSONField()),
                ('latlng', models.JSONField()),
                ('area', models.FloatField()),
                ('population', models.IntegerField()),
                ('timezones', models.JSONField()),
                ('continents', models.JSONField()),
                ('flags_png', models.URLField()),
                ('flags_svg', models.URLField()),
                ('flags_alt', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
