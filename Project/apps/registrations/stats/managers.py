from django.db import models


class UnitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('sub_county',
                                                     'sub_county__county',
                                                     'sub_county__county__region').values(
            'sections',
            'sub_county', 'sub_county__county__name',
            'sub_county__county__region__name')


class ScoutManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('unit',
                                                     'unit__sub_county',
                                                     'unit__sub_county__county',
                                                     'unit__sub_county__county__region').values(
            'section', 'unit', 'gender', 'unit__sub_county',
            'unit__sub_county__county__name',
            'unit__sub_county__county__region__name')


class ScoutLeaderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('sub_county',
                                                     'sub_county__county',
                                                     'sub_county__county__region', 'rank', 'unit').defer(
                                                     'unit__sub_county',
                                                     'unit__sub_county__county',
                                                     'unit__sub_county__county__region').values(
            'gender', 'sub_county', 'sub_county__county__name', 'sub_county__county__region__name')
