from apps.training.models import ITC, PTC, WBI, WBII, WBIII, ALT, LT, SLSpecialEvent
from apps.training.stats.managers import SLLEventManager, SLEventManager


class ITCStats(ITC):
    objects = SLLEventManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'ITC Stats'
        verbose_name_plural = 'ITCs Stats'


class PTCStats(PTC):
    objects = SLLEventManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'PTC Stats'
        verbose_name_plural = 'PTCs Stats'


class WBIStats(WBI):
    # objects = SLEventManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'WoodBadge I Stats'
        verbose_name_plural = 'WoodBadge I Stats'


class WBIIStats(WBII):
    objects = SLEventManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'WoodBadge II Stats'
        verbose_name_plural = 'WoodBadge II Stats'


class WBIIIStats(WBIII):
    # objects = SLEventManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'WoodBadge III Stats'
        verbose_name_plural = 'WoodBadge III Stats'


class ALTStats(ALT):
    objects = SLEventManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'ALT Stats'
        verbose_name_plural = 'ALTs Stats'


class LTStats(LT):
    objects = SLEventManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'LT Stats'
        verbose_name_plural = 'LTs Stats'


class SLSpecialEventStats(SLSpecialEvent):
    objects = SLEventManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'SL Special Event Stats'
        verbose_name_plural = 'SL Special Events Stats'
