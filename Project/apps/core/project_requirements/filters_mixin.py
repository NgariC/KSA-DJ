import django_filters
from django import forms
from django.db.models import Q

from apps.jurisdictions.models import Rank, Region, County, SubCounty
from apps.registrations.models import Unit


def region_queryset(request):
    user = request.user
    if user.is_superuser or user.is_staff:
        return Region.objects.all()
    if not user.link_to_scout_leader.sub_county:
        return Region.objects.none()
    level = user.link_to_scout_leader.rank.level
    return Region.objects.all() if level == 'National' else Region.objects.filter(
        country=user.link_to_scout_leader.sub_county.county.region.country)


def county_queryset(request):
    user = request.user
    if user.is_superuser or user.is_staff:
        return County.objects.all()
    if not user.link_to_scout_leader.sub_county:
        return County.objects.none()
    level = user.link_to_scout_leader.rank.level
    return County.objects.all() if level == 'National' else County.objects.filter(
        region=user.link_to_scout_leader.sub_county.county.region)


def sub_county_queryset(request):
    user = request.user
    if user.is_superuser or user.is_staff:
        return SubCounty.objects.all()
    if not user.link_to_scout_leader.sub_county:
        return SubCounty.objects.none()
    level = user.link_to_scout_leader.rank.level
    if level == 'National':
        return SubCounty.objects.all()
    elif level == 'Regional':
        return SubCounty.objects.filter(county__region=user.link_to_scout_leader.sub_county.county.region)
    else:
        return SubCounty.objects.filter(county=user.link_to_scout_leader.sub_county.county)


def unit_queryset(request):
    user = request.user
    if user.is_superuser or user.is_staff:
        return Unit.objects.active()
    if not user.link_to_scout_leader.sub_county:
        return Unit.objects.none()
    level = user.link_to_scout_leader.rank.level
    if level == 'National':
        return Unit.objects.active()
    elif level == 'Regional':
        return Unit.objects.filter(
            Q(active=True) | Q(sub_county__county__region=user.link_to_scout_leader.sub_county.county.region))
    elif level == 'County':
        return Unit.objects.filter(Q(active=True) | Q(sub_county__county=user.link_to_scout_leader.sub_county.county))
    elif level == 'SubCounty':
        return Unit.objects.filter(Q(active=True) | Q(sub_county=user.link_to_scout_leader.sub_county))
    else:
        return Unit.objects.filter(Q(active=True) | Q(
            name=user.link_to_scout_leader.unit.name)) if user.link_to_scout_leader.unit else Unit.objects.none()


def rank_queryset(request):
    user = request.user
    if user.is_superuser or user.is_staff:
        return Rank.objects.exclude(Q(code="PATRON") |
                                    Q(code="CS") |
                                    Q(code="CC") |
                                    Q(code="DCC") |
                                    Q(level="Scouts"))
    if not user.link_to_scout_leader.sub_county:
        return Rank.objects.none()
    user_level = user.link_to_scout_leader.rank.level
    if user_level == 'National':
        return Rank.objects.exclude(Q(code="PATRON") |
                                    Q(code="CS") |
                                    Q(code="CC") |
                                    Q(code="DCC") |
                                    Q(level="Scouts"))
    elif user_level == 'Regional':
        return Rank.objects.exclude(Q(level="National") |
                                    Q(level="Regional") |
                                    Q(level="Scouts"))
    elif user_level == 'County':
        return Rank.objects.exclude(Q(level="National") |
                                    Q(level="Regional") |
                                    Q(level="County") |
                                    Q(level="Scouts"))
    elif user_level == 'SubCounty':
        return Rank.objects.exclude(Q(level="National") |
                                    Q(level="Regional") |
                                    Q(level="County") |
                                    Q(level="SubCounty") |
                                    Q(level="Scouts"))
    elif user_level == 'Unit':
        return Rank.objects.exclude(Q(level="National") |
                                    Q(level="Regional") |
                                    Q(level="County") |
                                    Q(level="SubCounty") |
                                    Q(level="Zonal") |
                                    Q(level="Scouts"))
    else:
        return Rank.objects.none()


class EventFilterNational(django_filters.FilterSet):
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')
    region = django_filters.ModelChoiceFilter(field_name='sub_county__county__region', queryset=region_queryset,
                                              widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='sub_county__county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select,
                                                  label='SubCounty')


class EventFilterRegion(django_filters.FilterSet):
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')
    county = django_filters.ModelChoiceFilter(field_name='sub_county__county', queryset=county_queryset,
                                              widget=forms.Select, label='County')
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select,
                                                  label='SubCounty')


class EventFilterCounty(django_filters.FilterSet):
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')
    sub_county = django_filters.ModelChoiceFilter(queryset=sub_county_queryset, widget=forms.Select,
                                                  label='SubCounty')


class EventFilterSubCounty(django_filters.FilterSet):
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')


class EventFilterNational2(django_filters.FilterSet):
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')
    region = django_filters.ModelChoiceFilter(field_name='county__region', queryset=region_queryset,
                                              widget=forms.Select, label='Region')
    county = django_filters.ModelChoiceFilter(field_name='county', queryset=county_queryset,
                                              widget=forms.Select, label='County')


class EventFilterRegion2(django_filters.FilterSet):
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')


class EventFilterCounty2(django_filters.FilterSet):
    start_date = django_filters.DateRangeFilter(field_name='start_date')
    venue_name = django_filters.CharFilter(lookup_expr='icontains')
    region = django_filters.ModelChoiceFilter(field_name='county__region', queryset=region_queryset,
                                              widget=forms.Select, label='Region')
