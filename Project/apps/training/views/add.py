from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from apps.core.project_requirements.access import SelfSuccessMessageMixinAdded, StaffMemberRequiredForm, SubCountyMemberRequiredForm
from apps.training.forms import ITCForm, PTCForm, WBIForm, WBIIForm, WBIIIForm, ALTForm, LTForm, SLSpecialEventForm
from apps.training.models import ITC, PTC, WBI, WBII, WBIII, ALT, LT, SLSpecialEvent


class AddITC(SubCountyMemberRequiredForm, SelfSuccessMessageMixinAdded):
    form_class = ITCForm
    model = ITC


class AddPTC(SubCountyMemberRequiredForm, SelfSuccessMessageMixinAdded):
    form_class = PTCForm
    model = PTC


class AddWBI(LoginRequiredMixin, SelfSuccessMessageMixinAdded):
    form_class = WBIForm
    model = WBI
    success_url = reverse_lazy('training:wbi')


class AddWBII(StaffMemberRequiredForm, SelfSuccessMessageMixinAdded):
    form_class = WBIIForm
    model = WBII


class AddWBIII(LoginRequiredMixin, SelfSuccessMessageMixinAdded):
    form_class = WBIIIForm
    model = WBIII
    success_url = reverse_lazy('training:wbiii')


class AddALT(StaffMemberRequiredForm, SelfSuccessMessageMixinAdded):
    form_class = ALTForm
    model = ALT


class AddLT(StaffMemberRequiredForm, SelfSuccessMessageMixinAdded):
    form_class = LTForm
    model = LT


class AddSLSpecialEvent(SubCountyMemberRequiredForm, SelfSuccessMessageMixinAdded):
    form_class = SLSpecialEventForm
    model = SLSpecialEvent
