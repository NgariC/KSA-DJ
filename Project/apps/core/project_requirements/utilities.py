import datetime
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q
from django.utils.html import format_html

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")

old_enough_18 = datetime.date.today() - datetime.timedelta(days=6570)
old_enough_3 = datetime.date.today() - datetime.timedelta(days=1095)
old_26_years = datetime.date.today() - datetime.timedelta(days=9490)
old_27_years = datetime.date.today() - datetime.timedelta(days=9855)

years_back_3 = int(datetime.date.today().year) - 3
years_back_18 = int(datetime.date.today().year) - 18
years_back_26 = int(datetime.date.today().year) - 26
years_back_27 = int(datetime.date.today().year) - 27
years_back_100 = int(datetime.date.today().year) - 100


def active(modeladmin, request, queryset):
    rows_updated = queryset.update(active=True)
    if rows_updated == 1:
        message_bit = f"1 {modeladmin.model._meta.model_name} was"
    else:
        message_bit = f"{rows_updated} {modeladmin.model._meta.model_name}s were"
    modeladmin.message_user(request, f"{message_bit} successfully marked as active.")


active.allowed_permissions = ('change',)

active.short_description = "Mark selected %(verbose_name_plural)s as active"


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx']
    if ext not in valid_extensions:
        raise ValidationError(u'File not supported!')


class Perm:
    def has_view_permission(self, request, obj=None):
        return True


class Permi:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request):
        return False


class OnlySuper:
    def has_add_permission(self, request):
        return bool(request.user.is_superuser)


def this_year_limit():
    return Q(year=datetime.date.today().year)


def active_limit():
    return Q(active=True)


def active_not_invested_limit():
    return Q(active=True) & Q(investiture=False)


def active_invested_limit():
    return Q(active=True) & Q(investiture=True)


def active_ptc_and_above_limit():
    return Q(active=True) & (Q(training='PTC') |
                             Q(training='WBII Theory') |
                             Q(training='WBII Course') |
                             Q(training='WBII Assessment') |
                             Q(training='Two Beads') |
                             Q(training='ALT Course') |
                             Q(training='ALT Project') |
                             Q(training='Three Beads') |
                             Q(training='LT Course') |
                             Q(training='LT Project') |
                             Q(training='Four Beads'))


def active_two_beads_and_above_limit():
    return Q(active=True) & (Q(training='Two Beads') |
                             Q(training='ALT Course') |
                             Q(training='ALT Project') |
                             Q(training='Three Beads') |
                             Q(training='LT Course') |
                             Q(training='LT Project') |
                             Q(training='Four Beads'))


def active_three_beads_and_above_limit():
    return Q(active=True) & (Q(training='Three Beads') |
                             Q(training='LT Course') |
                             Q(training='LT Project') |
                             Q(training='Four Beads'))


def active_four_beads_limit():
    return Q(active=True) & Q(training='Four Beads')


class List:
    def no_of_participants(self, obj):
        return obj._participants_count

    def participants_list(self, obj):
        return "\n".join(['%d %s (%s %s)' % (i, a.get_short_name, a.phone_number, a.sub_county.name) for i, a in
                          enumerate(obj.trainees.all(), start=1)])

    def staff_list(self, obj):
        return "\n".join(['%d %s (%s %s)' % (i, a.get_short_name, a.phone_number, a.sub_county.name) for i, a in
                          enumerate(obj.staff.all(), start=1)])

    no_of_participants.short_description = "Participants No."
    participants_list.short_description = "List of Participants"
    staff_list.short_description = "Support Staff list"


def payments(modeladmin, request, queryset):
    rows_updated = queryset.update(payments=True)
    if rows_updated == 1:
        message_bit = f"1 {modeladmin.model._meta.model_name} was"
    else:
        message_bit = f"{rows_updated} {modeladmin.model._meta.model_name}s were"
    modeladmin.message_user(request, f"{message_bit} successfully marked as paid.")


payments.allowed_permissions = ('change',)

payments.short_description = "Mark selected %(verbose_name_plural)s as paid"


class Team(Perm):
    def no_of_scouts(self, obj):
        return obj._competitors_count

    def no_of_scout_leaders(self, obj):
        return obj._leaders_count

    def competitors_list(self, obj):
        return "\n".join(
            ['%d %s (%s %s)' % (i, a.get_short_name, a.unit, a.gender) for i, a in enumerate(obj.competitors.all(), start=1)])

    def leaders_list(self, obj):
        return "\n".join(['%d %s (%s %s)' % (i, a.get_short_name, a.phone_number, a.sub_county.name) for i, a in
                          enumerate(obj.leaders.all(), start=1)])

    no_of_scouts.short_description = "Competitors"
    no_of_scout_leaders.short_description = "Leaders"
    competitors_list.short_description = "Competitors List."
    leaders_list.short_description = "Leaders List"


class CoEvent:
    def no_of_scouts(self, obj):
        return obj.competitors_count

    no_of_scouts.short_description = "Competitors"

    def no_of_scout_leaders(self, obj):
        return obj.leaders_count

    no_of_scout_leaders.short_description = "Leaders"

    def assessor_list(self, obj):
        return "\n".join(['%d %s (%s %s)' % (i, a.get_short_name, a.phone_number, a.sub_county.name) for i, a in
                          enumerate(obj.assessor.all(), start=1)])

    def teams_list(self, obj):
        return "\n".join(
            ['%d %s (%s %s)' % (i, a.get_short_name, a.unit, a.gender) for i, a in enumerate(obj.teams.all(), start=1)])

    no_of_scouts.short_description = "Competitors"
    no_of_scout_leaders.short_description = "Leaders"
    assessor_list.short_description = "Assessors List."
    teams_list.short_description = "Teams List."


class Staff:
    def no_of_staff(self, obj):
        return obj._staff_count

    no_of_staff.short_description = "Support Staff No."


class ScoutsAward(Perm):
    def no_of_scouts(self, obj):
        return obj._scouts_count

    no_of_scouts.short_description = "Scouts No."

    def awardees_list(self, obj):
        return "\n".join(
            ['%d %s (%s %s)' % (i, a.get_short_name, a.unit, a.gender) for i, a in enumerate(obj.awardees.all(), start=1)])

    awardees_list.short_description = "Awarded Scouts."


class ScoutLeadersAward(Perm):
    def no_of_scout_leaders(self, obj):
        return obj._scout_leaders_count

    no_of_scout_leaders.short_description = "Scout Leaders No."

    def awardees_list(self, obj):
        return "\n".join(['%d %s (%s %s)' % (i, a.get_short_name, a.phone_number, a.sub_county.name) for i, a in
                          enumerate(obj.awardees.all(), start=1)])

    awardees_list.short_description = "Awarded Scout Leaders."


class AwardEvent(Perm):
    def no_of_sungura_scouts(self, obj):
        return obj._sungura_scouts_count

    def no_of_chipukizi_scouts(self, obj):
        return obj._chipukizi_scouts_count

    def no_of_mwamba_scouts(self, obj):
        return obj._mwamba_scouts_count

    def no_of_jasiri_scouts(self, obj):
        return obj._jasiri_scouts_count

    def no_of_scout_leaders(self, obj):
        return obj._scout_leaders_count

    no_of_sungura_scouts.short_description = "Sungura Awardees"
    no_of_chipukizi_scouts.short_description = "Chipukizi Awardees"
    no_of_mwamba_scouts.short_description = "Mwamba Awardees"
    no_of_jasiri_scouts.short_description = "Jasiri Awardees"
    no_of_scout_leaders.short_description = "Scout Leaders Awardees"


class AwardAttendees(Perm):
    def scouts(self, obj):
        return obj._scout_attendees_count

    def scout_leaders(self, obj):
        return obj._scout_leaders_attendees_count

    scouts.short_description = "Other Scouts"
    scout_leaders.short_description = "Other Scout Leaders"


def report_template(model):
    return format_html(
        'Download the report template <a class="button" target="_blank" href="%sTemplates/%s.docx">here</a> '
        'then attach in this form' % (settings.MEDIA_URL, model)
    )

