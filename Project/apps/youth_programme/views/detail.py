from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from apps.youth_programme.models import Investiture, BadgeCamp, ParkHoliday, PLC, RM


class InvestitureDetail(LoginRequiredMixin, generic.DetailView):
    model = Investiture


class BadgeCampDetail(LoginRequiredMixin, generic.DetailView):
    model = BadgeCamp


class ParkHolidayDetail(LoginRequiredMixin, generic.DetailView):
    model = ParkHoliday


class PLCDetail(LoginRequiredMixin, generic.DetailView):
    model = PLC


class RMDetail(LoginRequiredMixin, generic.DetailView):
    model = RM
