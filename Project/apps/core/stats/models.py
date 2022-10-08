from apps.core.models import ComingEvent
from apps.core.stats.managers import ComingEventManager


class ComingEventStats(ComingEvent):
    objects = ComingEventManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'ComingEvent Stats'
        verbose_name_plural = 'ComingEvents Stats'
