from braces.views import StaffuserRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from apps.training.models import ITC, PTC, WBI, WBII, WBIII, ALT, LT, SLSpecialEvent


class ITCDetail(LoginRequiredMixin, generic.DetailView):
    model = ITC


class PTCDetail(LoginRequiredMixin, generic.DetailView):
    model = PTC


class WBIDetail(LoginRequiredMixin, generic.DetailView):
    model = WBI


class WBIIDetail(LoginRequiredMixin, generic.DetailView):
    model = WBII


class WBIIIDetail(LoginRequiredMixin, generic.DetailView):
    model = WBIII


class ALTDetail(LoginRequiredMixin, generic.DetailView):
    model = ALT


class LTDetail(StaffuserRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = LT


class SLSpecialEventDetail(LoginRequiredMixin, generic.DetailView):
    model = SLSpecialEvent
