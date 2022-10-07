from django.db import models


class CountryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().only('name')


class RegionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('country').filter(country__name="Kenya").order_by('name')


class CountyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('region').order_by('code')

    def active(self):
        return super().get_queryset().select_related('region').filter(active=True)


class SubCountyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('county').order_by('county')

    def active(self):
        return super().get_queryset().select_related('county').filter(active=True)


class ZoneManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('sub_county').order_by('name')


class RankManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def national(self):
        return super().get_queryset().filter(level='National')

    def regional(self):
        return super().get_queryset().filter(level='Regional')

    def county(self):
        return super().get_queryset().filter(level='County')

    def sub_county(self):
        return super().get_queryset().filter(level='SubCounty')

    def zonal(self):
        return super().get_queryset().filter(level='Zonal')

    def unit(self):
        return super().get_queryset().filter(level='Unit')

    def scouts(self):
        return super().get_queryset().filter(level='Scouts')
