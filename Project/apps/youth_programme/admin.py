import sys

import pandas as pd
from django.contrib import admin
from django.db.models import Count, Q
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin

from apps.core.project_requirements.admins import auto_admin_site, stats_admin_site
from apps.core.project_requirements.utilities import Perm, Permi, payments, List, event_chart, event_table
from apps.youth_programme.certs import investiture_cert, investiture_report, badge_camp_cert, badge_camp_report, \
    park_holiday_cert, park_holiday_report, plc_cert, plc_report, rm_cert, rm_report
from apps.youth_programme.models import Investiture, BadgeCamp, Badge, ParkHoliday, PLC, RM
from apps.youth_programme.resources import BadgeResource, InvestitureResource, BadgeCampResource, ParkHolidayResource, \
    PLCResource, RMResource
from apps.youth_programme.stats import InvestitureStats, BadgeCampStats, ParkHolidayStats, PLCStats, RMStats


@admin.register(Investiture)
class InvestitureAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, investiture_cert, investiture_report)
    resource_class = InvestitureResource
    empty_value_display = '-empty-'
    list_display = ('venue_name', 'start_date', 'end_date', 'sub_county', 'no_of_participants')
    list_filter = ('trainees__section', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')
    search_fields = ('start_date', 'end_date', 'sub_county__county__region', 'sub_county__county', 'sub_county')
    autocomplete_fields = ['investor', 'sub_county', 'support_staff', 'participants', 'jasiri_participants',
                           'trainees', 'staff', 'director']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('youth_programme.can_verify_Investiture_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['start_date'].label = 'Investiture Date'
        form.base_fields['support_staff'].label = 'Witnesses'
        if not request.user.has_perm('youth_programme.can_verify_Investiture_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['participants_list', 'staff_list'] if request.user.has_perm('youth_programme.can_edit_Investiture_trainees') else ['participants_list', 'staff_list', 'director']

    def get_fieldsets(self, request, obj=None):
        return (("Event's participants", {'fields': (('investor', 'support_staff'), ('participants', 'jasiri_participants'),)}), ('Dates', {'classes': ('wide',), 'fields': (('start_date',),)}), ('Report', {'classes': ('wide',), 'fields': ('report',)}), ("Participant's Lists", {'fields': (('trainees', 'director', 'staff'),)}), ('Payments', {'classes': ('wide',), 'fields': ('payments',)}), ('Venues', {'classes': ('wide',), 'fields': (('sub_county', 'venue_name'), 'venue')})) if request.user.has_perm('youth_programme.can_edit_Investiture_trainees') else (("Event's participants", {'fields': (('investor', 'support_staff'), ('participants', 'jasiri_participants'),)}), ('Dates', {'classes': ('wide',), 'fields': (('start_date',),)}), ('Report', {'classes': ('wide',), 'fields': ('report',)}), ("Participant's Lists", {'fields': (('participants_list', 'director', 'staff_list'),)}), ('Payments', {'classes': ('wide',), 'fields': ('payments',)}), ('Venues', {'classes': ('wide',), 'fields': (('sub_county', 'venue_name'), 'venue')}))


@admin.register(BadgeCamp)
class BadgeCampAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, badge_camp_cert, badge_camp_report)
    resource_class = BadgeCampResource
    empty_value_display = '-empty-'
    list_display = ('venue_name', 'start_date', 'end_date', 'sub_county', 'no_of_participants')
    list_filter = ('trainees__section', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')
    search_fields = ('start_date', 'end_date', 'sub_county__county__region', 'sub_county__county', 'sub_county')
    autocomplete_fields = ['examiner', 'sub_county', 'support_staff', 'nyota_i_participants', 'nyota_ii_participants',
                           'nyota_iii_participants', 'zizi_participants', 'shina_participants', 'tawi_participants',
                           'mwanzo_participants', 'mwangaza_participants', 'kilele_participants',
                           'trainees', 'staff', 'director']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('youth_programme.can_verify_BadgeCamp_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['nyota_i_participants'].required = False
        form.base_fields['nyota_ii_participants'].required = False
        form.base_fields['nyota_iii_participants'].required = False
        form.base_fields['zizi_participants'].required = False
        form.base_fields['shina_participants'].required = False
        form.base_fields['tawi_participants'].required = False
        form.base_fields['mwanzo_participants'].required = False
        form.base_fields['mwangaza_participants'].required = False
        form.base_fields['kilele_participants'].required = False
        if not request.user.has_perm('youth_programme.can_verify_BadgeCamp_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['participants_list', 'staff_list'] if request.user.has_perm('youth_programme.can_edit_BadgeCamp_trainees') else ['participants_list', 'staff_list', 'director']

    def get_fieldsets(self, request, obj=None):
        return (("Event's participants", {'fields': ('examiner', 'support_staff', ('nyota_i_participants', 'nyota_ii_participants', 'nyota_iii_participants'), ('zizi_participants', 'shina_participants', 'tawi_participants'), ('mwanzo_participants', 'mwangaza_participants', 'kilele_participants'))}), ('Dates', {'classes': ('wide',), 'fields': (('start_date', 'end_date'),)}), ('Report', {'classes': ('wide',), 'fields': ('report',)}), ("Participant's Lists", {'fields': (('trainees', 'director', 'staff'),)}), ('Payments', {'classes': ('wide',), 'fields': ('payments',)}), ('Venues', {'classes': ('wide',), 'fields': (('sub_county', 'venue_name'), 'venue')})) if request.user.has_perm('youth_programme.can_edit_BadgeCamp_trainees') else (("Event's participants", {'fields': ('examiner', 'support_staff', ('nyota_i_participants', 'nyota_ii_participants', 'nyota_iii_participants'), ('zizi_participants', 'shina_participants', 'tawi_participants'), ('mwanzo_participants', 'mwangaza_participants', 'kilele_participants'))}), ('Dates', {'classes': ('wide',), 'fields': (('start_date', 'end_date'),)}), ('Report', {'classes': ('wide',), 'fields': ('report',)}), ("Participant's Lists", {'fields': (('participants_list', 'director', 'staff_list'),)}), ('Payments', {'classes': ('wide',), 'fields': ('payments',)}), ('Venues', {'classes': ('wide',), 'fields': (('sub_county', 'venue_name'), 'venue')}))


@admin.register(ParkHoliday)
class ParkHolidayAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, park_holiday_cert, park_holiday_report)
    resource_class = ParkHolidayResource
    empty_value_display = '-empty-'
    list_display = ('venue_name', 'start_date', 'end_date', 'sub_county', 'no_of_participants')
    list_filter = ('trainees__section', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')
    search_fields = ('start_date', 'end_date', 'sub_county__county__region', 'sub_county__county', 'sub_county')
    autocomplete_fields = ['examiner', 'sub_county', 'support_staff', 'participants', 'badges', 'trainees', 'staff',
                           'director']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('youth_programme.can_verify_ParkHoliday_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('youth_programme.can_verify_ParkHoliday_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['participants_list', 'staff_list'] if request.user.has_perm('youth_programme.can_edit_ParkHoliday_trainees') else ['participants_list', 'staff_list', 'director']

    def get_fieldsets(self, request, obj=None):
        return (("Event's participants", {'fields': ('examiner', 'support_staff', 'participants')}), ('Dates', {'classes': ('wide',), 'fields': (('start_date', 'end_date'),)}), ('Report', {'classes': ('wide',), 'fields': ('report', 'badges')}), ("Participant's Lists", {'fields': (('trainees', 'director', 'staff'),)}), ('Payments', {'classes': ('wide',), 'fields': ('payments',)}), ('Venues', {'classes': ('wide',), 'fields': (('sub_county', 'venue_name'), 'venue')})) if request.user.has_perm('youth_programme.can_edit_ParkHoliday_trainees') else (("Event's participants", {'fields': ('examiner', 'support_staff', 'participants')}), ('Dates', {'classes': ('wide',), 'fields': (('start_date', 'end_date'),)}), ('Report', {'classes': ('wide',), 'fields': ('report', 'badges')}), ("Participant's Lists", {'fields': (('participants_list', 'director', 'staff_list'),)}), ('Payments', {'classes': ('wide',), 'fields': ('payments',)}), ('Venues', {'classes': ('wide',), 'fields': (('sub_county', 'venue_name'), 'venue')}))


@admin.register(PLC)
class PLCAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, plc_cert, plc_report)
    resource_class = PLCResource
    empty_value_display = '-empty-'
    list_display = ('venue_name', 'start_date', 'end_date', 'sub_county', 'no_of_participants')
    list_filter = ('trainees__section', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')
    search_fields = ('start_date', 'end_date', 'sub_county__county__region', 'sub_county__county', 'sub_county')
    autocomplete_fields = ['course_director', 'sub_county', 'support_staff', 'participants', 'trainees', 'staff',
                           'director']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('youth_programme.can_verify_PLC_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('youth_programme.can_verify_PLC_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['participants_list', 'staff_list'] if request.user.has_perm('youth_programme.can_edit_PLC_trainees') else ['participants_list', 'staff_list', 'director']

    def get_fieldsets(self, request, obj=None):
        return (("Event's participants", {'fields': ('course_director', 'support_staff', 'participants')}), ('Dates', {'classes': ('wide',), 'fields': (('start_date', 'end_date'),)}), ('Report', {'classes': ('wide',), 'fields': ('report',)}), ("Participant's Lists", {'fields': (('trainees', 'director', 'staff'),)}), ('Payments', {'classes': ('wide',), 'fields': ('payments',)}), ('Venues', {'classes': ('wide',), 'fields': (('sub_county', 'venue_name'), 'venue')})) if request.user.has_perm('youth_programme.can_edit_PLC_trainees') else (("Event's participants", {'fields': ('course_director', 'support_staff', 'participants')}), ('Dates', {'classes': ('wide',), 'fields': (('start_date', 'end_date'),)}), ('Report', {'classes': ('wide',), 'fields': ('report',)}), ("Participant's Lists", {'fields': (('participants_list', 'director', 'staff_list'),)}), ('Payments', {'classes': ('wide',), 'fields': ('payments',)}), ('Venues', {'classes': ('wide',), 'fields': (('sub_county', 'venue_name'), 'venue')}))


@admin.register(RM)
class RMAdmin(List, ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (payments, rm_cert, rm_report)
    resource_class = RMResource
    empty_value_display = '-empty-'
    list_display = ('venue_name', 'start_date', 'end_date', 'sub_county', 'no_of_participants')
    list_filter = ('trainees__section', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')
    search_fields = ('start_date', 'end_date', 'sub_county__county__region', 'sub_county__county', 'sub_county')
    autocomplete_fields = ['course_director', 'sub_county', 'support_staff', 'participants', 'trainees', 'staff',
                           'director']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('youth_programme.can_verify_Rover_Mate_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('youth_programme.can_verify_Rover_Mate_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['participants_list', 'staff_list'] if request.user.has_perm('youth_programme.can_edit_Rover_Mate_trainees') else ['participants_list', 'staff_list', 'director']

    def get_fieldsets(self, request, obj=None):
        return (("Event's participants", {'fields': ('course_director', 'support_staff', 'participants')}), ('Dates', {'classes': ('wide',), 'fields': (('start_date', 'end_date'),)}), ('Report', {'classes': ('wide',), 'fields': ('report',)}), ("Participant's Lists", {'fields': (('trainees', 'director', 'staff'),)}), ('Payments', {'classes': ('wide',), 'fields': ('payments',)}), ('Venues', {'classes': ('wide',), 'fields': (('sub_county', 'venue_name'), 'venue')})) if request.user.has_perm('youth_programme.can_edit_Rover_Mate_trainees') else (("Event's participants", {'fields': ('course_director', 'support_staff', 'participants')}), ('Dates', {'classes': ('wide',), 'fields': (('start_date', 'end_date'),)}), ('Report', {'classes': ('wide',), 'fields': ('report',)}), ("Participant's Lists", {'fields': (('participants_list', 'director', 'staff_list'),)}), ('Payments', {'classes': ('wide',), 'fields': ('payments',)}), ('Venues', {'classes': ('wide',), 'fields': (('sub_county', 'venue_name'), 'venue')}))


@admin.register(Badge)
class BadgeAdmin(Perm, ImportExportActionModelAdmin):
    resource_class = BadgeResource
    empty_value_display = '-empty-'
    list_display = ('name', 'section')
    list_filter = ('section',)
    search_fields = ('name', 'section')
    fields = ['name', 'section']


class AutoBadgeAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('name', 'section')


class AutoAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('start_date', 'end_date', 'sub_county__county__region', 'sub_county__county', 'sub_county')


auto_admin_site.register(Badge, AutoBadgeAdmin)
auto_admin_site.register(Investiture, AutoAdmin)
auto_admin_site.register(BadgeCamp, AutoAdmin)
auto_admin_site.register(PLC, AutoAdmin)
auto_admin_site.register(ParkHoliday, AutoAdmin)
auto_admin_site.register(RM, AutoAdmin)


class InvestitureStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('trainees__section', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "Investitures"

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
                       'total': 'Investitures'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'Investitures')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'Investitures')

            df = pd.DataFrame(qs.values(
                'sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name'))
            df.rename({'sub_county__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Investitures'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'Investitures')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'Investitures')

            df = pd.DataFrame(qs.values('sub_county__name').annotate(**metrics).order_by('sub_county'))
            df.rename({'sub_county__name': 'SubCounty',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Investitures'}, axis=1, inplace=True)
            response.context_data['chart3'] = event_chart(df, 'SubCounty', 'Investitures')
            response.context_data['dataframe3'] = event_table(df, summary_total, 'SubCounty', 'Investitures')
        return response


class BadgeCampStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('trainees__section', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "Badge Camps"

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
                       'total': 'Badge Camps'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'Badge Camps')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'Badge Camps')

            df = pd.DataFrame(qs.values(
                'sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name'))
            df.rename({'sub_county__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Badge Camps'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'Badge Camps')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'Badge Camps')

            df = pd.DataFrame(qs.values('sub_county__name').annotate(**metrics).order_by('sub_county'))
            df.rename({'sub_county__name': 'SubCounty',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Badge Camps'}, axis=1, inplace=True)
            response.context_data['chart3'] = event_chart(df, 'SubCounty', 'Badge Camps')
            response.context_data['dataframe3'] = event_table(df, summary_total, 'SubCounty', 'Badge Camps')
        return response


class ParkHolidayStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('trainees__section', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "ParkHolidays"

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
                       'total': 'ParkHolidays'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'ParkHolidays')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'ParkHolidays')

            df = pd.DataFrame(qs.values(
                'sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name'))
            df.rename({'sub_county__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'ParkHolidays'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'ParkHolidays')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'ParkHolidays')

            df = pd.DataFrame(qs.values('sub_county__name').annotate(**metrics).order_by('sub_county'))
            df.rename({'sub_county__name': 'SubCounty',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'ParkHolidays'}, axis=1, inplace=True)
            response.context_data['chart3'] = event_chart(df, 'SubCounty', 'ParkHolidays')
            response.context_data['dataframe3'] = event_table(df, summary_total, 'SubCounty', 'ParkHolidays')
        return response


class PLCStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('trainees__section', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "PLCs"

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
                       'total': 'PLCs'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'PLCs')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'PLCs')

            df = pd.DataFrame(qs.values(
                'sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name'))
            df.rename({'sub_county__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'PLCs'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'PLCs')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'PLCs')

            df = pd.DataFrame(qs.values('sub_county__name').annotate(**metrics).order_by('sub_county'))
            df.rename({'sub_county__name': 'SubCounty',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'PLCs'}, axis=1, inplace=True)
            response.context_data['chart3'] = event_chart(df, 'SubCounty', 'PLCs')
            response.context_data['dataframe3'] = event_table(df, summary_total, 'SubCounty', 'PLCs')
        return response


class RMStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('trainees__section', 'sub_county__county__region', 'sub_county__county', 'sub_county', 'start_date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "Rover Mates"

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
                       'total': 'Rover Mates'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'Rover Mates')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'Rover Mates')

            df = pd.DataFrame(qs.values(
                'sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name'))
            df.rename({'sub_county__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Rover Mates'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'Rover Mates')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'Rover Mates')

            df = pd.DataFrame(qs.values('sub_county__name').annotate(**metrics).order_by('sub_county'))
            df.rename({'sub_county__name': 'SubCounty',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Rover Mates'}, axis=1, inplace=True)
            response.context_data['chart3'] = event_chart(df, 'SubCounty', 'Rover Mates')
            response.context_data['dataframe3'] = event_table(df, summary_total, 'SubCounty', 'Rover Mates')
        return response


stats_admin_site.register(InvestitureStats, InvestitureStatsAdmin)
stats_admin_site.register(BadgeCampStats, BadgeCampStatsAdmin)
stats_admin_site.register(ParkHolidayStats, ParkHolidayStatsAdmin)
stats_admin_site.register(PLCStats, PLCStatsAdmin)
stats_admin_site.register(RMStats, RMStatsAdmin)
