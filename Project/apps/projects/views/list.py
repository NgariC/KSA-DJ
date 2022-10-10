from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import generic

from apps.core.project_requirements.access import NationalMemberQueryset, UnitMemberQueryset, NationalFilterSetClass, \
    FilterSetClass
from apps.projects.models import CSAProject, ALTProject, LTProject, UnitProject


class CSAProjectList(LoginRequiredMixin, FilterSetClass, generic.ListView):
    model = CSAProject
    context_object_name = 'csa_projects'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural}"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Title', 'Project Code']
        return ctx

    def get_queryset(self):
        queryset = CSAProject.objects.all()
        user = self.request.user
        if user.is_staff:
            return queryset
        if not user.link_to_scout_leader:
            raise PermissionDenied
        level = user.link_to_scout_leader.rank.level
        if level == 'National':
            return queryset
        elif level == 'Regional':
            return queryset.filter(
                jasiri_scouts__unit__sub_county__county__region=user.link_to_scout_leader.sub_county.county.region)
        elif level == 'County':
            return queryset.filter(jasiri_scouts__unit__sub_county__county=user.link_to_scout_leader.sub_county.county)
        elif level == 'SubCounty':
            return queryset.filter(jasiri_scouts__unit__sub_county=user.link_to_scout_leader.sub_county)
        else:
            if user.link_to_scout_leader.unit:
                return queryset.filter(jasiri_scouts__unit=user.link_to_scout_leader.unit)

            else:
                raise PermissionDenied()


class UnitProjectList(FilterSetClass, UnitMemberQueryset):
    model = UnitProject
    context_object_name = 'unit_projects'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural}"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Title', 'Unit', 'Coordinator']
        return ctx


class ALTProjectList(NationalFilterSetClass, NationalMemberQueryset):
    model = ALTProject
    context_object_name = 'alt_projects'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural}"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Title', "Scout Leader's Name", 'County']
        return ctx


class LTProjectList(NationalFilterSetClass, NationalMemberQueryset):
    model = LTProject
    context_object_name = 'lt_projects'

    def get_context_data(self, **kwargs):
        opts = self.object_list.model._meta
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"{opts.verbose_name}"
        ctx['title_plural'] = f"{opts.verbose_name_plural}"
        ctx['table_heading'] = f"{opts.verbose_name_plural}"
        ctx['no_table'] = f"There are no {opts.verbose_name_plural} carried out within your jurisdiction yet!"
        ctx['list_display'] = ['#', 'Title', "Scout Leader's Name", 'County']
        return ctx
