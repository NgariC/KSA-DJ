from django.db import models


class FoundereeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'camp_chief',
            'county').prefetch_related('support_staff').defer(
            'county__region',
            'county__region__country'
        )


class PatronsDayManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
