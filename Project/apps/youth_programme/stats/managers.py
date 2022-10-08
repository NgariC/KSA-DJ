from django.db import models


class InvestitureManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'investor',
            'sub_county').defer(
            'sub_county__county__region',
            'sub_county__county__region__country'
        )


class BadgeCampManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'examiner',
            'sub_county').defer(
            'sub_county__county__region',
            'sub_county__county__region__country'
        )


class PLCManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'course_director',
            'sub_county').defer(
            'sub_county__county__region',
            'sub_county__county__region__country'
        )
