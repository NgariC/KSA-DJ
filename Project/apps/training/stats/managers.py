from django.db import models


class SLLEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'course_director',
            'sub_county',
            'sub_county__county',
            'sub_county__county__region').defer(
            'sub_county__county__region__country')


class SLEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'course_director',
            'county',
            'county__region').defer(
            'county__region__country')


class WBIManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('marker', 'marker_name', 'scout_leader', 'scout_leader_name')


class WBIIIManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('unit', 'assessor', 'assessor_name', 'scout_leader',
                                                     'scout_leader_name')
