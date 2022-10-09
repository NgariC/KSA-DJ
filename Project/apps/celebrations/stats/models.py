from django.utils.translation import gettext_lazy as _

from apps.celebrations.models import Founderee, PatronsDay
from apps.celebrations.stats.managers import FoundereeManager, PatronsDayManager


class FoundereeStats(Founderee):
    objects = FoundereeManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = _('Founderee Stats')
        verbose_name_plural = _('Founderees Stats')


class PatronsDayStats(PatronsDay):
    objects = PatronsDayManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = _('PatronsDay Stats')
        verbose_name_plural = _('PatronsDay Stats')

    def __str__(self):
        return f'{self.date} - {self.year}'
