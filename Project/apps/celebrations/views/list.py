from apps.celebrations.models import Founderee, CountyParticipants
from apps.core.project_requirements.access import CountyMemberQueryset, CountyFilterSetClass


class FoundereeList(CountyFilterSetClass, CountyMemberQueryset):
    model = Founderee
    context_object_name = 'founderees'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural} Events"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'County', 'Camp Chief', 'Start Date']
        return ctx


class CountyParticipantsList(CountyFilterSetClass, CountyMemberQueryset):
    model = CountyParticipants
    context_object_name = 'patrons_day_participants'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"Patrons Day Participants {opts.verbose_name_plural}"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'County', 'Sungura Scouts', 'Chipukizi Scouts', 'Mwamba Scouts',
                               'Jasiri Scouts', 'Scout Leaders']
        return ctx
