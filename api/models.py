from django.db import models

class Country(models.Model):
    common_name = models.CharField(max_length=255)
    official_name = models.CharField(max_length=255)
    native_name_common = models.CharField(max_length=255, blank=True, null=True)
    native_name_official = models.CharField(max_length=255, blank=True, null=True)
    capital = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    area = models.FloatField()
    population = models.IntegerField()
    timezones = models.CharField(max_length=255)
    continents = models.CharField(max_length=255)
    flag_png = models.URLField()
    flag_svg = models.URLField()

    def __str__(self):
        return self.common_name
