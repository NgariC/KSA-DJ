import django_filters
from django import forms

from apps.core.project_requirements.filters_mixin import county_queryset, sub_county_queryset, region_queryset, \
    unit_queryset, rank_queryset
from apps.core.project_requirements.utilities import GENDER
from apps.registrations.forms.scout import SECTION
from apps.registrations.models import Unit, Scout, ScoutLeader


class UnitFilterNational(django_filters.FilterSet):
    date_warranted = django_filters.DateRangeFilter(field_name='date_warranted')
    name = django_filters.CharFilter(lookup_expr='icontains')
    region = django_filters.ModelChoiceFilter(field_name='sub_county__county__region',
                                              queryset=region_queryset, widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='sub_county__county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select)
    sections = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple,
                                                   lookup_expr='icontains')

    class Meta:
        model = Unit
        fields = ['name', 'date_warranted', 'region', 'county', 'sub_county', 'sections']


class UnitFilterRegion(django_filters.FilterSet):
    date_warranted = django_filters.DateRangeFilter(field_name='date_warranted')
    name = django_filters.CharFilter(lookup_expr='icontains')
    county = django_filters.ModelChoiceFilter(field_name='sub_county__county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select)
    sections = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple,
                                                   lookup_expr='icontains')

    class Meta:
        model = Unit
        fields = ['name', 'date_warranted', 'county', 'sub_county', 'sections']


class UnitFilterCounty(django_filters.FilterSet):
    date_warranted = django_filters.DateRangeFilter(field_name='date_warranted')
    name = django_filters.CharFilter(lookup_expr='icontains')
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select)
    sections = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple,
                                                   lookup_expr='icontains')

    class Meta:
        model = Unit
        fields = ['name', 'date_warranted', 'sub_county', 'sections']


class UnitFilterSubCounty(django_filters.FilterSet):
    date_warranted = django_filters.DateRangeFilter(field_name='date_warranted')
    name = django_filters.CharFilter(lookup_expr='icontains')
    sections = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple,
                                                   lookup_expr='icontains')

    class Meta:
        model = Unit
        fields = ['name', 'date_warranted', 'sections']


class ScoutFilterNational(django_filters.FilterSet):
    registration_date = django_filters.DateRangeFilter(field_name='registration_date')
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    investiture = django_filters.BooleanFilter(label='Have undergone Investiture')
    section = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple)
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=unit_queryset,
                                            widget=forms.Select, label='Unit')
    region = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county__region',
                                              queryset=region_queryset,
                                              widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(field_name='unit__sub_county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = Scout
        fields = ['registration_date', 'region', 'county', 'sub_county', 'unit', 'investiture', 'gender', 'section']


class ScoutFilterRegion(django_filters.FilterSet):
    registration_date = django_filters.DateRangeFilter(field_name='registration_date')
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    section = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple)
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=unit_queryset,
                                            widget=forms.Select, label='Unit')
    county = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(field_name='unit__sub_county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = Scout
        fields = ['registration_date', 'county', 'sub_county', 'unit', 'investiture', 'gender', 'section']


class ScoutFilterCounty(django_filters.FilterSet):
    registration_date = django_filters.DateRangeFilter(field_name='registration_date')
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    section = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple)
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=unit_queryset,
                                            widget=forms.Select, label='Unit')
    sub_county = django_filters.ModelChoiceFilter(field_name='unit__sub_county',
                                                  queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = Scout
        fields = ['registration_date', 'sub_county', 'unit', 'investiture', 'gender', 'section']


class ScoutFilterSubCounty(django_filters.FilterSet):
    registration_date = django_filters.DateRangeFilter(field_name='registration_date')
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    section = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple)
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=unit_queryset,
                                            widget=forms.Select, label='Unit')

    class Meta:
        model = Scout
        fields = ['registration_date', 'unit', 'investiture', 'gender', 'section']


class ScoutFilterUnit(django_filters.FilterSet):
    registration_date = django_filters.DateRangeFilter(field_name='registration_date')
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    section = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Scout
        fields = ['registration_date', 'investiture', 'gender', 'section']


class ScoutleaderFilterNational(django_filters.FilterSet):
    registration_date = django_filters.DateRangeFilter(field_name='registration_date')
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    region = django_filters.ModelChoiceFilter(field_name='sub_county__county__region', queryset=region_queryset,
                                              widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='sub_county__county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select)
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=unit_queryset,
                                            widget=forms.Select, label='Unit')
    rank = django_filters.ModelChoiceFilter(field_name='rank', queryset=rank_queryset,
                                            widget=forms.Select, label='Rank')

    class Meta:
        model = ScoutLeader
        fields = ['registration_date', 'region', 'county', 'sub_county', 'unit', 'rank', 'training', 'gender']


class ScoutleaderFilterRegion(django_filters.FilterSet):
    registration_date = django_filters.DateRangeFilter(field_name='registration_date')
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    county = django_filters.ModelChoiceFilter(field_name='sub_county__county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select)
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=unit_queryset,
                                            widget=forms.Select, label='Unit')
    rank = django_filters.ModelChoiceFilter(field_name='rank', queryset=rank_queryset,
                                            widget=forms.Select, label='Rank')

    class Meta:
        model = ScoutLeader
        fields = ['registration_date', 'county', 'sub_county', 'unit', 'rank', 'training', 'gender']


class ScoutleaderFilterCounty(django_filters.FilterSet):
    registration_date = django_filters.DateRangeFilter(field_name='registration_date')
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select)
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=unit_queryset,
                                            widget=forms.Select, label='Unit')
    rank = django_filters.ModelChoiceFilter(field_name='rank', queryset=rank_queryset,
                                            widget=forms.Select, label='Rank')

    class Meta:
        model = ScoutLeader
        fields = ['registration_date', 'sub_county', 'unit', 'rank', 'training', 'gender']


class ScoutleaderFilterSubCounty(django_filters.FilterSet):
    registration_date = django_filters.DateRangeFilter(field_name='registration_date')
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    unit = django_filters.ModelChoiceFilter(field_name='unit', queryset=unit_queryset,
                                            widget=forms.Select, label='Unit')
    rank = django_filters.ModelChoiceFilter(field_name='rank', queryset=rank_queryset,
                                            widget=forms.Select, label='Rank')

    class Meta:
        model = ScoutLeader
        fields = ['registration_date', 'unit', 'rank', 'training', 'gender']


class ScoutleaderFilterUnit(django_filters.FilterSet):
    registration_date = django_filters.DateRangeFilter(field_name='registration_date')
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    rank = django_filters.ModelChoiceFilter(field_name='rank', queryset=rank_queryset,
                                            widget=forms.Select, label='Rank')

    class Meta:
        model = ScoutLeader
        fields = ['registration_date', 'rank', 'training', 'gender']
