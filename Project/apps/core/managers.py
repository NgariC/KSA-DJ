from datetime import datetime

from django.db.models import Q
from django.db import models


class ScoutCenterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('sub_county')


class ComingEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'county').defer(
            'requirement',
            'county__region',
            'county__region__country',
            'event_coordinators'
        )

    def featured(self):
        return super().get_queryset().select_related(
            'county').filter(
            Q(start_date__gte=datetime.now().date()) &
            Q(is_published=True) & Q(is_featured=True)).values(
            'id',
            'event_type',
            'start_date',
            'county__name'
        )
