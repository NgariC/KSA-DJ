from django.utils.translation import gettext_lazy as _

from apps.core.project_requirements.access import SubCountyMemberQueryset, FilterSetClass
from apps.youth_programme.models import Investiture, BadgeCamp, ParkHoliday, PLC, RM


class InvestitureList(FilterSetClass, SubCountyMemberQueryset):
    model = Investiture
    context_object_name = 'investitures'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _(f"{opts.verbose_name}")
        ctx['title_plural'] = _(f"{opts.verbose_name_plural}")
        ctx['table_heading'] = _(f"{opts.verbose_name_plural} Events")
        ctx['no_table'] = _(f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!")
        ctx['list_display'] = ['#', 'Venue', 'Start Date', 'SubCounty']
        return ctx


class BadgeCampList(FilterSetClass, SubCountyMemberQueryset):
    model = BadgeCamp
    context_object_name = 'badge_camps'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _(f"{opts.verbose_name}")
        ctx['title_plural'] = _(f"{opts.verbose_name_plural}")
        ctx['table_heading'] = _(f"{opts.verbose_name_plural} Events")
        ctx['no_table'] = _(f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!")
        ctx['list_display'] = ['#', 'Venue', 'Start Date', 'SubCounty']
        return ctx


class ParkHolidayList(FilterSetClass, SubCountyMemberQueryset):
    model = ParkHoliday
    context_object_name = 'park_holidays'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _(f"{opts.verbose_name}")
        ctx['title_plural'] = _(f"{opts.verbose_name_plural}")
        ctx['table_heading'] = _(f"{opts.verbose_name_plural} Events")
        ctx['no_table'] = _(f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!")
        ctx['list_display'] = ['#', 'Venue', 'Start Date', 'SubCounty']
        return ctx


class PLCList(FilterSetClass, SubCountyMemberQueryset):
    model = PLC
    context_object_name = 'plcs'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _(f"{opts.verbose_name}")
        ctx['title_plural'] = _(f"{opts.verbose_name_plural}")
        ctx['table_heading'] = _(f"{opts.verbose_name_plural} Events")
        ctx['no_table'] = _(f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!")
        ctx['list_display'] = ['#', 'Venue', 'Start Date', 'SubCounty']
        return ctx


class RMList(FilterSetClass, SubCountyMemberQueryset):
    model = RM
    context_object_name = 'rms'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _(f"{opts.verbose_name}")
        ctx['title_plural'] = _(f"{opts.verbose_name_plural}")
        ctx['table_heading'] = _(f"{opts.verbose_name_plural} Events")
        ctx['no_table'] = _(f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!")
        ctx['list_display'] = ['#', 'Venue', 'Start Date', 'SubCounty']
        return ctx
