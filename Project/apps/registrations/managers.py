from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat


class UnitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('sub_county',
                                                     'sub_county__county',
                                                     'sub_county__county__region').order_by('name')

    def active(self):
        return super().get_queryset().select_related('sub_county',
                                                     'sub_county__county',
                                                     'sub_county__county__region').filter(
            active=True).order_by('name')


class ScoutManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('unit', 'unit__sub_county', 'unit__sub_county__county',
                                                     'unit__sub_county__county__region').defer(
            'unit__id',
            'unit__sponsoring_authority',
            'unit__sections',
            'unit__date_warranted',
            'unit__active',
            'unit__sub_county',
            'unit__sub_county__county',
            'unit__sub_county__county__region',
            'unit__sub_county__county__region__country')
        # .annotate(
        # full_name=Concat('first_name', Value(' '),
        #                  'middle_name', Value(' '),
        #                  'surname')).order_by('full_name')

    def active(self):
        return super().get_queryset().select_related('unit', 'unit__sub_county', 'unit__sub_county__county',
                                                     'unit__sub_county__county__region')
        # .annotate(
        # full_name=Concat('first_name', Value(' '),
        #                  'middle_name', Value(' '),
        #                  'surname')).filter(active=True).order_by('full_name')


class ScoutLeaderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('sub_county',
                                                     'sub_county__county',
                                                     'sub_county__county__region', 'rank', 'unit').defer(
            'sub_county__county__code',
            'sub_county__county__region__country',
            'rank__level',
            'rank__name',
            'unit__id',
            'unit__sponsoring_authority',
            'unit__sections',
            'unit__date_warranted',
            'unit__active',
            'unit__sub_county',
            'unit__sub_county__county',
            'unit__sub_county__county__region',
            'unit__sub_county__county__region__country')
        # .annotate(
        # full_name=Concat('first_name', Value(' '),
        #                  'middle_name', Value(' '),
        #                  'surname'), ).order_by('full_name')

    def active(self):
        return super().get_queryset().select_related('sub_county', 'sub_county__county', 'sub_county__county__region',
                                                     'rank', 'unit')
        # .annotate(
        # full_name=Concat('first_name', Value(' '),
        #                  'middle_name', Value(' '),
        #                  'surname')).filter(active=True).order_by('full_name')
