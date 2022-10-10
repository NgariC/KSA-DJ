from apps.competitions.models import CompetitionTeam, Competition
from apps.core.project_requirements.access import SubCountyMemberQueryset, UnitMemberQueryset, FilterSetClass


class TeamsList(FilterSetClass, UnitMemberQueryset):
    model = CompetitionTeam
    context_object_name = 'teams'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural}"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Name', 'Section', 'Unit', 'County/SubCounty']
        return ctx


class CompetitionList(FilterSetClass, SubCountyMemberQueryset):
    model = Competition
    context_object_name = 'competitions'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural} Events"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Venue', 'Chief Assessor', 'Start Date']
        return ctx
