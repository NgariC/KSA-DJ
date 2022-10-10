from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from apps.projects.models import CSAProject, ALTProject, LTProject, UnitProject


class CSAProjectDetail(LoginRequiredMixin, generic.DetailView):
    model = CSAProject


class ALTProjectDetail(LoginRequiredMixin, generic.DetailView):
    model = ALTProject


class LTProjectDetail(LoginRequiredMixin, generic.DetailView):
    model = LTProject


class UnitProjectDetail(LoginRequiredMixin, generic.DetailView):
    model = UnitProject
