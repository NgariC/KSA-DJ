from django.db import models
from django.db.models import Count


class FoundereeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
                'camp_chief',
                'county').defer(
                        'county__region',
                        'county__region__country'
                    ).annotate(
                    _staff_count=Count("support_staff__id", distinct=True))


class LinkBadgeAwardManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('sungura_scouts').annotate(
            _scouts_count=Count("sungura_scouts__id", distinct=True))


class ChuiBadgeAwardManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('chipukizi_scouts').annotate(
            _scouts_count=Count("chipukizi_scouts__id", distinct=True))


class SimbaBadgeAwardManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('mwamba_scouts').annotate(
            _scouts_count=Count("mwamba_scouts__id", distinct=True))


class ChiefScoutAwardManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('jasiri_scouts').annotate(
            _scouts_count=Count("jasiri_scouts__id", distinct=True))


class ScoutLeaderAwardManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('scout_leaders').annotate(
            _scout_leaders_count=Count("scout_leaders__id", distinct=True))


class BeadsAwardManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('scout_leaders').annotate(
            _scout_leaders_count=Count("scout_leaders__id", distinct=True))


class CountyParticipantsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('county').annotate(
            _sungura_scouts_count=Count("sungura_scouts__id", distinct=True),
            _chipukizi_scouts_count=Count("chipukizi_scouts__id", distinct=True),
            _mwamba_scouts_count=Count("mwamba_scouts__id", distinct=True),
            _jasiri_scouts_count=Count("jasiri_scouts__id", distinct=True),
            _scout_leaders_count=Count("scout_leaders__id", distinct=True))


class PatronsDayManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'sungura_awards',
            'chipukizi_awards',
            'mwamba_awards',
            'jasiri_awards',
            'scout_leaders_awards',
            'county_participants').annotate(
            _sungura_scouts_count=Count("sungura_awards__sungura_scouts__id", distinct=True),
            _chipukizi_scouts_count=Count("chipukizi_awards__chipukizi_scouts__id", distinct=True),
            _mwamba_scouts_count=Count("mwamba_awards__mwamba_scouts__id", distinct=True),
            _jasiri_scouts_count=Count("jasiri_awards__jasiri_scouts__id", distinct=True),
            _scout_leaders_count=Count("scout_leaders_awards__scout_leaders__id", distinct=True),
            _scout_attendees_count=Count("county_participants__scouts_attendees__id", distinct=True),
            _scout_leaders_attendees_count=Count("county_participants__scout_leaders_attendees__id", distinct=True))
