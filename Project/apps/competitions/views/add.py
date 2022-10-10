from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic

from apps.competitions.forms import CPForm, MPForm, JCForm, SCCForm, CCForm, RCForm, LevelSelectForm1, \
    LevelSelectForm2, LevelSelectForm3, SectionSelectForm
from apps.competitions.models import Competition
from apps.core.project_requirements.access import SelfSuccessMessageMixinAddedNoLog
from apps.core.project_requirements.log import log_addition


class SectionSelect(LoginRequiredMixin, generic.FormView):
    form_class = SectionSelectForm
    template_name = 'form.html'
    success_url = reverse_lazy('competitions:add_team')

    def post(self, request, *args, **kwargs):
        self.request.session['team_section'] = self.request.POST.get('team_section')
        return super().post(request, *args, **kwargs)


class AddTeam(LoginRequiredMixin, SelfSuccessMessageMixinAddedNoLog):

    def get_form_class(self, *args, **kwargs):
        team_section = self.request.session.get('team_section')
        if team_section == 'Chipukizi':
            return CPForm
        elif team_section == 'Mwamba':
            return MPForm
        else:
            return JCForm

    def form_valid(self, form):
        team = form.save(commit=False)
        team.section = self.request.session.get('team_section')
        log_addition(object=form.save())
        form.save()
        return super().form_valid(form)


class LevelSelect(LoginRequiredMixin, generic.FormView):
    template_name = 'form.html'
    success_url = reverse_lazy('competitions:add_competition')

    def get_form_class(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return LevelSelectForm3
        if not user.link_to_scout_leader:
            raise PermissionDenied()
        if user.link_to_scout_leader.rank.level in ['National', 'Regional']:
            return LevelSelectForm3
        elif user.link_to_scout_leader.rank.level == 'County':
            return LevelSelectForm2
        elif user.link_to_scout_leader.rank.level == 'SubCounty':
            return LevelSelectForm1
        else:
            raise PermissionDenied()



    def post(self, request, *args, **kwargs):
        self.request.session['level'] = self.request.POST.get('level')
        return super().post(request, *args, **kwargs)


class AddCompetition(LoginRequiredMixin, SelfSuccessMessageMixinAddedNoLog):
    model = Competition

    def get_form_class(self, *args, **kwargs):
        section = self.request.session.get('level')
        if section == 'Regional':
            return RCForm
        elif section == 'County':
            return CCForm
        else:
            return SCCForm

    def form_valid(self, form):
        competition = form.save(commit=False)
        competition.level = self.request.session.get('level')
        log_addition(object=form.save())
        form.save()
        return super().form_valid(form)
