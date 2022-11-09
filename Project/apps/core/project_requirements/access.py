import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.views import generic
from django_filters.views import FilterView

from apps.celebrations.models import Founderee, CountyParticipants
from apps.competitions.models import CompetitionTeam
from apps.core.models import ComingEvent
from apps.core.project_requirements.log import log_addition, log_change
from apps.projects.models import UnitProject, CSAProject, ALTProject, LTProject
from apps.celebrations.filters import FoundereeFilterNational, FoundereeFilterRegion, FoundereeFilterCounty, \
    CountyparticipantsFilterNational, CountyparticipantsFilterRegion, CountyparticipantsFilterCounty
from apps.competitions.filters import CompetitionFilterNational, CompetitionFilterRegion, CompetitionFilterCounty, \
    CompetitionFilterSubCounty, CompetitionteamFilterNational, CompetitionteamFilterRegion, \
    CompetitionteamFilterCounty, CompetitionteamFilterSubCounty, CompetitionteamFilterUnit
from apps.projects.filters import CsaprojectFilterNational, CsaprojectFilterRegion, CsaprojectFilterCounty, \
    CsaprojectFilterSubCounty, CsaprojectFilterUnit, AltprojectFilterNational, LtprojectFilterNational, \
    UnitprojectFilterNational, UnitprojectFilterRegion, UnitprojectFilterCounty, UnitprojectFilterSubCounty, \
    UnitprojectFilterUnit
from apps.registrations.filters import UnitFilterNational, UnitFilterRegion, UnitFilterCounty, \
    UnitFilterSubCounty, ScoutFilterNational, ScoutFilterRegion, ScoutFilterCounty, \
    ScoutFilterSubCounty, ScoutFilterUnit, ScoutleaderFilterNational, ScoutleaderFilterRegion, \
    ScoutleaderFilterCounty, ScoutleaderFilterSubCounty, ScoutleaderFilterUnit
from apps.training.filters import ItcFilterNational, ItcFilterRegion, ItcFilterCounty, ItcFilterSubCounty, \
    PtcFilterNational, PtcFilterRegion, PtcFilterCounty, PtcFilterSubCounty, WbiiFilterNational, \
    WbiiFilterRegion, WbiiFilterCounty, AltFilterNational, LtFilterNational, SlspecialeventFilterNational, \
    SlspecialeventFilterRegion, SlspecialeventFilterCounty, SlspecialeventFilterSubCounty, WbiFilterNational, \
    WbiFilterRegion, WbiFilterCounty, WbiiiFilterNational, WbiiiFilterRegion, WbiiiFilterCounty, WbiiiFilterSubCounty
from apps.training.models import WBI
from apps.youth_programme.filters import InvestitureFilterNational, InvestitureFilterRegion, InvestitureFilterCounty, \
    InvestitureFilterSubCounty, BadgecampFilterNational, BadgecampFilterRegion, BadgecampFilterCounty, \
    BadgecampFilterSubCounty, ParkholidayFilterNational, ParkholidayFilterRegion, ParkholidayFilterCounty, \
    ParkholidayFilterSubCounty, PlcFilterNational, PlcFilterRegion, PlcFilterCounty, PlcFilterSubCounty, \
    RmFilterNational, RmFilterRegion, RmFilterCounty, RmFilterSubCounty
from apps.registrations.models import Scout, ScoutLeader


class TraceableAddition:
    def form_valid(self, form):
        log_addition(object=form.save())
        return super().form_valid(form)


class TraceableUpdate:
    def form_valid(self, form):
        log_change(object=form.save())
        return super().form_valid(form)


class DateRegulated:
    pass
    # if datetime.datetime.now().month in [1, 2, 3]:
    #     template_name = 'form.html'
    # else:
    #     template_name = 'registrations/reg_not_allowed.html'


class SelfSuccessMessageMixinRegistered(SuccessMessageMixin, generic.CreateView, DateRegulated, TraceableAddition):
    template_name = 'form.html'

    def get_success_message(self, cleaned_data):
        return u"{0} registered!".format(self.object)


class SelfSuccessMessageMixinRegisteredNoLog(SuccessMessageMixin, generic.CreateView, DateRegulated):
    template_name = 'form.html'

    def get_success_message(self, cleaned_data):
        return u"{0} registered!".format(self.object)


class SelfSuccessMessageMixinAdded(SuccessMessageMixin, generic.CreateView, TraceableAddition):
    template_name = 'form.html'

    def get_success_message(self, cleaned_data):
        return u"{0} added!".format(self.object)


class SelfSuccessMessageMixinAddedNoLog(SuccessMessageMixin, generic.CreateView):
    template_name = 'form.html'

    def get_success_message(self, cleaned_data):
        return u"{0} added!".format(self.object)


class SelfSuccessMessageMixinUpdated(SuccessMessageMixin, generic.UpdateView, TraceableUpdate):
    template_name = 'form.html'

    def get_success_message(self, cleaned_data):
        return u"{0} updated!".format(self.object)


class StaffMemberRequiredForm(LoginRequiredMixin):
    def get_form_class(self, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            return self.form_class
        else:
            raise PermissionDenied


class SubCountyMemberRequiredForm(LoginRequiredMixin):
    def get_form_class(self, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            return self.form_class
        if not user.link_to_scout_leader:
            raise PermissionDenied
        if user.link_to_scout_leader.rank.level in ['National', 'Regional', 'County', 'SubCounty']:
            return self.form_class
        else:
            raise PermissionDenied


class UnitMemberQueryset(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        if self.model == Scout:
            queryset = self.model.objects.active()
        elif self.model == UnitProject:
            queryset = self.model.objects.all()
        elif self.model == CompetitionTeam:
            queryset = self.model.objects.unit_leader()
        else:
            queryset = self.model.objects.paid()
        user = self.request.user
        if user.is_staff:
            return queryset
        if not user.link_to_scout_leader:
            raise PermissionDenied
        level = user.link_to_scout_leader.rank.level
        if level == 'County':
            return queryset.filter(unit__sub_county__county=user.link_to_scout_leader.sub_county.county)
        elif level == 'National':
            return queryset
        elif level == 'Regional':
            return queryset.filter(unit__sub_county__county__region=user.link_to_scout_leader.sub_county.county.region)
        elif level == 'SubCounty':
            return queryset.filter(unit__sub_county=user.link_to_scout_leader.sub_county)
        else:
            if user.link_to_scout_leader.unit:
                return queryset.filter(unit__name=user.link_to_scout_leader.unit.name)

            else:
                raise PermissionDenied


class UnitSubCountyMemberQueryset(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        queryset = self.model.objects.active()
        user = self.request.user
        if user.is_staff:
            return queryset
        if not user.link_to_scout_leader:
            raise PermissionDenied
        level = user.link_to_scout_leader.rank.level
        if level == 'National':
            return queryset
        elif level == 'Regional':
            return queryset.filter(sub_county__county__region=user.link_to_scout_leader.sub_county.county.region)
        elif level == 'County':
            return queryset.filter(sub_county__county=user.link_to_scout_leader.sub_county.county)
        elif level == 'SubCounty':
            return queryset.filter(sub_county=user.link_to_scout_leader.sub_county)
        else:
            if user.link_to_scout_leader.unit:
                return queryset.filter(unit=user.link_to_scout_leader.unit)

            else:
                raise PermissionDenied


class SubCountyMemberQueryset(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        queryset = self.model.objects.paid()
        user = self.request.user
        if user.is_staff:
            return queryset
        if not user.link_to_scout_leader:
            raise PermissionDenied
        level = user.link_to_scout_leader.rank.level
        if level == 'National':
            return queryset
        elif level == 'Regional':
            return queryset.filter(sub_county__county__region=user.link_to_scout_leader.sub_county.county.region)
        elif level == 'County':
            return queryset.filter(sub_county__county=user.link_to_scout_leader.sub_county.county)
        elif level == 'SubCounty':
            return queryset.filter(sub_county=user.link_to_scout_leader.sub_county)
        else:
            raise PermissionDenied


class CountyMemberQueryset(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        if self.model in [WBI, Founderee, CountyParticipants]:
            queryset = self.model.objects.all()
        elif self.model == ComingEvent:
            queryset = self.model.objects.filter(Q(start_date__gte=datetime.datetime.now().date()) &
                                                 Q(is_published=True))
        else:
            queryset = self.model.objects.paid()
        user = self.request.user
        if user.is_staff:
            return queryset
        if not user.link_to_scout_leader:
            raise PermissionDenied()
        level = user.link_to_scout_leader.rank.level
        if level != 'County' and level != 'National' and level != 'Regional' and self.model == ComingEvent or level == 'County':
            return queryset.filter(county=user.link_to_scout_leader.sub_county.county)
        elif level not in ['National', 'Regional']:
            raise PermissionDenied

        elif level == 'National':
            return queryset
        else:
            return queryset.filter(county__region=user.link_to_scout_leader.sub_county.county.region)


class NationalMemberQueryset(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        if self.model in [ALTProject, LTProject]:
            queryset = self.model.objects.all()
        else:
            queryset = self.model.objects.paid()
        user = self.request.user
        if user.is_staff:
            return queryset
        if not user.link_to_scout_leader:
            raise PermissionDenied
        level = user.link_to_scout_leader.rank.level
        if level == 'National':
            return queryset
        else:
            raise PermissionDenied


class StaffMemberQueryset(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        queryset = self.model.objects.paid()
        user = self.request.user
        if user.is_staff:
            return queryset
        else:
            raise PermissionDenied


class FilterSetClass(FilterView):
    def get_filterset_class(self):
        user = self.request.user
        if user.is_staff:
            return eval(f'{self.model._meta.model_name.title()}FilterNational')
        if not user.link_to_scout_leader:
            raise PermissionDenied
        level = user.link_to_scout_leader.rank.level
        if level == 'County':
            return eval(f'{self.model._meta.model_name.title()}FilterCounty')
        elif level == 'National':
            return eval(f'{self.model._meta.model_name.title()}FilterNational')
        elif level == 'Regional':
            return eval(f'{self.model._meta.model_name.title()}FilterRegion')
        elif level == 'SubCounty':
            return eval(f'{self.model._meta.model_name.title()}FilterSubCounty')
        else:
            if not user.link_to_scout_leader.unit:
                raise PermissionDenied()
            return eval(f'{self.model._meta.model_name.title()}FilterUnit') if self.model in [Scout, ScoutLeader, CompetitionTeam, UnitProject, CSAProject] else eval(f'{self.model._meta.model_name.title()}FilterSubCounty')


class CountyFilterSetClass(FilterView):
    def get_filterset_class(self):
        user = self.request.user
        if user.is_staff:
            return eval(f'{self.model._meta.model_name.title()}FilterNational')
        if not user.link_to_scout_leader:
            raise PermissionDenied
        level = user.link_to_scout_leader.rank.level
        if level == 'National':
            return eval(f'{self.model._meta.model_name.title()}FilterNational')
        elif level == 'Regional':
            return eval(f'{self.model._meta.model_name.title()}FilterRegion')
        elif level == 'County':
            return eval(f'{self.model._meta.model_name.title()}FilterCounty')
        else:
            raise PermissionDenied


class NationalFilterSetClass(FilterView):
    def get_filterset_class(self):
        user = self.request.user
        if user.is_staff:
            return eval(f'{self.model._meta.model_name.title()}FilterNational')
        if not user.link_to_scout_leader:
            raise PermissionDenied
        level = user.link_to_scout_leader.rank.level
        if level == 'National':
            return eval(f'{self.model._meta.model_name.title()}FilterNational')
        else:
            raise PermissionDenied


class StaffFilterSetClass(FilterView):
    def get_filterset_class(self):
        user = self.request.user
        if user.is_staff:
            return eval(f'{self.model._meta.model_name.title()}FilterNational')
        else:
            raise PermissionDenied
