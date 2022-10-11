from django.urls import path, re_path
from django.views.generic import TemplateView

from apps.core import views

app_name = 'core'

urlpatterns = [
    path('email', views.ContactUs.as_view(), name='contact_us'),
    path('success', TemplateView.as_view(template_name='contact_form_sent.html'), name='success'),
    path('about-us', views.AboutUs.as_view(), name='about_us'),

    path('up-coming-events', views.ComingEventList.as_view(), name='ce'),
    re_path('up-coming-event-detail/(?P<pk>\d+)', views.ComingEventDetail.as_view(), name='ce_detail'),
    re_path('up-coming-event-registration/(?P<pk>\d+)', views.RegistrationDetail.as_view(), name='ce_registration'),
    path('up-coming-event/add', views.AddComingEvent.as_view(), name='add_ce'),
    path('event-registration', views.EventRegistration.as_view(), name='event_r'),

    path('scout-centers', views.ScoutsCenterList.as_view(), name='scouts_centers'),
    re_path('scouts-center-detail/(?P<pk>\d+)', views.ScoutsCenterDetail.as_view(), name='sc_detail'),
]
