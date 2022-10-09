from apps.celebrations.models import Founderee, PatronsDay
from apps.celebrations.stats.managers import FoundereeManager, PatronsDayManager


class FoundereeStats(Founderee):
    objects = FoundereeManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'Founderee Stats'
        verbose_name_plural = 'Founderees Stats'


class PatronsDayStats(PatronsDay):
    objects = PatronsDayManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'PatronsDay Stats'
        verbose_name_plural = 'PatronsDay Stats'

    def __str__(self):
        return f'{self.date} - {self.year}'
