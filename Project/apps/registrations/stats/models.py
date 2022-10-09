from django.utils.translation import gettext_lazy as _

from apps.registrations.models import Unit, Scout, ScoutLeader
from apps.registrations.stats.managers import UnitManager, ScoutManager, ScoutLeaderManager


class UnitStats(Unit):
    objects = UnitManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = _('Units Stats')
        verbose_name_plural = _('Units Stats')


class ScoutStats(Scout):
    objects = ScoutManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = _('Scouts Stats')
        verbose_name_plural = _('Scouts Stats')


class ScoutLeaderStats(ScoutLeader):
    objects = ScoutLeaderManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = _('Scout Leaders Stats')
        verbose_name_plural = _('Scout Leaders Stats')
