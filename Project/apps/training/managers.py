from django.db import models
from django.db.models import Count


class SLLEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('course_director', 'director', 'sub_county').prefetch_related(
            'support_staff', 'staff', 'participants', 'trainees').annotate(
            _participants_count=Count("trainees__id", distinct=True))

    def paid(self):
        return super().get_queryset().select_related('course_director', 'director', 'sub_county').prefetch_related(
            'support_staff', 'staff', 'participants', 'trainees').filter(payments=True)


class SLEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'course_director',
            'director',
            'county').prefetch_related('support_staff',
                                       'staff',
                                       'participants',
                                       'trainees').annotate(
            _participants_count=Count("trainees__id", distinct=True))

    def paid(self):
        return super().get_queryset().select_related('course_director', 'director', 'county').prefetch_related(
            'support_staff', 'staff', 'participants', 'trainees').filter(payments=True)


class WBIManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('marker', 'marker_name', 'scout_leader', 'scout_leader_name')


class WBIIIManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('unit', 'assessor', 'assessor_name', 'scout_leader',
                                                     'scout_leader_name')

    def paid(self):
        return super().get_queryset().select_related('unit', 'assessor', 'assessor_name', 'scout_leader',
                                                     'scout_leader_name').filter(payments=True)
