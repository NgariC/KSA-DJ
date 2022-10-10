from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from apps.registrations.models import Unit, Scout, ScoutLeader


class UnitDetail(LoginRequiredMixin, generic.DetailView):
    model = Unit


class ScoutDetail(LoginRequiredMixin, generic.DetailView):
    model = Scout


class ScoutLeaderDetail(LoginRequiredMixin, generic.DetailView):
    model = ScoutLeader
