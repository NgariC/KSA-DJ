import django_filters
from django import forms
from django.db.models import Q

from apps.core.project_requirements.filters_mixin import county_queryset, region_queryset, sub_county_queryset
from apps.projects.models import CSAProject, ALTProject, LTProject, UnitProject
from apps.registrations.models import Unit, Scout


class CsaprojectFilterNational(django_filters.FilterSet):
    unit = django_filters.ModelChoiceFilter(field_name='jasiri_scouts__unit', queryset=Unit.objects.all(),
                                            widget=forms.Select, label='Unit')
    region = django_filters.ModelChoiceFilter(field_name='jasiri_scouts__unit__sub_county__county__region',
                                              queryset=region_queryset,
                                              widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='jasiri_scouts__unit__sub_county__county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(field_name='jasiri_scouts__unit__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = CSAProject
        fields = ['unit', 'region', 'county', 'sub_county']


class CsaprojectFilterRegion(django_filters.FilterSet):
    unit = django_filters.ModelChoiceFilter(field_name='jasiri_scouts__unit', queryset=Unit.objects.all(),
                                            widget=forms.Select, label='Unit')
    county = django_filters.ModelChoiceFilter(field_name='jasiri_scouts__unit__sub_county__county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(field_name='jasiri_scouts__unit__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = CSAProject
        fields = ['unit', 'county', 'sub_county']


class CsaprojectFilterCounty(django_filters.FilterSet):
    unit = django_filters.ModelChoiceFilter(field_name='jasiri_scouts__unit', queryset=Unit.objects.all(),
                                            widget=forms.Select, label='Unit')
    sub_county = django_filters.ModelChoiceFilter(field_name='jasiri_scouts__unit__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = CSAProject
        fields = ['unit', 'sub_county']


class CsaprojectFilterSubCounty(django_filters.FilterSet):
    unit = django_filters.ModelChoiceFilter(field_name='jasiri_scouts__unit', queryset=Unit.objects.all(),
                                            widget=forms.Select, label='Unit')

    class Meta:
        model = CSAProject
        fields = ['unit']


class CsaprojectFilterUnit(django_filters.FilterSet):
    jasiri_scouts = django_filters.ModelChoiceFilter(field_name='jasiri_scouts__name',
                                                     queryset=Scout.objects.filter(
                                                         Q(section='Jasiri') & Q(active=True)),
                                                     widget=forms.Select,
                                                     label='Jasiri Name')

    class Meta:
        model = CSAProject
        fields = ['jasiri_scouts', 'title']


class AltprojectFilterNational(django_filters.FilterSet):
    region = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county__region',
                                              queryset=region_queryset,
                                              widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = ALTProject
        fields = ['region', 'county', 'sub_county']


class LtprojectFilterNational(django_filters.FilterSet):
    region = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county__region',
                                              queryset=region_queryset,
                                              widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(field_name='scout_leader_name__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = LTProject
        fields = ['region', 'county', 'sub_county']


class UnitprojectFilterNational(django_filters.FilterSet):
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=Unit.objects.all(),
                                            widget=forms.Select, label='Unit')
    region = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county__region',
                                              queryset=region_queryset,
                                              widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = UnitProject
        fields = ['unit', 'region', 'county', 'sub_county']


class UnitprojectFilterRegion(django_filters.FilterSet):
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=Unit.objects.all(),
                                            widget=forms.Select, label='Unit')
    county = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county',
                                              queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = UnitProject
        fields = ['unit', 'county', 'sub_county']


class UnitprojectFilterCounty(django_filters.FilterSet):
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=Unit.objects.all(),
                                            widget=forms.Select, label='Unit')
    sub_county = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = UnitProject
        fields = ['unit', 'sub_county']


class UnitprojectFilterSubCounty(django_filters.FilterSet):
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=Unit.objects.all(),
                                            widget=forms.Select, label='Unit')

    class Meta:
        model = UnitProject
        fields = ['unit']


class UnitprojectFilterUnit(django_filters.FilterSet):

    class Meta:
        model = UnitProject
        fields = ['title']
