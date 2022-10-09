from django.db import models


class TeamManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'unit',
            'unit__sub_county',
            'unit__sub_county__county',
            'unit__sub_county__county__region').values('unit', 'gender', 'unit__sub_county',
                                                       'unit__sub_county__county__name',
                                                       'unit__sub_county__county__region__name', 'leaders',
                                                       'competitors')


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'chief')


class CompetitionManager(EventManager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'sub_county').defer('sub_county__county__region__country')
