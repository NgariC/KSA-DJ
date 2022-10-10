from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from apps.celebrations.models import Founderee, CountyParticipants


class FoundereeDetail(LoginRequiredMixin, generic.DetailView):
    model = Founderee


class CountyParticipantsDetail(LoginRequiredMixin, generic.DetailView):
    model = CountyParticipants
