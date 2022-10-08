import sys

from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin
from tinymce.widgets import TinyMCE

from apps.core.project_requirements.admins import strict_admin_site, stats_admin_site, auto_admin_site
from apps.core.models import SiteConfig, Slide, About, WeProduce, ScoutingInBrief, Department, ScoutsCenter, \
    ComingEvent, Registration
from apps.core.resources import ScoutsCenterResource
from apps.core.stats import ComingEventStats
from apps.core.project_requirements.utilities import OnlySuper, Perm, Permi


class LogEntryAdmin(admin.ModelAdmin):
    # date_hierarchy = 'action_time'
    list_filter = ['user', 'content_type__model', 'action_flag']
    search_fields = ['object_repr', 'change_message']
    list_display = ['action_time', 'user', 'content_type', 'object_link', 'action_flag']
    list_select_related = ['user', 'content_type']
    show_full_result_count = False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            if ct.model in ["site", "siteconfig", "logentry"]:
                link = '<a href="%s">%s</a>' % (reverse(f'strict_admin:{ct.app_label}_{ct.model}_change',
                                                        args=[obj.object_id]), escape(obj.object_repr))

            else:
                link = '<a href="%s">%s</a>' % (reverse(f'admin:{ct.app_label}_{ct.model}_change',
                                                        args=[obj.object_id]), escape(obj.object_repr))

        return mark_safe(link)

    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"


class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    change_list_template = 'site_config.html'


class CustomFlatPage(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE},
    }


strict_admin_site.register(LogEntry, LogEntryAdmin)
admin.site.unregister(Site)
strict_admin_site.register(Site)
admin.site.unregister(FlatPage)
strict_admin_site.register(FlatPage, CustomFlatPage)
strict_admin_site.register(SiteConfig, SiteConfigAdmin)


# admin.site.disable_action('delete_selected')


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'featured')
    list_filter = ('featured',)


@admin.register(About)
class AboutAdmin(OnlySuper, admin.ModelAdmin):
    list_display = ('id',)


@admin.register(WeProduce)
class WeProduceAdmin(OnlySuper, admin.ModelAdmin):
    list_display = ('title',)


@admin.register(ScoutingInBrief)
class ScoutingInBriefAdmin(OnlySuper, admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Department)
class DepartmentAdmin(ImportExportActionModelAdmin):
    list_display = ('name',)
    list_display_links = 'name',


@admin.register(ScoutsCenter)
class ScoutsCenterAdmin(ImportExportActionModelAdmin):
    list_per_page = sys.maxsize
    resource_class = ScoutsCenterResource
    list_display = ('name', 'camp_warden')
    search_fields = ('name', 'camp_warden', 'email', 'sub_county__county')
    list_filter = ('sub_county__county',)
    autocomplete_fields = ['sub_county']
    show_full_result_count = False


def is_published(modeladmin, request, queryset):
    rows_updated = queryset.update(is_published=True)
    if rows_updated == 1:
        message_bit = f"1 {modeladmin.model._meta.model_name} was"
    else:
        message_bit = f"{rows_updated} {modeladmin.model._meta.model_name}s were"
    modeladmin.message_user(request, f"{message_bit} successfully published.")


is_published.allowed_permissions = ('change',)

is_published.short_description = "Mark selected %(verbose_name_plural)s as published"


@admin.register(ComingEvent)
class ComingEventAdmin(ImportExportActionModelAdmin):
    actions = ExportActionModelAdmin.actions + (is_published, )
    list_display = ('event_type', 'start_date', 'end_date', 'county')
    list_filter = ('event_type', 'county__region', 'county')
    search_fields = ('event_type', 'county__region', 'county', 'start_date', 'end_date')
    autocomplete_fields = 'county', 'event_coordinators'
    fields = ['event_type', ('start_date', 'end_date'), 'event_coordinators',
              ('enable_registration', 'registration_deadline_at'),
              'requirement', ('county', 'venue_name'),
              'venue', ('is_featured', 'is_published')
              ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('events.can_publish_coming_events') and 'is_published' in actions:
            del actions['is_published']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('events.can_publish_coming_events') and 'is_published' in form.base_fields:
            form.base_fields['is_published'].disabled = True
        if not request.user.has_perm('events.can_publish_coming_events') and 'is_featured' in form.base_fields:
            form.base_fields['is_featured'].disabled = True
        return form


@admin.register(Registration)
class RegistrationAdmin(ImportExportActionModelAdmin):

    def get_changeform_initial_data(self, request):
        return {'phone_number': '+254'}

    list_display = ('event', 'first_name', 'last_name', 'email')
    list_filter = ('event', 'sub_county', 'sub_county__county', 'sub_county__county__region')
    search_fields = ('event', 'sub_county', 'sub_county__county', 'sub_county__county__region')
    autocomplete_fields = 'event', 'sub_county'
    fields = ['event', ('first_name', 'last_name'), ('phone_number', 'email'), 'sub_county', 'message'
              ]


class AutoComingEventAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('event_type', 'county', 'start_date', 'end_date')


auto_admin_site.register(ComingEvent, AutoComingEventAdmin)


class ComingEventStatsAdmin(Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    change_list_template = 'stats/comingevent.html'
    list_filter = ('event_type', 'county__region', 'county')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Count('id', distinct=True),
        }

        response.context_data['title'] = "Up Coming Events"

        response.context_data['regions'] = list(
            qs.values('county__region__name').annotate(**metrics).order_by('county__region')
        )

        response.context_data['counties'] = list(
            qs.values('county__name').annotate(**metrics).order_by('county__name')
        )

        response.context_data['summary_total'] = dict(qs.aggregate(**metrics))

        return response


stats_admin_site.register(ComingEventStats, ComingEventStatsAdmin)
