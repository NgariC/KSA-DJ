from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from apps.core.project_requirements.access import SelfSuccessMessageMixinRegistered, DateRegulated, \
    SelfSuccessMessageMixinRegisteredNoLog
from apps.core.project_requirements.log import log_addition
from apps.registrations.models import Unit, Scout, ScoutLeader, ScoutLeaderCert
from apps.registrations.forms import UnitForm, JasiriForm, ScoutLeaderForm, SectionSelectForm, SunguraForm, \
    ChipukiziForm, MwambaForm, ScoutLeaderCertForm


class AddUnit(LoginRequiredMixin, SelfSuccessMessageMixinRegistered):
    form_class = UnitForm
    model = Unit

    def post(self, request, *args, **kwargs):
        save_action = super().post(request, *args, **kwargs)
        if "another" in request.POST:
            return HttpResponseRedirect(reverse('registrations:add_unit'))
        return save_action


class SectionSelect(LoginRequiredMixin, generic.FormView, DateRegulated):
    form_class = SectionSelectForm
    success_url = reverse_lazy('registrations:add_scout')
    template_name = 'form.html'

    def post(self, request, *args, **kwargs):
        save_action = super().post(request, *args, **kwargs)
        self.request.session['section'] = self.request.POST.get('section')
        if "another" in request.POST:
            return HttpResponseRedirect(reverse('registrations:add_scout'))
        return save_action


class AddScout(LoginRequiredMixin, SelfSuccessMessageMixinRegisteredNoLog):
    model = Scout

    def get_form_class(self, *args, **kwargs):
        section = self.request.session.get('section')
        if section == 'Sungura':
            return SunguraForm
        elif section == 'Chipukizi':
            return ChipukiziForm
        elif section == 'Mwamba':
            return MwambaForm
        else:
            return JasiriForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.section = self.request.session.get('section')
        log_addition(object=form.save())
        form.save()
        return super().form_valid(form)


class AddScoutLeader(LoginRequiredMixin, SelfSuccessMessageMixinRegistered):
    form_class = ScoutLeaderForm
    model = ScoutLeader

    def post(self, request, *args, **kwargs):
        save_action = super().post(request, *args, **kwargs)
        if "another" in request.POST:
            return HttpResponseRedirect(reverse('registrations:add_scout_leader'))
        return save_action


class AddScoutLeaderCert(LoginRequiredMixin, SelfSuccessMessageMixinRegistered):
    form_class = ScoutLeaderCertForm
    model = ScoutLeaderCert
