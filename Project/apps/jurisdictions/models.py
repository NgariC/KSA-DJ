from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse

from apps.jurisdictions.managers import CountryManager, RegionManager, CountyManager, SubCountyManager, ZoneManager, \
    RankManager
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    code = models.CharField(_('code'), primary_key=True, max_length=2, db_index=True)
    name = models.CharField(_('name'), max_length=50, unique=True, db_index=True)

    objects = CountryManager()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['code', 'name'], name='unique_country')
        ]
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(_('name'), max_length=50, primary_key=True, db_index=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, db_index=True)

    objects = RegionManager()

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')

    def __str__(self):
        return self.name


class County(models.Model):
    code = models.PositiveSmallIntegerField(_('code'), primary_key=True, db_index=True)
    name = models.CharField(_('name'), max_length=50, unique=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, db_index=True)
    active = models.BooleanField(_('activeness'), default=False, db_index=True)

    objects = CountyManager()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['code', 'name'], name='unique_county')
        ]
        permissions = [('can_verify_county', 'Can verify Counties')]
        verbose_name = _('county')
        verbose_name_plural = _('counties')

    def __str__(self):
        return self.name

    @property
    def reg_amount(self):
        return 1000


class SubCounty(models.Model):
    name = models.CharField(_('name'), primary_key=True, max_length=50)
    county = models.ForeignKey(County, on_delete=models.PROTECT, db_index=True)
    active = models.BooleanField(_('activeness'), default=False, db_index=True)

    objects = SubCountyManager()

    class Meta:
        permissions = [('can_verify_sub_county', 'Can verify SubCounty')]
        verbose_name = _('sub_county')
        verbose_name_plural = _('sub_counties')

    def __str__(self):
        return f'{self.county}/{self.name}'

    @property
    def reg_amount(self):
        return 500


class Zone(models.Model):
    name = models.CharField(_('name'), primary_key=True, max_length=50)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT, db_index=True)

    objects = ZoneManager()

    class Meta:
        verbose_name = _('zone')
        verbose_name_plural = _('zones')

    def __str__(self):
        return f'{self.sub_county}/{self.name}'


class Rank(models.Model):
    RANK_LEVEL = (
        ('National', _('National Level')),
        ('Regional', _('Regional Level')),
        ('County', _('County Level')),
        ('SubCounty', _('SubCounty Level')),
        ('Zonal', _('Zonal Level')),
        ('Unit', _('Unit Level')),
        ('Scouts', _('Scouts Level')),
    )
    code = models.CharField(_('code'), primary_key=True, max_length=20)
    name = models.CharField(_('name'), max_length=100, unique=True)
    level = models.CharField(_('level'), max_length=20, choices=RANK_LEVEL, db_index=True)

    objects = RankManager()

    class Meta:
        unique_together = ['code', 'name']
        ordering = ['level']
        verbose_name = _('rank')
        verbose_name_plural = _('ranks')

    def __str__(self):
        return f'{self.code} - ({self.get_level_display()})'

    def get_absolute_url(self):
        return reverse('ranks:r_detail', kwargs={'pk': self.pk})
