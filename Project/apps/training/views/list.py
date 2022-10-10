from apps.core.project_requirements.access import SubCountyMemberQueryset, CountyMemberQueryset, StaffMemberQueryset, FilterSetClass, \
    CountyFilterSetClass, StaffFilterSetClass
from apps.training.models import ITC, PTC, WBI, WBII, WBIII, ALT, LT, SLSpecialEvent


class ITCList(FilterSetClass, SubCountyMemberQueryset):
    model = ITC
    context_object_name = 'itcs'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural} Events"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Venue', 'Start Date', 'SubCounty']
        return ctx


class PTCList(FilterSetClass, SubCountyMemberQueryset):
    model = PTC
    context_object_name = 'ptcs'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural} Events"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Venue', 'Start Date', 'SubCounty']
        return ctx


class WBIList(CountyFilterSetClass, CountyMemberQueryset):
    model = WBI
    context_object_name = 'wbis'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural}"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Scout Leader', 'Submission Date', 'Marked']
        return ctx


class WBIIList(CountyFilterSetClass, CountyMemberQueryset):
    model = WBII
    context_object_name = 'wbiis'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural} Events"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Venue', 'Start Date', 'County']
        return ctx


class WBIIIList(FilterSetClass, SubCountyMemberQueryset):
    model = WBIII
    context_object_name = 'wbiiis'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural}"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Scout Leader', 'Unit', 'Assessed']
        return ctx


class ALTList(StaffFilterSetClass, StaffMemberQueryset):
    model = ALT
    context_object_name = 'alts'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural} Events"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Venue', 'Start Date', 'County']
        return ctx


class LTList(StaffFilterSetClass, StaffMemberQueryset):
    model = LT
    context_object_name = 'lts'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural} Events"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Venue', 'Start Date', 'County']
        return ctx


class SLSpecialEventList(FilterSetClass, SubCountyMemberQueryset):
    model = SLSpecialEvent
    context_object_name = 'slse'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural} Events"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Event Name', 'Venue', 'Start Date', 'SubCounty']
        return ctx
