from django.contrib.auth.mixins import LoginRequiredMixin

from apps.competitions.forms import CompetitionUpdateForm
from apps.competitions.models import Competition
from apps.core.project_requirements.access import SelfSuccessMessageMixinUpdated


class CompetitionUpdate(LoginRequiredMixin, SelfSuccessMessageMixinUpdated):
    form_class = CompetitionUpdateForm
    model = Competition
