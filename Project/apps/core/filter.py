import django_filters
from django import forms

from apps.core.project_requirements.filters_mixin import EventFilterNational2, EventFilterRegion2, EventFilterCounty2
from apps.core.models import ComingEvent, ScoutsCenter
from apps.jurisdictions.models import Region, County, SubCounty


class ComingeventFilterNational(EventFilterNational2):

    class Meta:
        model = ComingEvent
        fields = ['venue_name', 'start_date', 'region', 'county']


class ComingeventFilterRegion(EventFilterRegion2):

    class Meta:
        model = ComingEvent
        fields = ['venue_name', 'start_date', 'county']


class ComingeventFilterCounty(EventFilterCounty2):

    class Meta:
        model = ComingEvent
        fields = ['venue_name', 'start_date']


class ScoutsCenterFilter(django_filters.FilterSet):
    region = django_filters.ModelChoiceFilter(field_name='sub_county__county__region',
                                              queryset=Region.objects.all(),
                                              widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='sub_county__county', queryset=County.objects.all(),
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(field_name='sub_county', queryset=SubCounty.objects.all(),
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = ScoutsCenter
        fields = ['region', 'county', 'sub_county']
