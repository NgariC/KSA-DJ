from apps.registrations.models import Unit, Scout, ScoutLeader
from apps.registrations.stats.managers import UnitManager, ScoutManager, ScoutLeaderManager


class UnitStats(Unit):
    history = None
    objects = UnitManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'Units Stats'
        verbose_name_plural = 'Units Stats'


class ScoutStats(Scout):
    history = None
    objects = ScoutManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'Scouts Stats'
        verbose_name_plural = 'Scouts Stats'


class ScoutLeaderStats(ScoutLeader):
    history = None
    objects = ScoutLeaderManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'Scout Leaders Stats'
        verbose_name_plural = 'Scout Leaders Stats'
