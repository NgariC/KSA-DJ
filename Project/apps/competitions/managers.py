from datetime import datetime

from django.db import models
from django.db.models import Count, Q


class TeamManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('unit', 'unit__sub_county', 'unit__sub_county__county',
                                                     'unit__sub_county__county__region', 'special_category').annotate(
            _competitors_count=Count("competitors__id", distinct=True),
            _leaders_count=Count("leaders__id", distinct=True),
        )

    def unit_leader(self):
        return super().get_queryset().select_related('unit', 'unit__sub_county', 'unit__sub_county__county',
                                                     'unit__sub_county__county__region', 'special_category')


class CompetitionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('chief_assessor', 'chief', 'sub_county', 'sub_county__county',
                                                     'sub_county__county__region', 'country').annotate(
            competitors_count=Count("teams__competitors__id", distinct=True),
            leaders_count=Count("teams__leaders__id", distinct=True),
        )

    def paid(self):
        return super().get_queryset().select_related('chief_assessor', 'chief', 'sub_county', 'sub_county__county',
                                                     'sub_county__county__region', 'country').filter(payments=True)

    def paid_or_ongoing(self):
        return super().get_queryset().select_related('chief_assessor', 'chief', 'sub_county', 'sub_county__county',
                                                     'sub_county__county__region', 'country').filter(
            Q(end_date__gte=datetime.now()) | Q(payments=True))
