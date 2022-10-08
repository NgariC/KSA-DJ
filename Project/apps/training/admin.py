import sys

import pandas as pd
from django import forms
from django.contrib import admin
from django.db.models import Count, Q
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin

from apps.core.project_requirements.admins import auto_admin_site, stats_admin_site
from apps.core.project_requirements.utilities import Permi, payments, List, event_chart, event_table, Perm
from apps.training.certs import itc_cert, itc_report, ptc_cert, ptc_report, wbii_cert, wbii_report, alt_cert, \
    alt_report, lt_cert, lt_report

from apps.training.models import LT, ALT, WBI, WBII, WBIII, PTC, ITC, SLSpecialEvent
from apps.training.stats import ITCStats, PTCStats, WBIStats, WBIIStats, WBIIIStats, ALTStats, LTStats, \
    SLSpecialEventStats


from apps.training.resources import ITCResource, PTCResource, WBIResource, WBIIResource, WBIIIResource, \
    ALTResource, LTResource, SLSpecialEventResource

SubCountyFieldset1 = (
                ("Event's participants", {
                    'fields': ('course_director', 'support_staff', 'participants')
                }),
                ('Dates', {
                    'classes': ('wide',),
                    'fields': (('start_date', 'end_date'),)
                }),
                ('Report', {
                    'classes': ('wide',),
                    'fields': ('report',)
                }),
                ("Participant's Lists", {
                    'fields': (('participants_list', 'director', 'staff_list'),)
                }),
                ('Payments', {
                    'classes': ('wide',),
                    'fields': ('payments',)
                }),
                ('Venues', {
                    'classes': ('wide',),
                    'fields': (('sub_county', 'venue_name'), 'venue')
                }),
            )

SubCountyFieldset2 = (
                ("Event's participants", {
                    'fields': ('course_director', 'support_staff', 'participants')
                }),
                ('Dates', {
                    'classes': ('wide',),
                    'fields': (('start_date', 'end_date'),)
                }),
                ('Report', {
                    'classes': ('wide',),
                    'fields': ('report',)
                }),
                ("Participant's Lists", {
                    'fields': (('trainees', 'director', 'staff'),)
                }),
                ('Payments', {
                    'classes': ('wide',),
                    'fields': ('payments',)
                }),
                ('Venues', {
                    'classes': ('wide',),
                    'fields': (('sub_county', 'venue_name'), 'venue')
                }),
            )

CountyFieldset1 = (
                ("", {
                    'fields': ('number',)
                }),
                ("Event's participants", {
                    'fields': ('course_director', 'support_staff', 'participants')
                }),
                ('Dates', {
                    'classes': ('wide',),
                    'fields': (('start_date', 'end_date'),)
                }),
                ('Report', {
                    'classes': ('wide',),
                    'fields': ('report',)
                }),
                ("Participant's Lists", {
                    'fields': (('participants_list', 'director', 'staff_list'),)
                }),
                ('Payments', {
                    'classes': ('wide',),
                    'fields': ('payments',)
                }),
                ('Venues', {
                    'classes': ('wide',),
                    'fields': (('county', 'venue_name'), 'venue')
                }),
            )

CountyFieldset2 = (
                ("", {
                    'fields': ('number',)
                }),
                ("Event's participants", {
                    'fields': ('course_director', 'support_staff', 'participants')
                }),
                ('Dates', {
                    'classes': ('wide',),
                    'fields': (('start_date', 'end_date'),)
                }),
                ('Report', {
                    'classes': ('wide',),
                    'fields': ('report',)
                }),
                ("Participant's Lists", {
                    'fields': (('trainees', 'director', 'staff'),)
                }),
                ('Payments', {
                    'classes': ('wide',),
                    'fields': ('payments',)
                }),
                ('Venues', {
                    'classes': ('wide',),
                    'fields': (('county', 'venue_name'), 'venue')
                }),
            )


@admin.register(ITC)
class ITCAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, itc_cert, itc_report)
    resource_class = ITCResource
    empty_value_display = '-empty-'
    list_display = ('venue_name', 'sub_county', 'start_date', 'end_date', 'no_of_participants')
    list_filter = ('course_director', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')
    search_fields = ('course_director', 'sub_county__county__region', 'sub_county__county', 'sub_county')
    autocomplete_fields = ['course_director', 'sub_county', 'support_staff', 'participants', 'trainees', 'staff',
                           'director']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('training.can_verify_ITC_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['start_date'].label = 'ITC Date'
        form.base_fields['end_date'].label = 'ITC Date (Leave Blank)'
        form.base_fields['end_date'].disabled = True
        form.base_fields['end_date'].required = False
        form.base_fields['end_date'].widget = forms.DateInput()
        if not request.user.has_perm('training.can_verify_ITC_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['participants_list', 'staff_list'] if request.user.has_perm('training.can_edit_ITC_trainees') \
            else ['participants_list', 'staff_list', 'director']

    def get_fieldsets(self, request, obj=None):
        return SubCountyFieldset2 if request.user.has_perm('training.can_edit_ITC_trainees') else SubCountyFieldset1


@admin.register(PTC)
class PTCAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, ptc_cert, ptc_report)
    resource_class = PTCResource
    empty_value_display = '-empty-'
    list_display = ('venue_name', 'sub_county', 'start_date', 'end_date', 'no_of_participants')
    list_filter = ('course_director', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')
    search_fields = ('course_director', 'sub_county__county__region', 'sub_county__county', 'sub_county')
    autocomplete_fields = ['course_director', 'sub_county', 'support_staff', 'participants', 'trainees', 'staff',
                           'director']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('training.can_verify_PTC_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('training.can_verify_PTC_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['participants_list', 'staff_list'] if request.user.has_perm('training.can_edit_PTC_trainees') \
            else ['participants_list', 'staff_list', 'director']

    def get_fieldsets(self, request, obj=None):
        return SubCountyFieldset2 if request.user.has_perm('training.can_edit_PTC_trainees') else SubCountyFieldset1


@admin.register(WBII)
class WBIIAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, wbii_cert, wbii_report)
    resource_class = WBIIResource
    empty_value_display = '-empty-'
    list_display = ('venue_name', 'number', 'county', 'start_date', 'end_date', 'no_of_participants')
    list_filter = ('course_director', 'number', 'county__region', 'county')
    search_fields = ('course_director', 'number', 'county__region', 'county')
    autocomplete_fields = ['course_director', 'county', 'support_staff', 'participants', 'trainees', 'staff',
                           'director']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('training.can_verify_WoodBadge_II_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('training.can_verify_WoodBadge_II_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['participants_list', 'staff_list'] if request.user.has_perm('training.can_edit_WoodBadge_II_trainees') \
            else ['participants_list', 'staff_list', 'director']

    def get_fieldsets(self, request, obj=None):
        return CountyFieldset2 if request.user.has_perm('training.can_edit_WoodBadge_II_trainees') else CountyFieldset1


@admin.register(ALT)
class ALTAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, alt_cert, alt_report)
    resource_class = ALTResource
    empty_value_display = '-empty-'
    list_display = ('venue_name', 'number', 'county', 'start_date', 'end_date', 'no_of_participants')
    list_filter = ('course_director', 'number', 'county__region', 'county')
    search_fields = ('course_director', 'number', 'county__region', 'county')
    autocomplete_fields = ['course_director', 'county', 'support_staff', 'participants', 'trainees', 'staff',
                           'director']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('training.can_verify_ALT_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('training.can_verify_ALT_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['participants_list', 'staff_list'] if request.user.has_perm('training.can_edit_ALT_trainees') \
            else ['participants_list', 'staff_list', 'director']

    def get_fieldsets(self, request, obj=None):
        return CountyFieldset2 if request.user.has_perm('training.can_edit_ALT_trainees') else CountyFieldset1


@admin.register(LT)
class LTAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, lt_cert, lt_report)
    resource_class = LTResource
    empty_value_display = '-empty-'
    list_display = ('venue_name', 'number', 'county', 'start_date', 'end_date', 'no_of_participants')
    list_filter = ('course_director', 'number', 'county__region', 'county')
    search_fields = ('course_director', 'number', 'county__region', 'county')
    autocomplete_fields = ['course_director', 'county', 'support_staff', 'participants', 'trainees', 'staff',
                           'director']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('training.can_verify_LT_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('training.can_verify_LT_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['participants_list', 'staff_list'] if request.user.has_perm('training.can_edit_LT_trainees') \
            else ['participants_list', 'staff_list', 'director']

    def get_fieldsets(self, request, obj=None):
        return CountyFieldset2 if request.user.has_perm('training.can_edit_LT_trainees') else CountyFieldset1


@admin.register(WBI)
class WBIAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, )
    resource_class = WBIResource
    empty_value_display = '-empty-'
    list_display = ('scout_leader_name', 'marker', 'submission_date', 'marked')
    list_filter = ('marked', 'scout_leader__sub_county__county__region', 'scout_leader__sub_county__county',
                   'scout_leader__sub_county')
    search_fields = ('scout_leader_name', 'scout_leader_name__sub_county__county__region',
                     'scout_leader_name__sub_county__county', 'scout_leader_name__sub_county')
    autocomplete_fields = 'scout_leader', 'marker', 'scout_leader_name', 'marker_name'
    fieldsets = (
        ("", {
            'fields': ('scout_leader', 'theory_book')
        }),
        ('Marker & Comments', {
            'classes': ('wide',),
            'fields': (('marker', 'marked', 'comments'),)
        }),
        ("", {
            'fields': (('scout_leader_name', 'marker_name'),)
        }),
        ('Payments', {
            'classes': ('wide',),
            'fields': ('payments',)
        }),
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('training.can_verify_WoodBadge_I_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('training.can_verify_WoodBadge_I_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form


@admin.register(WBIII)
class WBIIIAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, )
    resource_class = WBIIIResource
    empty_value_display = '-empty-'
    list_display = ('scout_leader', 'unit', 'assessed', 'assessment_date')
    list_filter = ('assessed', 'unit', 'scout_leader__sub_county__county__region', 'scout_leader__sub_county__county',
                   'scout_leader__sub_county')
    search_fields = ('scout_leader', 'unit', 'scout_leader__sub_county__county', 'scout_leader__sub_county__county',
                     'scout_leader__sub_county')
    autocomplete_fields = 'scout_leader', 'unit', 'assessor', 'scout_leader_name', 'assessor_name'
    fieldsets = (
        ("", {
            'fields': (('scout_leader', 'unit'), 'venue')
        }),
        ('Assessor & Report', {
            'classes': ('wide',),
            'fields': (('assessor', 'assessed'), 'report')
        }),
        ("", {
            'fields': (('scout_leader_name', 'assessor_name'),)
        }),
        ('Payments', {
            'classes': ('wide',),
            'fields': ('payments',)
        }),
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('training.can_verify_WoodBadge_III_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('training.can_verify_WoodBadge_III_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form


@admin.register(SLSpecialEvent)
class SLSpecialEventAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, )
    resource_class = SLSpecialEventResource
    empty_value_display = '-empty-'
    list_display = ('venue_name', 'sub_county', 'start_date', 'end_date', 'no_of_participants')
    list_filter = ('course_director', 'sub_county__county__region', 'sub_county__county', 'sub_county')
    search_fields = ('course_director', 'sub_county__county__region', 'sub_county__county', 'sub_county')
    autocomplete_fields = 'course_director', 'sub_county', 'support_staff', 'participants'

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('training.can_verify_SLSpecialEvent_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('training.can_verify_SLSpecialEvent_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['participants_list', 'staff_list'] \
            if request.user.has_perm('training.can_edit_SLSpecialEvent_trainees')\
            else ['participants_list', 'staff_list', 'director']

    def get_fieldsets(self, request, obj=None):
        return SubCountyFieldset2 if request.user.has_perm('training.can_edit_SLSpecialEvent_trainees') \
            else SubCountyFieldset1


class ITCStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "ITCs"

        metrics = {
            'male_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='M')),
            'female_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='F')),
            'total': Count('trainees__id', distinct=True),
        }

        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values(
                'sub_county__county__region__name').annotate(**metrics).order_by('sub_county__county__region'))
            df.rename({'sub_county__county__region__name': 'Region',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'ITCs'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'ITCs')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'ITCs')

            df = pd.DataFrame(qs.values(
                'sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name'))
            df.rename({'sub_county__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'ITCs'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'ITCs')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'ITCs')

            df = pd.DataFrame(qs.values('sub_county__name').annotate(**metrics).order_by('sub_county'))
            df.rename({'sub_county__name': 'SubCounty',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'ITCs'}, axis=1, inplace=True)
            response.context_data['chart3'] = event_chart(df, 'SubCounty', 'ITCs')
            response.context_data['dataframe3'] = event_table(df, summary_total, 'SubCounty', 'ITCs')
        return response


class PTCStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "PTCs"

        metrics = {
            'male_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='M')),
            'female_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='F')),
            'total': Count('trainees__id', distinct=True),
        }

        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values(
                'sub_county__county__region__name').annotate(**metrics).order_by('sub_county__county__region'))
            df.rename({'sub_county__county__region__name': 'Region',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'PTCs'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'PTCs')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'PTCs')

            df = pd.DataFrame(qs.values(
                'sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name'))
            df.rename({'sub_county__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'PTCs'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'PTCs')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'PTCs')

            df = pd.DataFrame(qs.values('sub_county__name').annotate(**metrics).order_by('sub_county'))
            df.rename({'sub_county__name': 'SubCounty',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'PTCs'}, axis=1, inplace=True)
            response.context_data['chart3'] = event_chart(df, 'SubCounty', 'PTCs')
            response.context_data['dataframe3'] = event_table(df, summary_total, 'SubCounty', 'PTCs')
        return response


class WBIStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/wbi.html'
    list_filter = ('marked', 'scout_leader__sub_county__county__region', 'scout_leader__sub_county__county',
                   'scout_leader__sub_county')


class WBIIStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('county__region', 'county', 'start_date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "WoodBadge II (Courses)"

        metrics = {
            'male_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='M')),
            'female_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='F')),
            'total': Count('trainees__id', distinct=True),
        }

        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values(
                'county__region__name').annotate(**metrics).order_by('county__region'))
            df.rename({'county__region__name': 'Region',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'WBIIs'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'WBIIs')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'WBIIs')

            df = pd.DataFrame(qs.values(
                'county__name').annotate(**metrics).order_by('county__name'))
            df.rename({'county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'WBIIs'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'WBIIs')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'WBIIs')
        return response


class WBIIIStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/wbiii.html'
    list_filter = ('assessed', 'unit', 'scout_leader__sub_county__county__region', 'scout_leader__sub_county__county',
                   'scout_leader__sub_county')


class ALTStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('county__region', 'county', 'start_date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "ALTs"

        metrics = {
            'male_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='M')),
            'female_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='F')),
            'total': Count('trainees__id', distinct=True),
        }

        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values(
                'county__region__name').annotate(**metrics).order_by('county__region'))
            df.rename({'county__region__name': 'Region',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'ALTs'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'ALTs')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'ALTs')

            df = pd.DataFrame(qs.values(
                'county__name').annotate(**metrics).order_by('county__name'))
            df.rename({'county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'ALTs'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'ALTs')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'ALTs')
        return response


class LTStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('county__region', 'county', 'start_date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "LTs"

        metrics = {
            'male_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='M')),
            'female_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='F')),
            'total': Count('trainees__id', distinct=True),
        }

        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values(
                'county__region__name').annotate(**metrics).order_by('county__region'))
            df.rename({'county__region__name': 'Region',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'LTs'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'LTs')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'LTs')

            df = pd.DataFrame(qs.values(
                'county__name').annotate(**metrics).order_by('county__name'))
            df.rename({'county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'LTs'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'LTs')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'LTs')
        return response


class SLSpecialEventStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "Scout Leader's Special Events"

        metrics = {
            'male_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='M')),
            'female_total': Count('trainees__id', distinct=True, filter=Q(trainees__gender__exact='F')),
            'total': Count('trainees__id', distinct=True),
        }

        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values(
                'sub_county__county__region__name').annotate(**metrics).order_by('sub_county__county__region'))
            df.rename({'sub_county__county__region__name': 'Region',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'SLSEs'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'SLSEs')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'SLSEs')

            df = pd.DataFrame(qs.values(
                'sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name'))
            df.rename({'sub_county__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'SLSEs'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'SLSEs')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'SLSEs')

            df = pd.DataFrame(qs.values('sub_county__name').annotate(**metrics).order_by('sub_county'))
            df.rename({'sub_county__name': 'SubCounty',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'SLSEs'}, axis=1, inplace=True)
            response.context_data['chart3'] = event_chart(df, 'SubCounty', 'SLSEs')
            response.context_data['dataframe3'] = event_table(df, summary_total, 'SubCounty', 'SLSEs')
        return response


stats_admin_site.register(ITCStats, ITCStatsAdmin)
stats_admin_site.register(PTCStats, PTCStatsAdmin)
stats_admin_site.register(WBIStats, WBIStatsAdmin)
stats_admin_site.register(WBIIStats, WBIIStatsAdmin)
stats_admin_site.register(WBIIIStats, WBIIIStatsAdmin)
stats_admin_site.register(ALTStats, ALTStatsAdmin)
stats_admin_site.register(LTStats, LTStatsAdmin)
stats_admin_site.register(SLSpecialEventStats, SLSpecialEventStatsAdmin)


class AutoTCAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('course_director', 'sub_county__county__region', 'sub_county__county', 'sub_county')


auto_admin_site.register(ITC, AutoTCAdmin)
auto_admin_site.register(PTC, AutoTCAdmin)
