import django_filters
from django import forms

from apps.competitions.models import Competition, CompetitionTeam, SpecialTeamsCategories
from apps.core.project_requirements.filters_mixin import region_queryset, county_queryset, sub_county_queryset
from apps.core.project_requirements.utilities import GENDER

LEVEL = (
    ('SubCounty', 'SubCounty'),
    ('County', 'County'),
    ('Region', 'Region'),
    ('National', 'National'),
    ('Zonal', 'Zonal'),
)
SECTION = (
    ('Chipukizi', 'Chipukizi'),
    ('Mwamba', 'Mwamba'),
    ('Jasiri', 'Jasiri'),
)


class CompetitionteamFilterNational(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year', label='Year of Competition')
    section = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple)
    level_of_competition = django_filters.MultipleChoiceFilter(choices=LEVEL, widget=forms.CheckboxSelectMultiple)
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    special_category = django_filters.ModelChoiceFilter(field_name='special_category',
                                                        queryset=SpecialTeamsCategories.objects.all(),
                                                        widget=forms.Select)
    region = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county__region',
                                              queryset=region_queryset,
                                              widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(field_name='unit__sub_county', queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = CompetitionTeam
        fields = ['year', 'region', 'county', 'sub_county',
                  'special_category', 'gender', 'section', 'level_of_competition']


class CompetitionteamFilterRegion(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year', label='Year of Competition')
    section = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple)
    level_of_competition = django_filters.MultipleChoiceFilter(choices=LEVEL, widget=forms.CheckboxSelectMultiple)
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    special_category = django_filters.ModelChoiceFilter(field_name='special_category',
                                                        queryset=SpecialTeamsCategories.objects.all(),
                                                        widget=forms.Select)
    county = django_filters.ModelChoiceFilter(field_name='unit__sub_county__county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(field_name='unit__sub_county', queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = CompetitionTeam
        fields = ['year', 'county', 'sub_county',
                  'special_category', 'gender', 'section', 'level_of_competition']


class CompetitionteamFilterCounty(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year', label='Year of Competition')
    section = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple)
    level_of_competition = django_filters.MultipleChoiceFilter(choices=LEVEL, widget=forms.CheckboxSelectMultiple)
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    special_category = django_filters.ModelChoiceFilter(field_name='special_category',
                                                        queryset=SpecialTeamsCategories.objects.all(),
                                                        widget=forms.Select)
    sub_county = django_filters.ModelChoiceFilter(field_name='unit__sub_county', queryset=sub_county_queryset,
                                                  widget=forms.Select, label='SubCounty')

    class Meta:
        model = CompetitionTeam
        fields = ['year', 'sub_county', 'special_category', 'gender', 'section', 'level_of_competition']


class CompetitionteamFilterSubCounty(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year', label='Year of Competition')
    section = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple)
    level_of_competition = django_filters.MultipleChoiceFilter(choices=LEVEL, widget=forms.CheckboxSelectMultiple)
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    special_category = django_filters.ModelChoiceFilter(field_name='special_category',
                                                        queryset=SpecialTeamsCategories.objects.all(),
                                                        widget=forms.Select)

    class Meta:
        model = CompetitionTeam
        fields = ['year', 'special_category', 'gender', 'section', 'level_of_competition']


class CompetitionteamFilterUnit(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year', label='Year of Competition')
    section = django_filters.MultipleChoiceFilter(choices=SECTION, widget=forms.CheckboxSelectMultiple)
    level_of_competition = django_filters.MultipleChoiceFilter(choices=LEVEL, widget=forms.CheckboxSelectMultiple)
    gender = django_filters.ChoiceFilter(choices=GENDER, widget=forms.RadioSelect())
    special_category = django_filters.ModelChoiceFilter(field_name='special_category',
                                                        queryset=SpecialTeamsCategories.objects.all(),
                                                        widget=forms.Select)

    class Meta:
        model = CompetitionTeam
        fields = ['year', 'special_category', 'gender', 'section', 'level_of_competition']


class CompetitionFilterNational(django_filters.FilterSet):
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')
    level = django_filters.MultipleChoiceFilter(choices=LEVEL, widget=forms.CheckboxSelectMultiple)
    region = django_filters.ModelChoiceFilter(field_name='region', queryset=region_queryset,
                                              widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select,
                                                  label='SubCounty')

    class Meta:
        model = Competition
        fields = ['venue_name', 'start_date', 'level', 'region', 'county', 'sub_county']


class CompetitionFilterRegion(django_filters.FilterSet):
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')
    level = django_filters.MultipleChoiceFilter(choices=LEVEL, widget=forms.CheckboxSelectMultiple)
    county = django_filters.ModelChoiceFilter(field_name='county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select,
                                                  label='SubCounty')

    class Meta:
        model = Competition
        fields = ['venue_name', 'start_date', 'level', 'county', 'sub_county']


class CompetitionFilterCounty(django_filters.FilterSet):
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')
    level = django_filters.MultipleChoiceFilter(choices=LEVEL, widget=forms.CheckboxSelectMultiple)
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select,
                                                  label='SubCounty')

    class Meta:
        model = Competition
        fields = ['venue_name', 'start_date', 'level', 'sub_county']


class CompetitionFilterSubCounty(django_filters.FilterSet):
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')
    level = django_filters.MultipleChoiceFilter(choices=LEVEL, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Competition
        fields = ['venue_name', 'start_date', 'level']
