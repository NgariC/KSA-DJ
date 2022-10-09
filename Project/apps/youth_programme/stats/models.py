from apps.youth_programme.models import Investiture, BadgeCamp, ParkHoliday, PLC, RM
from apps.youth_programme.stats.managers import InvestitureManager, BadgeCampManager, PLCManager


class InvestitureStats(Investiture):
    objects = InvestitureManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'Investiture Stats'
        verbose_name_plural = 'Investitures Stats'


class BadgeCampStats(BadgeCamp):
    objects = BadgeCampManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'Badge Camp Stats'
        verbose_name_plural = 'Badge Camps Stats'


class ParkHolidayStats(ParkHoliday):
    objects = BadgeCampManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'Park Holiday Stats'
        verbose_name_plural = 'Park Holiday Stats'


class PLCStats(PLC):
    objects = PLCManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'PLC Stats'
        verbose_name_plural = 'PLC Stats'


class RMStats(RM):
    objects = PLCManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'Rover Mate Stats'
        verbose_name_plural = 'Rover Mate Stats'
