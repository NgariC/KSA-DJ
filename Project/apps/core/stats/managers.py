from django.db import models


class ComingEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'county').defer(
            'requirement',
            'county__region',
            'county__region__country',
            'event_coordinators'
        )
