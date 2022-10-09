from django.db import models


class CSAProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'supervisor').prefetch_related(
            'jasiri_scouts').defer(
                'project_description')


class ALTProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'scout_leader_name',
            'supervisor').defer(
                'project_description')


class UnitProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'unit',
            'coordinator').defer(
                'project_description')
