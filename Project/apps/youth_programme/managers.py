from django.db import models
from django.db.models import Count


class InvestitureManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('investor', 'director', 'sub_county', 'sub_county__county',
                                                     'sub_county__county__region').annotate(
            _participants_count=Count("trainees__id", distinct=True))

    def paid(self):
        return super().get_queryset().select_related('investor', 'director', 'sub_county', 'sub_county__county',
                                                     'sub_county__county__region').filter(payments=True)


class BadgeCampManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('examiner', 'director', 'sub_county', 'sub_county__county',
                                                     'sub_county__county__region').annotate(
            _participants_count=Count("trainees__id", distinct=True))

    def paid(self):
        return super().get_queryset().select_related('examiner', 'director', 'sub_county', 'sub_county__county',
                                                     'sub_county__county__region').filter(payments=True)


class CManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('course_director', 'director', 'sub_county', 'sub_county__county',
                                                     'sub_county__county__region').annotate(
            _participants_count=Count("trainees__id", distinct=True))

    def paid(self):
        return super().get_queryset().select_related('course_director', 'director', 'sub_county', 'sub_county__county',
                                                     'sub_county__county__region').filter(payments=True)
