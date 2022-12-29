import sys

import pandas as pd
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from django.db.models import Count, Q
from django import forms

from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin

from apps.analytics.models import ObjectViewed
from apps.core.project_requirements.admins import auto_admin_site, stats_admin_site
from apps.core.project_requirements.utilities import Perm, Permi, years_back_3, years_back_26, years_back_27, \
    years_back_100, active
from apps.payments.models import Payments
from apps.registrations.models import Unit, Scout, ScoutLeader, ScoutLeaderCert
from apps.registrations.certs import print_cert, print_warrant
from apps.registrations.resources import ScoutLeaderResource, ScoutResource, UnitResource
from apps.registrations.utilities import unit_chart, unit_table, scouts_table, scouts_chart
from apps.registrations.stats import UnitStats, ScoutStats, ScoutLeaderStats


class ObjectViewedInline(GenericTabularInline):
    model = ObjectViewed

class PaymentsInline(GenericTabularInline):
    model = Payments


class ScoutLeaderCertInline(admin.TabularInline):
    model = ScoutLeaderCert
    extra = 1
    fields = ['name', 'code']


@admin.register(Unit)
class UnitAdmin(Perm, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (active, print_cert, print_warrant)
    resource_class = UnitResource
    list_per_page = 100
    list_display = 'name', 'code', 'sections'
    search_fields = ('name', 'sections', 'sponsoring_authority', 'sub_county__name', 'sub_county__county__name')
    list_filter = ('active', 'date_warranted', 'sections', 'sub_county__county__region', 'sub_county__county',
                   'sub_county')
    autocomplete_fields = ['sub_county']
    readonly_fields = ['date_warranted', 'unique_code']
    fieldsets = (
        ('Unit info', {
            'fields': (('name', 'sponsoring_authority'), 'sub_county', 'sections')
        }),
        ('Verification', {
            'classes': ('wide',),
            'fields': ('active',)
        }),
        ('Other Details Saved Automatically', {
            'classes': ('collapse',),
            'fields': (('date_warranted', 'unique_code'),)
        }),
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('registrations.can_verify_units') and 'active' in actions:
            del actions['active']
        if not request.user.has_perm('registrations.can_print_units_certs'):
            if 'print_cert' in actions:
                del actions['print_cert']
            if 'print_warrant' in actions:
                del actions['print_warrant']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('registrations.can_verify_units') and 'active' in form.base_fields:
            form.base_fields['active'].disabled = True
        return form


@admin.register(Scout)
class ScoutAdmin(Perm, ImportExportActionModelAdmin):
    formfield_overrides = {
        models.DateField: {'widget': forms.SelectDateWidget(years=range(years_back_27, years_back_3), )},
    }

    def get_changeform_initial_data(self, request):
        return {'phone_number': '07'}

    actions = ExportActionModelAdmin.actions + (active,)
    resource_class = ScoutResource
    list_per_page = 100
    radio_fields = {"gender": admin.HORIZONTAL, "section": admin.HORIZONTAL}
    list_display = ('get_full_name', 'unit', 'code', 'section', 'phone_number', 'email')
    list_filter = (
        'active', 'registration_date', 'gender', 'investiture', 'jasiri_investiture', 'section', 'link_badge_award',
        'chui_badge_award', 'simba_badge_award', 'csa_award', 'unit', 'unit__sub_county__county__region',
        'unit__sub_county__county', 'unit__sub_county')
    search_fields = ('first_name', 'middle_name', 'surname', 'unit__name', 'unit__id', 'section', 'national_id',
                     'unit__sub_county__name', 'unit__sub_county__county__name')
    autocomplete_fields = 'unit',
    readonly_fields = ["registration_date", 'unique_code', 'code', 'sub_county', 'profile_image']
    fieldsets = (
        ('Personal info', {
            'fields': (('first_name', 'middle_name'), ('surname', 'gender'), ('date_of_birth', 'image'),)
        }),
        ('More Information (Jasiri Scout Only)', {
            'fields': (('national_id', 'email', 'phone_number'),)
        }),
        ('Unit details', {
            'fields': ('unit', 'section')
        }),
        ('Trainings Level', {
            'classes': ('wide',),
            'fields': (('investiture', 'jasiri_investiture'),
                       ('nyota_i', 'nyota_ii', 'nyota_iii', 'link_badge_award'),
                       ('zizi', 'shina', 'tawi', 'chui_badge_award'),
                       ('mwanzo', 'mwangaza', 'kilele', 'simba_badge_award'),
                       'csa_award',)
        }),
        ('Verification', {
            'classes': ('wide',),
            'fields': ('active',)
        }),
        ('Other Details Saved Automatically', {
            'classes': ('collapse',),
            'fields': (("registration_date", 'unique_code', 'code', 'sub_county'), 'profile_image')
        }),
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('registrations.can_verify_scouts') and 'active' in actions:
            del actions['active']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('registrations.can_verify_scouts') and 'active' in form.base_fields:
            form.base_fields['active'].disabled = True
        return form


@admin.register(ScoutLeader)
class ScoutLeaderAdmin(Perm, ImportExportActionModelAdmin):
    formfield_overrides = {
        models.DateField: {'widget': forms.SelectDateWidget(years=range(years_back_100, years_back_26), )},
    }

    def get_changeform_initial_data(self, request):
        return {'phone_number': '07'}

    actions = ExportActionModelAdmin.actions + (active,)
    resource_class = ScoutLeaderResource
    inlines = [ScoutLeaderCertInline]
    list_per_page = 100
    list_display = ('get_full_name', 'unit', 'code', 'phone_number', 'email')
    list_filter = ('active', 'life_member', 'registration_date', 'gender', 'rank', 'training', 'unit',
                   'sub_county__county__region', 'sub_county__county', 'sub_county')
    search_fields = ('first_name', 'middle_name', 'surname', 'unit__name', 'unit__id', 'national_id', 'training',
                     'sub_county__name', 'sub_county__county__name')
    autocomplete_fields = ['unit', 'sub_county', 'rank']
    radio_fields = {"gender": admin.HORIZONTAL, "training": admin.HORIZONTAL}
    readonly_fields = ["registration_date", 'unique_code', 'code', 'office', 'profile_image']
    fieldsets = (
        ('Personal info', {
            'classes': ('wide',),
            'fields': (('first_name', 'middle_name'), 'surname',
                       ('gender', 'date_of_birth'),
                       ('national_id', 'tsc_number'), 'image')
        }),
        ('Contact Information', {
            'classes': ('wide',),
            'fields': (('email', 'phone_number'), 'sub_county')
        }),
        ('Unit & Rank details', {
            'fields': (('unit', 'rank'),)
        }),
        ('Verification and Renewal', {
            'classes': ('wide',),
            'fields': ('active', 'life_member')
        }),
        ('Level of training by awards', {
            'classes': ('wide',),
            'fields': ('training',)
        }),
        ('Other Details Saved Automatically', {
            'classes': ('collapse',),
            'fields': (("registration_date", 'unique_code', 'code', 'office'), 'profile_image')
        }),
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('registrations.can_verify_scout_leaders') and 'active' in actions:
            del actions['active']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('registrations.can_verify_scout_leaders') and 'active' in form.base_fields:
            form.base_fields['active'].disabled = True
        return form


class AutoUnitAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    ordering = ('name', )
    search_fields = ('id', 'name', 'sections', 'sponsoring_authority', 'sub_county__name', 'sub_county__county__name')


class AutoScoutAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    ordering = ('first_name', )
    search_fields = ('first_name', 'middle_name', 'surname', 'section', 'unit__name', 'unit__id',
                     'unit__sub_county__name', 'unit__sub_county__county__name')


class AutoScoutLeaderAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    ordering = ('first_name', )
    search_fields = (
        'first_name', 'middle_name', 'surname', 'unit__name', 'unit__id', 'national_id', 'training',
        'sub_county__name', 'sub_county__county__name')


auto_admin_site.register(Unit, AutoUnitAdmin)
auto_admin_site.register(Scout, AutoScoutAdmin)
auto_admin_site.register(ScoutLeader, AutoScoutLeaderAdmin)


class UnitStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('active', 'date_warranted', 'sub_county__county__region', 'sub_county__county', 'sub_county')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = 'Units'

        metrics = {
            'sungura_total': Count('id', distinct=True, filter=Q(sections__icontains='Sungura')),
            'chipukizi_total': Count('id', distinct=True, filter=Q(sections__icontains='Chipukizi')),
            'mwamba_total': Count('id', distinct=True, filter=Q(sections__icontains='Mwamba')),
            'jasiri_total': Count('id', distinct=True, filter=Q(sections__icontains='Jasiri')),
            'total': Count('id', distinct=True),
        }

        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values(
                'sub_county__county__region__name').annotate(**metrics).order_by('sub_county__county__region'))
            df.rename({'sub_county__county__region__name': 'Region',
                       'sungura_total': 'Sungura',
                       'chipukizi_total': 'Chipukizi',
                       'mwamba_total': 'Mwamba',
                       'jasiri_total': 'Jasiri',
                       'total': 'Units'}, axis=1, inplace=True)
            response.context_data['chart1'] = unit_chart(df, 'Region', 'Units')
            response.context_data['dataframe1'] = unit_table(df, summary_total, 'Region', 'Units')

            df = pd.DataFrame(qs.values(
                'sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name'))
            df.rename({'sub_county__county__name': 'County',
                       'sungura_total': 'Sungura',
                       'chipukizi_total': 'Chipukizi',
                       'mwamba_total': 'Mwamba',
                       'jasiri_total': 'Jasiri',
                       'total': 'Units'}, axis=1, inplace=True)
            response.context_data['chart2'] = unit_chart(df, 'County', 'Units')
            response.context_data['dataframe2'] = unit_table(df, summary_total, 'County', 'Units')

            df = pd.DataFrame(qs.values('sub_county__name').annotate(**metrics).order_by('sub_county'))
            df.rename({'sub_county__name': 'SubCounty',
                       'sungura_total': 'Sungura',
                       'chipukizi_total': 'Chipukizi',
                       'mwamba_total': 'Mwamba',
                       'jasiri_total': 'Jasiri',
                       'total': 'Units'}, axis=1, inplace=True)
            response.context_data['chart3'] = unit_chart(df, 'SubCounty', 'Units')
            response.context_data['dataframe3'] = unit_table(df, summary_total, 'SubCounty', 'Units')
        return response


class ScoutStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = (
        'active', 'registration_date', 'gender', 'investiture', 'jasiri_investiture', 'section', 'link_badge_award',
        'chui_badge_award', 'simba_badge_award', 'csa_award', 'unit', 'unit__sub_county__county__region',
        'unit__sub_county__county', 'unit__sub_county')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = 'Scouts'

        metrics = {
            'male_total': Count('id', distinct=True, filter=Q(gender__exact='M')),
            'female_total': Count('id', distinct=True, filter=Q(gender__exact='F')),
            'total': Count('id', distinct=True),
        }

        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values(
                'unit__sub_county__county__region__name').annotate(**metrics).order_by(
                'unit__sub_county__county__region'))
            df.rename({'unit__sub_county__county__region__name': 'Region',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Scouts'}, axis=1, inplace=True)
            response.context_data['chart1'] = scouts_chart(df, 'Region', 'Scouts')
            response.context_data['dataframe1'] = scouts_table(df, summary_total, 'Region', 'Scouts')

            df = pd.DataFrame(qs.values(
                'unit__sub_county__county__name').annotate(**metrics).order_by('unit__sub_county__county__code'))
            df.rename({'unit__sub_county__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Scouts'}, axis=1, inplace=True)
            response.context_data['chart2'] = scouts_chart(df, 'County', 'Scouts')
            response.context_data['dataframe2'] = scouts_table(df, summary_total, 'County', 'Scouts')

            df = pd.DataFrame(qs.values('unit__sub_county__name').annotate(**metrics).order_by('unit__sub_county'))
            df.rename({'unit__sub_county__name': 'SubCounty',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Scouts'}, axis=1, inplace=True)
            response.context_data['chart3'] = scouts_chart(df, 'SubCounty', 'Scouts')
            response.context_data['dataframe3'] = scouts_table(df, summary_total, 'SubCounty', 'Scouts')
        return response


class ScoutLeaderStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('active', 'life_member', 'registration_date', 'gender', 'rank', 'training', 'unit',
                   'sub_county__county__region', 'sub_county__county', 'sub_county')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = 'Scout leaders'

        metrics = {
            'male_total': Count('id', distinct=True, filter=Q(gender__exact='M')),
            'female_total': Count('id', distinct=True, filter=Q(gender__exact='F')),
            'total': Count('id', distinct=True),
        }

        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values(
                'sub_county__county__region__name').annotate(**metrics).order_by('sub_county__county__region'))
            df.rename({'sub_county__county__region__name': 'Region',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Scout Leaders'}, axis=1, inplace=True)
            response.context_data['chart1'] = scouts_chart(df, 'Region', 'Scout Leaders')
            response.context_data['dataframe1'] = scouts_table(df, summary_total, 'Region', 'Scout Leaders')

            df = pd.DataFrame(qs.values(
                'sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name'))
            df.rename({'sub_county__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Scout Leaders'}, axis=1, inplace=True)
            response.context_data['chart2'] = scouts_chart(df, 'County', 'Scout Leaders')
            response.context_data['dataframe2'] = scouts_table(df, summary_total, 'County', 'Scout Leaders')

            df = pd.DataFrame(qs.values('sub_county__name').annotate(**metrics).order_by('sub_county'))
            df.rename({'sub_county__name': 'SubCounty',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Scout Leaders'}, axis=1, inplace=True)
            response.context_data['chart3'] = scouts_chart(df, 'SubCounty', 'Scout Leaders')
            response.context_data['dataframe3'] = scouts_table(df, summary_total, 'SubCounty', 'Scout Leaders')
        return response


stats_admin_site.register(UnitStats, UnitStatsAdmin)
stats_admin_site.register(ScoutStats, ScoutStatsAdmin)
stats_admin_site.register(ScoutLeaderStats, ScoutLeaderStatsAdmin)
