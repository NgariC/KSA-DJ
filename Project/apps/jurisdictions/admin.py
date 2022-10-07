import sys

from django.contrib import admin
from django.db.models import Q
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin

from apps.jurisdictions.models import Country, Region, County, SubCounty, Zone, Rank
from apps.jurisdictions.resources import CountryResource, RegionResource, CountyResource, SubCountyResource, \
    ZoneResource, RankResource
from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.utilities import Perm, Permi, active


@admin.register(Country)
class CountryAdmin(Perm, ImportExportActionModelAdmin):
    list_per_page = sys.maxsize
    resource_class = CountryResource
    show_full_result_count = False
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    list_display_links = ('name',)


@admin.register(Region)
class RegionAdmin(Perm, ImportExportActionModelAdmin):
    list_per_page = sys.maxsize
    resource_class = RegionResource
    show_full_result_count = False
    list_display = ('name', 'country')
    list_filter = ('country',)
    search_fields = ('name',)
    autocomplete_fields = ['country']
    list_select_related = ('country',)


@admin.register(County)
class CountyAdmin(Perm, ImportExportActionModelAdmin):
    # actions = ExportActionModelAdmin.actions + [active]
    list_per_page = sys.maxsize
    resource_class = CountyResource
    show_full_result_count = False
    list_display = ('name', 'code', 'region')
    list_filter = ('active', 'region',)
    search_fields = ('name', 'code')
    autocomplete_fields = ['region', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.select_related('region').filter(active=True)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('jurisdictions.can_verify_county') and 'active' in actions:
            del actions['active']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('jurisdictions.can_verify_county') and 'active' in form.base_fields:
            form.base_fields['active'].disabled = True
        return form


@admin.register(SubCounty)
class SubCountyAdmin(Perm, ImportExportActionModelAdmin):
    # actions = ExportActionModelAdmin.actions + [active]
    list_per_page = sys.maxsize
    resource_class = SubCountyResource
    show_full_result_count = False
    list_display = ('name', 'county')
    list_filter = ('active', 'county__region', 'county',)
    search_fields = ('county__name', 'name', 'county__code')
    autocomplete_fields = ['county', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.select_related('county').filter(Q(county__active=True) & Q(active=True))

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('jurisdictions.can_verify_sub_county') and 'active' in actions:
            del actions['active']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('jurisdictions.can_verify_sub_county') and 'active' in form.base_fields:
            form.base_fields['active'].disabled = True
        return form


@admin.register(Zone)
class ZoneAdmin(Perm, ImportExportActionModelAdmin):
    list_per_page = sys.maxsize
    resource_class = ZoneResource
    show_full_result_count = False
    list_display = ('name', 'sub_county')
    list_filter = ('sub_county__county', 'sub_county',)
    search_fields = ('sub_county__county__name', 'sub_county__name', 'name')
    autocomplete_fields = ['sub_county', ]


@admin.register(Rank)
class RankAdmin(Perm, ImportExportActionModelAdmin):
    # resource_class = RankResource
    list_display = ('code', 'level', 'name')
    search_fields = ('code', 'name', 'level')
    list_filter = ('level',)


class AutoCountryAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('name', 'code')


class AutoRegionAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('name',)


class AutoCountyAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('name', 'code')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('region').filter(active=True)


class AutoSubCountyAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('county__name', 'name', 'county__code')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('county').filter(Q(county__active=True) & Q(active=True))


class AutoZoneAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('sub_county__county__name', 'sub_county__name', 'name')


class AutoRankAdmin(Perm, Permi, admin.ModelAdmin):
    list_per_page = sys.maxsize
    show_full_result_count = False
    search_fields = ('code', 'name', 'level')


auto_admin_site.register(Country, AutoCountryAdmin)
auto_admin_site.register(Region, AutoRegionAdmin)
auto_admin_site.register(County, AutoCountyAdmin)
auto_admin_site.register(SubCounty, AutoSubCountyAdmin)
auto_admin_site.register(Zone, AutoZoneAdmin)
auto_admin_site.register(Rank, AutoRankAdmin)
