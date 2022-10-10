from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.project_requirements.access import SelfSuccessMessageMixinUpdated
from apps.registrations.forms.update import ScoutUnitUpdateForm, ScoutSectionUpdateForm, ScoutLeaderUnitUpdateForm
from apps.registrations.models import Scout, ScoutLeader


class ScoutUnitUpdate(LoginRequiredMixin, SelfSuccessMessageMixinUpdated):
    model = Scout
    form_class = ScoutUnitUpdateForm


class ScoutSectionUpdate(LoginRequiredMixin, SelfSuccessMessageMixinUpdated):
    model = Scout
    form_class = ScoutSectionUpdateForm


class ScoutLeaderUnitUpdate(LoginRequiredMixin, SelfSuccessMessageMixinUpdated):
    model = ScoutLeader
    form_class = ScoutLeaderUnitUpdateForm
