import django_filters
from django import forms

from apps.celebrations.models import Founderee, CountyParticipants
from apps.core.project_requirements.filters_mixin import region_queryset, county_queryset


class FoundereeFilterNational(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year')
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')
    county = django_filters.ModelChoiceFilter(field_name='county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')
    region = django_filters.ModelChoiceFilter(field_name='county__region',
                                              queryset=region_queryset,
                                              widget=forms.Select, label='Region')

    class Meta:
        model = Founderee
        fields = ['year', 'start_date', 'venue_name', 'region', 'county']


class FoundereeFilterRegion(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year')
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')
    county = django_filters.ModelChoiceFilter(field_name='county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')

    class Meta:
        model = Founderee
        fields = ['year', 'start_date', 'venue_name', 'county']


class FoundereeFilterCounty(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year')
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Founderee
        fields = ['year', 'start_date', 'venue_name']


class CountyparticipantsFilterNational(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year')
    county = django_filters.ModelChoiceFilter(field_name='county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')
    region = django_filters.ModelChoiceFilter(field_name='county__region',
                                              queryset=region_queryset,
                                              widget=forms.Select, label='Region')

    class Meta:
        model = CountyParticipants
        fields = ['year', 'region', 'county']


class CountyparticipantsFilterRegion(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year')
    county = django_filters.ModelChoiceFilter(field_name='county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')

    class Meta:
        model = CountyParticipants
        fields = ['year', 'county']


class CountyparticipantsFilterCounty(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = CountyParticipants
        fields = ['year']
