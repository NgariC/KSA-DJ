import base64
import datetime
import os
from io import BytesIO

import numpy as np
import pandas as pd
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from matplotlib import pyplot as plt

GENDER = (
    ('M', _('Male')),
    ('F', _('Female')),
)

mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message=_("Entered mobile number isn't in a right format!"))

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
        message_bit = _(f"1 {modeladmin.model._meta.model_name} was")
    else:
        message_bit = _(f"{rows_updated} {modeladmin.model._meta.model_name}s were")
    modeladmin.message_user(request, _(f"{message_bit} successfully marked as active."))


active.allowed_permissions = ('change',)

active.short_description = _("Mark selected %(verbose_name_plural)s as active")


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx']
    if ext not in valid_extensions:
        raise ValidationError(_(u'File not supported!'))


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

    no_of_participants.short_description = _("Participants No.")
    participants_list.short_description = _("List of Participants")
    staff_list.short_description = _("Support Staff list")


def payments(modeladmin, request, queryset):
    rows_updated = queryset.update(payments=True)
    if rows_updated == 1:
        message_bit = _(f"1 {modeladmin.model._meta.model_name} was")
    else:
        message_bit = _(f"{rows_updated} {modeladmin.model._meta.model_name}s were")
    modeladmin.message_user(request, _(f"{message_bit} successfully marked as paid."))


payments.allowed_permissions = ('change',)

payments.short_description = _("Mark selected %(verbose_name_plural)s as paid")


class Team(Perm):
    def no_of_scouts(self, obj):
        return obj._competitors_count

    def no_of_scout_leaders(self, obj):
        return obj._leaders_count

    def competitors_list(self, obj):
        return "\n".join(
            ['%d %s (%s %s)' % (i, a.get_short_name, a.unit, a.gender) for i, a in
             enumerate(obj.competitors.all(), start=1)])

    def leaders_list(self, obj):
        return "\n".join(['%d %s (%s %s)' % (i, a.get_short_name, a.phone_number, a.sub_county.name) for i, a in
                          enumerate(obj.leaders.all(), start=1)])

    no_of_scouts.short_description = _("Competitors")
    no_of_scout_leaders.short_description = _("Leaders")
    competitors_list.short_description = _("Competitors List.")
    leaders_list.short_description = _("Leaders List")


class CoEvent:
    def no_of_scouts(self, obj):
        return obj.competitors_count

    no_of_scouts.short_description = _("Competitors")

    def no_of_scout_leaders(self, obj):
        return obj.leaders_count

    no_of_scout_leaders.short_description = _("Leaders")

    def assessor_list(self, obj):
        return "\n".join(['%d %s (%s %s)' % (i, a.get_short_name, a.phone_number, a.sub_county.name) for i, a in
                          enumerate(obj.assessor.all(), start=1)])

    def teams_list(self, obj):
        return "\n".join(
            ['%d %s (%s %s)' % (i, a.get_short_name, a.unit, a.gender) for i, a in enumerate(obj.teams.all(), start=1)])

    no_of_scouts.short_description = _("Competitors")
    no_of_scout_leaders.short_description = _("Leaders")
    assessor_list.short_description = _("Assessors List.")
    teams_list.short_description = _("Teams List.")


class Staff:
    def no_of_staff(self, obj):
        return obj._staff_count

    no_of_staff.short_description = _("Support Staff No.")


class ScoutsAward(Perm):
    def no_of_scouts(self, obj):
        return obj._scouts_count

    no_of_scouts.short_description = _("Scouts No.")

    def awardees_list(self, obj):
        return "\n".join(
            ['%d %s (%s %s)' % (i, a.get_short_name, a.unit, a.gender) for i, a in
             enumerate(obj.awardees.all(), start=1)])

    awardees_list.short_description = _("Awarded Scouts.")


class ScoutLeadersAward(Perm):
    def no_of_scout_leaders(self, obj):
        return obj._scout_leaders_count

    no_of_scout_leaders.short_description = _("Scout Leaders No.")

    def awardees_list(self, obj):
        return "\n".join(['%d %s (%s %s)' % (i, a.get_short_name, a.phone_number, a.sub_county.name) for i, a in
                          enumerate(obj.awardees.all(), start=1)])

    awardees_list.short_description = _("Awarded Scout Leaders.")


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

    no_of_sungura_scouts.short_description = _("Sungura Awardees")
    no_of_chipukizi_scouts.short_description = _("Chipukizi Awardees")
    no_of_mwamba_scouts.short_description = _("Mwamba Awardees")
    no_of_jasiri_scouts.short_description = _("Jasiri Awardees")
    no_of_scout_leaders.short_description = _("Scout Leaders Awardees")


class AwardAttendees(Perm):
    def scouts(self, obj):
        return obj._scout_attendees_count

    def scout_leaders(self, obj):
        return obj._scout_leaders_attendees_count

    scouts.short_description = _("Other Scouts")
    scout_leaders.short_description = _("Other Scout Leaders")


def report_template(model):
    return format_html(
        _('Download the report template <a class="button" target="_blank" href="%sTemplates/%s.docx">here</a> '
          'then attach in this form' % (settings.MEDIA_URL, model)
          ))


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def event_chart(df, level, model):
    plt.switch_backend('AGG')
    plt.subplots()
    plt.figure(figsize=(16, 9))

    x = df[level]
    y1 = df[f'{model}']
    y2 = df['Male']
    y3 = df['Female']
    width = 0.4
    z = np.arange(len(df))

    plt.plot(x, y1, label='Totals', color='red', marker='o', linestyle='dashed')
    plt.bar(z - (width / 2), y2, width=width, color='blue', label='Male')
    plt.bar(z + (width / 2), y3, width=width, color='pink', label='Female')
    if level == 'Region':
        plt.title(f'{model.upper()} PER {level.upper()}S', fontsize=20)
        plt.xlabel(f'{level.upper()}S', fontsize=14)
    elif level == 'County':
        plt.title(f'{model.upper()} PER COUNTIES', fontsize=20)
        plt.xlabel('COUNTIES', fontsize=14)
    elif level == 'SubCounty':
        plt.title(f'{model.upper()} PER SUBCOUNTIES', fontsize=20)
        plt.xlabel('SUBCOUNTIES', fontsize=14)
    plt.ylabel(model.upper(), fontsize=14)
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    return get_graph()


def event_table(df, summary_total, level, model):
    new_row = pd.Series(data={f'{level}': 'Total',
                              'Male': summary_total.get('male_total'),
                              'Female': summary_total.get('female_total'),
                              f'{model}': summary_total.get('total'),
                              'Percentage': '100% of Total'}, name='-')
    df['Percentage'] = round((df.get(model) / summary_total.get('total') * 100), 2)
    df.index = np.arange(1, len(df) + 1)
    df = df.append(new_row, ignore_index=False)
    df.insert(2, 'M-%', round((df.get('Male') / summary_total.get('male_total') * 100)), 2)
    df.insert(4, 'F-%', round((df.get('Female') / summary_total.get('female_total') * 100)), 2)
    return df.to_html(border=0, classes='totals')
