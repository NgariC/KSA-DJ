from django.contrib.auth.mixins import LoginRequiredMixin

from apps.celebrations.forms import FoundereeForm, CountyParticipantsForm
from apps.celebrations.models import Founderee, CountyParticipants
from apps.core.project_requirements.access import SelfSuccessMessageMixinAdded


class AddFounderee(LoginRequiredMixin, SelfSuccessMessageMixinAdded):
    form_class = FoundereeForm
    model = Founderee


class AddCountyParticipants(LoginRequiredMixin, SelfSuccessMessageMixinAdded):
    form_class = CountyParticipantsForm
    model = CountyParticipants
