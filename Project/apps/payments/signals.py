from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from apps.payments.models import PaymentsList
from apps.registrations.models import Unit, Scout, ScoutLeader
from apps.training.models import ITC, PTC
from apps.youth_programme.models import Investiture, BadgeCamp, ParkHoliday, PLC, RM


@receiver(m2m_changed, sender=PaymentsList.units.through)
def m2m_changed_unit(sender, instance, **kwargs):
    for i in instance.units.all():
        obj = Unit.objects.get(pk=i.pk)
        instance.units_paid_for.add(obj)
        instance.save()


@receiver(m2m_changed, sender=PaymentsList.scouts.through)
def m2m_changed_scout(sender, instance, **kwargs):
    for i in instance.scouts.all():
        obj = Scout.objects.get(pk=i.pk)
        instance.scouts_paid_for.add(obj)
        instance.save()


@receiver(m2m_changed, sender=PaymentsList.scout_leaders.through)
def m2m_changed_scout_leader(sender, instance, **kwargs):
    for i in instance.scout_leaders.all():
        obj = ScoutLeader.objects.get(pk=i.pk)
        instance.scout_leaders_paid_for.add(obj)
        instance.save()


@receiver(m2m_changed, sender=PaymentsList.itcs.through)
def m2m_itc(sender, instance, **kwargs):
    for i in instance.itcs.all():
        obj = ITC.objects.get(pk=i.pk)
        instance.itcs_paid_for.add(obj)
        instance.save()


@receiver(m2m_changed, sender=PaymentsList.ptcs.through)
def m2m_ptc(sender, instance, **kwargs):
    for i in instance.ptcs.all():
        obj = PTC.objects.get(pk=i.pk)
        instance.ptcs_paid_for.add(obj)
        instance.save()


@receiver(m2m_changed, sender=PaymentsList.investitures.through)
def m2m_investiture(sender, instance, **kwargs):
    for i in instance.investitures.all():
        obj = Investiture.objects.get(pk=i.pk)
        instance.investitures_paid_for.add(obj)
        instance.save()


@receiver(m2m_changed, sender=PaymentsList.badge_camps.through)
def m2m_badge_camp(sender, instance, **kwargs):
    for i in instance.badge_camps.all():
        obj = BadgeCamp.objects.get(pk=i.pk)
        instance.badge_camps_paid_for.add(obj)
        instance.save()


@receiver(m2m_changed, sender=PaymentsList.park_holidays.through)
def m2m_park_holiday(sender, instance, **kwargs):
    for i in instance.park_holidays.all():
        obj = ParkHoliday.objects.get(pk=i.pk)
        instance.park_holidays_paid_for.add(obj)
        instance.save()


@receiver(m2m_changed, sender=PaymentsList.plcs.through)
def m2m_plc(sender, instance, **kwargs):
    for i in instance.plcs.all():
        obj = PLC.objects.get(pk=i.pk)
        instance.plcs_paid_for.add(obj)
        instance.save()


@receiver(m2m_changed, sender=PaymentsList.rover_mates.through)
def m2m_rover_mate(sender, instance, **kwargs):
    for i in instance.rover_mates.all():
        obj = RM.objects.get(pk=i.pk)
        instance.rover_mates_paid_for.add(obj)
        instance.save()


@receiver(post_save, sender=PaymentsList.units.through)
def unit_activeness(sender, instance, **kwargs):
    for i in instance.units.all():
        obj = Unit.objects.get(pk=i.pk)
        obj.active = True
        obj.save()