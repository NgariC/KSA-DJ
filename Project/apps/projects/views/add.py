from django.contrib.auth.mixins import LoginRequiredMixin
from apps.projects.forms import CSAProjectForm, ALTProjectForm, LTProjectForm, UnitProjectForm

from apps.core.project_requirements.access import SelfSuccessMessageMixinAdded
from apps.projects.models import CSAProject, ALTProject, LTProject, UnitProject


class AddCSAProject(LoginRequiredMixin, SelfSuccessMessageMixinAdded):
    form_class = CSAProjectForm
    model = CSAProject


class AddALTProject(LoginRequiredMixin, SelfSuccessMessageMixinAdded):
    form_class = ALTProjectForm
    model = ALTProject


class AddLTProject(LoginRequiredMixin, SelfSuccessMessageMixinAdded):
    form_class = LTProjectForm
    model = LTProject


class AddUnitProject(LoginRequiredMixin, SelfSuccessMessageMixinAdded):
    form_class = UnitProjectForm
    model = UnitProject
