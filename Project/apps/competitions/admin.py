import sys

import pandas as pd
from django.contrib import admin
from django.db.models import Count, Q

from apps.competitions.models import CompetitionTeam, SpecialTeamsCategories, Competition
from apps.competitions.stats import CompetitionTeamStats, CompetitionStats
from apps.core.project_requirements.admins import auto_admin_site, stats_admin_site
from apps.core.project_requirements.utilities import Perm, Permi, payments, Team, CoEvent, event_chart, event_table

TeamsFieldset1 = (
    ('', {
        'classes': ('wide',),
        'fields': (('name', 'gender'), ('unit', 'section'),)
    }),
    ("Members", {
        'fields': (('team_leaders', 'chipukizi_competitors', 'mwamba_competitors', 'jasiri_competitors'),)
    }),
    ("Special Teams Details", {
        'fields': (('special', 'special_category'),)
    }),
    ("Level of Competition", {
        'classes': ('wide',),
        'fields': ('level_of_competition',)
    }),
    ("Members Lists", {
        'fields': (('competitors_list', 'leaders_list'),)
    }),
)

TeamsFieldset2 = (
    ('', {
        'classes': ('wide',),
        'fields': (('name', 'gender'), ('unit', 'section'),)
    }),
    ("Members", {
        'fields': (('team_leaders', 'chipukizi_competitors', 'mwamba_competitors', 'jasiri_competitors'),)
    }),
    ("Special Teams Details", {
        'fields': (('special', 'special_category'),)
    }),
    ("Level of Competition", {
        'classes': ('wide',),
        'fields': ('level_of_competition',)
    }),
    ("Members Lists", {
        'fields': (('competitors', 'leaders'),)
    }),
)


@admin.register(SpecialTeamsCategories)
class SpecialTeamsCategoriesAdmin(Perm, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': ('name',)
        }),
    )


@admin.register(CompetitionTeam)
class CompetitionTeamAdmin(Team, admin.ModelAdmin):
    radio_fields = {"gender": admin.HORIZONTAL, "section": admin.HORIZONTAL, "level_of_competition": admin.HORIZONTAL}
    list_display = ('name', 'section', 'unit', 'gender', 'year', 'no_of_scout_leaders', 'no_of_scouts',
                    'level_of_competition')
    list_filter = ('year', 'section', 'gender', 'unit', 'special', 'special_category',
                   'unit__sub_county__county__region', 'unit__sub_county__county', 'unit__sub_county',
                   'level_of_competition')
    search_fields = ('name', 'unit__name', 'team_leaders__first_name', 'team_leaders__middle_name')
    autocomplete_fields = 'team_leaders', 'unit', 'chipukizi_competitors', 'mwamba_competitors', 'jasiri_competitors',\
                          'leaders', 'competitors', 'special_category'
    readonly_fields = 'competitors_list', 'leaders_list'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('competitions.can_update_competition_team_level_of_competition') and \
                'level_of_competition' in form.base_fields:
            form.base_fields['level_of_competition'].disabled = True
        return form

    def get_fieldsets(self, request, obj=None):
        return TeamsFieldset2 if request.user.has_perm('competitions.can_edit_competition_team_competitors') \
            else TeamsFieldset1


@admin.register(Competition)
class CompetitionAdmin(CoEvent, admin.ModelAdmin):
    actions = [payments]
    list_display = ('level', 'year', 'no_of_scout_leaders', 'no_of_scouts')
    list_filter = ('level', 'start_date', 'year', 'country', 'sub_county__county__region',
                   'sub_county__county', 'sub_county')
    radio_fields = {"level": admin.HORIZONTAL}
    search_fields = ('chief_assessor', 'level', 'start_date', 'end_date', 'sub_county', 'sub_county__county',
                     'sub_county__county__region', 'country')
    autocomplete_fields = ('chief_assessor', 'sub_county', 'country', 'assistant_assessors', 'chief',
                           'assessors', 'teams')
    filter_horizontal = ('competing_teams',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('competitions.can_verify_Competition_payments') and 'payments' in actions:
            del actions['payments']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('competitions.can_verify_Competition_payments') and 'payments' in form.base_fields:
            form.base_fields['payments'].disabled = True
        return form

    def get_readonly_fields(self, request, obj=None):
        return ['assessor_list', 'teams_list'] if request.user.has_perm('competitions.can_edit_Competition_teams') \
            else ['teams_list', 'assessor_list', 'chief']

    def get_fieldsets(self, request, obj=None):
        return (('Level of Competition', {'classes': ('wide',), 'fields': ('level',)}),
                ('Assessors', {'fields': (('chief_assessor', 'assistant_assessors'),)}),
                ('Participants', {'fields': (('competing_teams',),)}),
                ('Dates', {'fields': (('start_date', 'end_date'),)}),
                ('Report', {'classes': ('wide',), 'fields': ('report',)}),
                ("Participant's Lists", {'fields': (('assessors', 'chief'), 'teams')}),
                ('Payments', {'classes': ('collapse',), 'fields': ('payments',)}),
                ('Venues', {'fields': (('sub_county', 'country'), ('venue_name',), 'venue')})) \
            if request.user.has_perm('competitions.can_edit_Competition_teams') else \
            (('Level of Competition', {'classes': ('wide',), 'fields': ('level',)}),
             ('Assessors', {'fields': (('chief_assessor', 'assistant_assessors'),)}),
             ('Participants', {'fields': (('chipukizi_patrols', 'mwamba_patrols'), 'crews')}),
             ('Dates', {'fields': (('start_date', 'end_date'),)}),
             ('Report', {'classes': ('wide',), 'fields': ('report',)}),
             ("Participant's Lists", {'fields': (('chief', 'assessor_list'), 'teams_list')}),
             ('Payments', {'classes': ('collapse',), 'fields': ('payments',)}),
             ('Venues', {'fields': (('sub_county', 'country'), ('venue_name',), 'venue')}))


class AutoSpecialTeamsCategoriesAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('name',)


class AutoCompetitionTeamAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('name', 'unit__name', 'scout_leader__first_name', 'scout_leader__middle_name',
                     'gender', 'year')


auto_admin_site.register(SpecialTeamsCategories, AutoSpecialTeamsCategoriesAdmin)
auto_admin_site.register(CompetitionTeam, AutoCompetitionTeamAdmin)


class CompetitionTeamStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/teams.html'
    list_filter = ('year', 'unit', 'gender', 'special', 'special_category', 'unit__sub_county__county__region',
                   'unit__sub_county__county', 'unit__sub_county', 'level_of_competition')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'male_total': Count('id', distinct=True, filter=Q(gender__exact='M')),
            'female_total': Count('id', distinct=True, filter=Q(gender__exact='F')),
            'scout_leader_male_total': Count('leaders__id', distinct=True,
                                             filter=Q(leaders__gender__exact='M')),
            'scout_leader_female_total': Count('leaders__id', distinct=True,
                                               filter=Q(leaders__gender__exact='F')),
            'participants_male_total': Count('competitors__id', distinct=True,
                                             filter=Q(competitors__gender__exact='M')),
            'participants_female_total': Count('competitors__id', distinct=True,
                                               filter=Q(competitors__gender__exact='F')),
            'scout_leader_total': Count("leaders__id", distinct=True),
            'participants_total': Count("competitors__id", distinct=True),
            'total': Count('id', distinct=True),
        }

        response.context_data['title'] = "Competitions Teams"

        response.context_data['regions'] = list(
            qs.values('unit__sub_county__county__region__name').annotate(**metrics).order_by(
                'unit__sub_county__county__region')
        )

        response.context_data['counties'] = list(
            qs.values('unit__sub_county__county__name').annotate(**metrics).order_by(
                'unit__sub_county__county__name')
        )

        response.context_data['sub_counties'] = list(
            qs.values('unit__sub_county__name').annotate(**metrics).order_by('unit__sub_county')
        )

        response.context_data['summary_total'] = dict(qs.aggregate(**metrics))

        return response


# class CompetitionStatsAdmin(Permi, admin.ModelAdmin):
#     list_per_page = sys.maxsize
#     show_full_result_count = False
#     change_list_template = 'stats/competition.html'
#     list_filter = ('level', 'start_date', 'year', 'country', 'sub_county')
#
#     def changelist_view(self, request, extra_context=None):
#         response = super().changelist_view(request, extra_context=extra_context)
#
#         try:
#             qs = response.context_data['cl'].queryset
#         except (AttributeError, KeyError):
#             return response
#
#         metrics = {
#             'male_total': Count('competing_teams__competitors__id', distinct=True,
#                                 filter=Q(competing_teams__competitors__gender__exact='M')),
#             'female_total': Count('competing_teams__competitors__id', distinct=True,
#                                   filter=Q(competing_teams__competitors__gender__exact='F')),
#             'total': Count('competing_teams__competitors__id', distinct=True),
#         }
#
#         response.context_data['title'] = "Competitions"
#
#         response.context_data['regions'] = list(
#             qs.values('sub_county__county__region__name').annotate(**metrics).order_by('sub_county__county__region')
#         )
#
#         response.context_data['counties'] = list(
#             qs.values('sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name')
#         )
#
#         response.context_data['sub_counties'] = list(
#             qs.values('sub_county__name').annotate(**metrics).order_by('sub_county')
#         )
#
#         response.context_data['summary_total'] = dict(qs.aggregate(**metrics))
#
#         return response


class CompetitionStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/stats.html'
    list_filter = ('level', 'start_date', 'year', 'country', 'sub_county')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['title'] = "Competitions"

        metrics = {
            'male_total': Count('competing_teams__competitors__id', distinct=True,
                                filter=Q(competing_teams__competitors__gender__exact='M')),
            'female_total': Count('competing_teams__competitors__id', distinct=True,
                                  filter=Q(competing_teams__competitors__gender__exact='F')),
            'total': Count('competing_teams__competitors__id', distinct=True),
        }
        if qs.exists():
            summary_total = dict(qs.aggregate(**metrics))
            df = pd.DataFrame(qs.values(
                'sub_county__county__region__name').annotate(**metrics).order_by('sub_county__county__region'))
            df.rename({'sub_county__county__region__name': 'Region',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Competitions'}, axis=1, inplace=True)
            response.context_data['chart1'] = event_chart(df, 'Region', 'Competitions')
            response.context_data['dataframe1'] = event_table(df, summary_total, 'Region', 'Competitions')

            df = pd.DataFrame(qs.values(
                'sub_county__county__name').annotate(**metrics).order_by('sub_county__county__name'))
            df.rename({'sub_county__county__name': 'County',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Competitions'}, axis=1, inplace=True)
            response.context_data['chart2'] = event_chart(df, 'County', 'Competitions')
            response.context_data['dataframe2'] = event_table(df, summary_total, 'County', 'Competitions')

            df = pd.DataFrame(qs.values('sub_county__name').annotate(**metrics).order_by('sub_county'))
            df.rename({'sub_county__name': 'SubCounty',
                       'male_total': 'Male',
                       'female_total': 'Female',
                       'total': 'Competitions'}, axis=1, inplace=True)
            response.context_data['chart3'] = event_chart(df, 'SubCounty', 'Competitions')
            response.context_data['dataframe3'] = event_table(df, summary_total, 'SubCounty', 'Competitions')
        return response


stats_admin_site.register(CompetitionTeamStats, CompetitionTeamStatsAdmin)
stats_admin_site.register(CompetitionStats, CompetitionStatsAdmin)
