from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from apps.competitions.models import CompetitionTeam, Competition


class CompetitionTeamDetail(LoginRequiredMixin, generic.DetailView):
    model = CompetitionTeam


class CompetitionDetail(LoginRequiredMixin, generic.DetailView):
    model = Competition
