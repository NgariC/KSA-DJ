import sys

import pandas as pd
from django.contrib import admin
from django.db.models import Count, Q

from apps.celebrations.models import Founderee, LinkBadgeAward, ChuiBadgeAward, SimbaBadgeAward, ChiefScoutAward, \
    ScoutLeaderAward, CountyParticipants, PatronsDay, TwoBeadsAward, ThreeBeadsAward, FourBeadsAward
from apps.celebrations.stats import FoundereeStats, PatronsDayStats
from apps.core.project_requirements.admins import stats_admin_site
from apps.core.project_requirements.utilities import Permi, Staff, ScoutsAward, ScoutLeadersAward, AwardEvent, \
    AwardAttendees, event_chart, event_table


@admin.register(Founderee)
class FoundereeAdmin(Staff, admin.ModelAdmin):
    show_full_result_count = False
    list_display = ('county', 'start_date', 'end_date', 'camp_chief', 'no_of_staff')
    list_filter = ('camp_chief', 'county')
    search_fields = ('county', 'start_date', 'end_date')
    autocomplete_fields = 'camp_chief', 'county', 'support_staff'
    fields = ['camp_chief', 'support_staff', ('start_date', 'end_date'), 'report', 'county', 'venue_name', 'venue']


@admin.register(LinkBadgeAward)
class LinkBadgeAwardAdmin(ScoutsAward, admin.ModelAdmin):
    list_display = ('year', 'no_of_scouts')
    list_filter = ('year', 'sungura_scouts__unit__sub_county__county__region',
                   'sungura_scouts__unit__sub_county__county', 'sungura_scouts__unit__sub_county')
    search_fields = ('year', 'sungura_scouts__first_name', 'sungura_scouts__middle_name')
    # autocomplete_fields = 'sungura_scouts',
    filter_horizontal = ('sungura_scouts',)
    readonly_fields = ['awardees_list']
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': ('award_date', 'sungura_scouts')
        }),
        ('Awardees', {
            'classes': ('collapse',),
            'fields': ('awardees_list',)
        }),
    )


@admin.register(ChuiBadgeAward)
class ChuiBadgeAwardAdmin(ScoutsAward, admin.ModelAdmin):
    list_display = ('year', 'no_of_scouts')
    list_filter = ('year', 'chipukizi_scouts__unit__sub_county__county__region',
                   'chipukizi_scouts__unit__sub_county__county', 'chipukizi_scouts__unit__sub_county')
    search_fields = ('year', 'chipukizi_scouts__first_name', 'chipukizi_scouts__middle_name')
    # autocomplete_fields = 'chipukizi_scouts',
    filter_horizontal = ('chipukizi_scouts',)
    readonly_fields = ['awardees_list']
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': ('award_date', 'chipukizi_scouts')
        }),
        ('Awardees', {
            'classes': ('collapse',),
            'fields': ('awardees_list',)
        }),
    )


@admin.register(SimbaBadgeAward)
class SimbaBadgeAwardAdmin(ScoutsAward, admin.ModelAdmin):
    list_display = ('year', 'no_of_scouts')
    list_filter = ('year', 'mwamba_scouts__unit__sub_county__county__region',
                   'mwamba_scouts__unit__sub_county__county', 'mwamba_scouts__unit__sub_county')
    search_fields = ('year', 'mwamba_scouts__first_name', 'mwamba_scouts__middle_name')
    # autocomplete_fields = 'mwamba_scouts',
    filter_horizontal = ('mwamba_scouts',)
    readonly_fields = ['awardees_list']
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': ('award_date', 'mwamba_scouts')
        }),
        ('Awardees', {
            'classes': ('collapse',),
            'fields': ('awardees_list',)
        }),
    )


@admin.register(ChiefScoutAward)
class ChiefScoutAwardAdmin(ScoutsAward, admin.ModelAdmin):
    list_display = ('year', 'no_of_scouts')
    list_filter = ('year', 'jasiri_scouts__unit__sub_county__county__region',
                   'jasiri_scouts__unit__sub_county__county', 'jasiri_scouts__unit__sub_county')
    search_fields = ('year', 'jasiri_scouts__first_name', 'jasiri_scouts__middle_name')
    # autocomplete_fields = 'jasiri_scouts',
    filter_horizontal = ('jasiri_scouts',)
    readonly_fields = ['awardees_list']
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': ('award_date', 'jasiri_scouts')
        }),
        ('Awardees', {
            'classes': ('collapse',),
            'fields': ('awardees_list',)
        }),
    )


@admin.register(ScoutLeaderAward)
class ScoutLeaderAwardAdmin(ScoutLeadersAward, admin.ModelAdmin):
    list_display = ('name', 'year', 'no_of_scout_leaders')
    list_filter = ('year', 'scout_leaders__sub_county__county__region',
                   'scout_leaders__sub_county__county', 'scout_leaders__sub_county')
    search_fields = ('name', 'year', 'scout_leaders__first_name', 'scout_leaders__middle_name')
    # autocomplete_fields = 'scout_leaders',
    filter_horizontal = ('scout_leaders',)
    readonly_fields = ['awardees_list']
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': ('award_date', 'name', 'scout_leaders')
        }),
        ('Awardees', {
            'classes': ('collapse',),
            'fields': ('awardees_list',)
        }),
    )


@admin.register(TwoBeadsAward)
class TwoBeadsAwardAdmin(ScoutLeadersAward, admin.ModelAdmin):
    list_display = ('year', 'no_of_scout_leaders')
    list_filter = ('year', 'scout_leaders__sub_county__county__region',
                   'scout_leaders__sub_county__county', 'scout_leaders__sub_county')
    search_fields = ('year', 'scout_leaders__first_name', 'scout_leaders__middle_name')
    # autocomplete_fields = 'scout_leaders',
    filter_horizontal = ('scout_leaders',)
    readonly_fields = ['awardees_list']
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': ('award_date', 'scout_leaders')
        }),
        ('Awardees', {
            'classes': ('collapse',),
            'fields': ('awardees_list',)
        }),
    )


@admin.register(ThreeBeadsAward)
class ThreeBeadsAwardAdmin(ScoutLeadersAward, admin.ModelAdmin):
    list_display = ('year', 'no_of_scout_leaders')
    list_filter = ('year', 'scout_leaders__sub_county__county__region',
                   'scout_leaders__sub_county__county', 'scout_leaders__sub_county')
    search_fields = ('year', 'scout_leaders__first_name', 'scout_leaders__middle_name')
    # autocomplete_fields = 'scout_leaders',
    filter_horizontal = ('scout_leaders',)
    readonly_fields = ['awardees_list']
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': ('award_date', 'scout_leaders')
        }),
        ('Awardees', {
            'classes': ('collapse',),
            'fields': ('awardees_list',)
        }),
    )


@admin.register(FourBeadsAward)
class FourBeadsAwardAdmin(ScoutLeadersAward, admin.ModelAdmin):
    list_display = ('year', 'no_of_scout_leaders')
    list_filter = ('year', 'scout_leaders__sub_county__county__region',
                   'scout_leaders__sub_county__county', 'scout_leaders__sub_county')
    search_fields = ('year', 'scout_leaders__first_name', 'scout_leaders__middle_name')
    # autocomplete_fields = 'scout_leaders',
    filter_horizontal = ('scout_leaders',)
    readonly_fields = ['awardees_list']
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': ('award_date', 'scout_leaders')
        }),
        ('Awardees', {
            'classes': ('collapse',),
            'fields': ('awardees_list',)
        }),
    )


@admin.register(CountyParticipants)
class CountyParticipantsAdmin(AwardEvent, admin.ModelAdmin):
    list_display = ('county', 'year', 'no_of_sungura_scouts', 'no_of_chipukizi_scouts', 'no_of_mwamba_scouts',
                    'no_of_jasiri_scouts', 'no_of_scout_leaders')
    list_filter = ('year', 'county__region', 'county')
    search_fields = ('name', 'year', 'county__region', 'county')
    autocomplete_fields = ['county', 'sungura_scouts', 'chipukizi_scouts', 'mwamba_scouts',
                           'jasiri_scouts', 'scout_leaders']
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': ('county', 'sungura_scouts', 'chipukizi_scouts', 'mwamba_scouts',
                       'jasiri_scouts', 'scout_leaders')
        }),
    )


@admin.register(PatronsDay)
class PatronsDayAdmin(AwardEvent, AwardAttendees, admin.ModelAdmin):
    filter_horizontal = ('sungura_awards', 'chipukizi_awards', 'mwamba_awards',
                         'jasiri_awards', 'scout_leaders_awards', 'county_participants')
    list_display = ('year', 'no_of_sungura_scouts', 'no_of_chipukizi_scouts', 'no_of_mwamba_scouts',
                    'no_of_jasiri_scouts', 'no_of_scout_leaders', 'scouts', 'scout_leaders')
    list_filter = ('year',)
    search_fields = ('year',)
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': ('date', 'sungura_awards', 'chipukizi_awards', 'mwamba_awards',
                       'jasiri_awards', 'scout_leaders_awards', 'county_participants')
        }),
    )


class FoundereeStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('county__region', 'county')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = 'Founderee'

        metrics = {
            'male_total': Count('support_staff__id', distinct=True, filter=Q(support_staff__gender__exact='M')),
            'female_total': Count('support_staff__id', distinct=True, filter=Q(support_staff__gender__exact='F')),
            'total': Count('support_staff__id', distinct=True),
        }

        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values(
                'county__region__name').annotate(**metrics).order_by('county__region'))
            df.rename({'county__region__name': 'Region',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Founderee'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'Founderee')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'Founderee')

            df = pd.DataFrame(qs.values(
                'county__name').annotate(**metrics).order_by('county__name'))
            df.rename({'county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Founderee'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'Founderee')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'Founderee')
        return response


class PatronsDayStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('year', )

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = 'Patrons Day'

        metrics = {
            'male_total': Count('county_participants__scouts_attendees__id', distinct=True, filter=Q(
                county_participants__scouts_attendees__gender__exact='M')),
            'female_total': Count('county_participants__scouts_attendees__id', distinct=True, filter=Q(
                county_participants__scouts_attendees__gender__exact='F')),
            'total': Count('county_participants__scouts_attendees__id', distinct=True),
        }

        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values('county_participants__county__region__name').annotate(**metrics).order_by(
                'county_participants__county__region'))
            df.rename({'county_participants__county__region__name': 'Region',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Patrons Day'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'Patrons Day')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'Patrons Day')

            df = pd.DataFrame(qs.values(
                'county_participants__county__name').annotate(**metrics).order_by('county_participants__county__name'))
            df.rename({'county_participants__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Patrons Day'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'Patrons Day')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'Patrons Day')
        return response


stats_admin_site.register(FoundereeStats, FoundereeStatsAdmin)
stats_admin_site.register(PatronsDayStats, PatronsDayStatsAdmin)
