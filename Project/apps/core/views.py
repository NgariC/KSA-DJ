from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic
from django_filters.views import FilterView

from apps.core.project_requirements.access import CountyMemberQueryset, SelfSuccessMessageMixinAdded
from apps.core.filter import ScoutsCenterFilter, ComingeventFilterCounty, ComingeventFilterRegion, \
    ComingeventFilterNational
from apps.core.forms import ContactForm, RegistrationForm, ComingEventForm
from apps.core.models import Slide, Department, WeProduce, ComingEvent, ScoutingInBrief, About, ScoutsCenter, \
    Registration
from apps.files.models import Document


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = Slide.objects.filter(featured=True).order_by('-timestamp')[:5]

        context['abouts'] = About.objects.all()
        context['departments'] = Department.objects.all()[:6]
        context['we_produce'] = WeProduce.objects.all()
        context['comingevents'] = ComingEvent.objects.featured()[:5]
        context['document_list'] = Document.objects.filter(date_to_cease_showing__gte=datetime.now().date())[:5]

        context['scouting_in_brief'] = ScoutingInBrief.objects.all()
        context["total_scouts"] = 2100000
        context["scoutleaders_count"] = 40000

        return context


class ContactUs(LoginRequiredMixin, generic.FormView):
    form_class = ContactForm
    template_name = 'form.html'

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        from_email = form.cleaned_data['from_email']
        message = form.cleaned_data['message']
        try:
            send_mail(subject, message, from_email, ['ngangaricharles@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('core:success')


def clear(request):
    return HttpResponse("")


class AboutUs(LoginRequiredMixin, generic.ListView):
    model = About
    context_object_name = 'abouts'
    template_name = 'core/about_us.html'


class ComingEventList(FilterView, CountyMemberQueryset):
    model = ComingEvent
    context_object_name = 'coming_events'

    def get_filterset_class(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return ComingeventFilterNational
        if not user.link_to_scout_leader:
            raise PermissionDenied
        level = user.link_to_scout_leader.rank.level
        if level == 'National':
            return ComingeventFilterNational
        elif level == 'Regional':
            return ComingeventFilterRegion
        else:
            return ComingeventFilterCounty


class ComingEventDetail(LoginRequiredMixin, generic.DetailView):
    model = ComingEvent


class RegistrationDetail(LoginRequiredMixin, generic.DetailView):
    model = Registration


class AddComingEvent(LoginRequiredMixin, SelfSuccessMessageMixinAdded):
    form_class = ComingEventForm
    model = ComingEvent
    template_name = 'form.html'


class EventRegistration(LoginRequiredMixin, SelfSuccessMessageMixinAdded):
    form_class = RegistrationForm
    model = Registration
    template_name = 'form.html'


class ScoutsCenterList(LoginRequiredMixin, FilterView, generic.ListView):
    model = ScoutsCenter
    context_object_name = 'scouts_centers'
    filterset_class = ScoutsCenterFilter


class ScoutsCenterDetail(LoginRequiredMixin, generic.DetailView):
    model = ScoutsCenter
