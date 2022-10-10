import django_filters
from django import forms

from apps.core.project_requirements.filters_mixin import (region_queryset, county_queryset, sub_county_queryset, EventFilterNational,
                                                          EventFilterRegion, EventFilterCounty, EventFilterSubCounty, EventFilterNational2,
                                                          EventFilterRegion2, EventFilterCounty2)
from apps.training.models import ITC, PTC, WBI, WBII, WBIII, ALT, LT, SLSpecialEvent


class ItcFilterNational(EventFilterNational):

    class Meta:
        model = ITC
        fields = ['venue_name', 'start_date', 'region', 'county', 'sub_county']


class ItcFilterRegion(EventFilterRegion):

    class Meta:
        model = ITC
        fields = ['venue_name', 'start_date', 'county', 'sub_county']


class ItcFilterCounty(EventFilterCounty):

    class Meta:
        model = ITC
        fields = ['venue_name', 'start_date', 'sub_county']


class ItcFilterSubCounty(EventFilterSubCounty):

    class Meta:
        model = ITC
        fields = ['venue_name', 'start_date']


class PtcFilterNational(EventFilterNational):

    class Meta:
        model = PTC
        fields = ['venue_name', 'start_date', 'region', 'county', 'sub_county']


class PtcFilterRegion(EventFilterRegion):

    class Meta:
        model = PTC
        fields = ['venue_name', 'start_date', 'county', 'sub_county']


class PtcFilterCounty(EventFilterCounty):

    class Meta:
        model = PTC
        fields = ['venue_name', 'start_date', 'sub_county']


class PtcFilterSubCounty(EventFilterSubCounty):

    class Meta:
        model = PTC
        fields = ['venue_name', 'start_date']


class WbiiFilterNational(EventFilterNational2):

    class Meta:
        model = WBII
        fields = ['venue_name', 'start_date', 'region', 'county']


class WbiiFilterRegion(EventFilterRegion2):

    class Meta:
        model = WBII
        fields = ['venue_name', 'start_date', 'county']


class WbiiFilterCounty(EventFilterCounty2):

    class Meta:
        model = WBII
        fields = ['venue_name', 'start_date']


class AltFilterNational(EventFilterNational2):

    class Meta:
        model = ALT
        fields = ['venue_name', 'start_date', 'region', 'county']


class LtFilterNational(EventFilterNational2):

    class Meta:
        model = LT
        fields = ['venue_name', 'start_date', 'region', 'county']


class SlspecialeventFilterNational(EventFilterNational):

    class Meta:
        model = SLSpecialEvent
        fields = ['venue_name', 'start_date', 'region', 'county', 'sub_county']


class SlspecialeventFilterRegion(EventFilterRegion):

    class Meta:
        model = SLSpecialEvent
        fields = ['venue_name', 'start_date', 'county', 'sub_county']


class SlspecialeventFilterCounty(EventFilterCounty):

    class Meta:
        model = SLSpecialEvent
        fields = ['venue_name', 'start_date', 'sub_county']


class SlspecialeventFilterSubCounty(EventFilterSubCounty):

    class Meta:
        model = SLSpecialEvent
        fields = ['venue_name', 'start_date']


class WbiFilterNational(django_filters.FilterSet):
    submission_date = django_filters.DateRangeFilter(field_name='submission_date')
    sub_county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')
    county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')
    region = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county__region',
                                              queryset=region_queryset,
                                              widget=forms.Select, label='Region')

    class Meta:
        model = WBI
        fields = ['submission_date', 'region', 'county', 'sub_county']


class WbiFilterRegion(django_filters.FilterSet):
    submission_date = django_filters.DateRangeFilter(field_name='submission_date')
    sub_county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')
    county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')

    class Meta:
        model = WBI
        fields = ['submission_date', 'county', 'sub_county']


class WbiFilterCounty(django_filters.FilterSet):
    submission_date = django_filters.DateRangeFilter(field_name='submission_date')
    sub_county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = WBI
        fields = ['submission_date', 'sub_county']


class WbiiiFilterNational(django_filters.FilterSet):
    assessed = django_filters.BooleanFilter(field_name='assessed')
    sub_county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')
    county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')
    region = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county__region',
                                              queryset=region_queryset,
                                              widget=forms.Select, label='Region')

    class Meta:
        model = WBIII
        fields = ['assessed', 'region', 'county', 'sub_county']


class WbiiiFilterRegion(django_filters.FilterSet):
    assessed = django_filters.BooleanFilter(field_name='assessed')
    sub_county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')
    county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')

    class Meta:
        model = WBIII
        fields = ['assessed', 'county', 'sub_county']


class WbiiiFilterCounty(django_filters.FilterSet):
    assessed = django_filters.BooleanFilter(field_name='assessed')
    sub_county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = WBIII
        fields = ['assessed', 'sub_county']


class WbiiiFilterSubCounty(django_filters.FilterSet):
    assessed = django_filters.BooleanFilter(field_name='assessed')

    class Meta:
        model = WBIII
        fields = ['assessed']
