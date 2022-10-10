from apps.core.project_requirements.access import UnitMemberQueryset, UnitSubCountyMemberQueryset, FilterSetClass
from apps.registrations.models import Unit, Scout, ScoutLeader


class UnitList(FilterSetClass, UnitSubCountyMemberQueryset):
    model = Unit
    paginate_by = 100
    context_object_name = 'units'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['app_name'] = f"{opts.app_label}/{opts.model_name}_filter"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = "Registered Units"
        ctx['no_table'] = "There are no registered units within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Name', 'Code', 'SubCounty']
        return ctx


class ScoutList(FilterSetClass, UnitMemberQueryset):
    model = Scout
    paginate_by = 100
    context_object_name = 'scouts'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = "Registered Units"
        ctx['no_table'] = "There are no registered Scouts within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Name', 'Code', 'SubCounty']
        return ctx


class ScoutLeaderList(FilterSetClass, UnitSubCountyMemberQueryset):
    model = ScoutLeader
    paginate_by = 100
    context_object_name = 'scout_leaders'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = "Registered Units"
        ctx['no_table'] = "There are no registered Scout Leaders within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Name', 'Code', 'SubCounty']
        return ctx
