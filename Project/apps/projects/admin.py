from django.contrib import admin

from apps.projects.models import CSAProject, ALTProject, LTProject, UnitProject


@admin.register(CSAProject)
class CSAProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('jasiri_scouts__unit__sub_county__county',)
    search_fields = ('title', 'csa_number', 'jasiri_name__name', 'jasiri_name__code')
    autocomplete_fields = 'jasiri_scouts', 'supervisor'
    list_select_related = ('jasiri_scouts', 'supervisor',)
    readonly_fields = ["project_code"]
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': (('title', 'supervisor'), 'jasiri_scouts')
        }),
        ('Details', {
            'fields': ('proposal', 'project_description')
        }),
        ('Reports', {
            'classes': ('wide',),
            'fields': (('report1', 'report2', 'report3'),)
        }),
        ('Completion Date', {
            'classes': ('wide',),
            'fields': ('completion_date',)
        }),
        ('Other Details Saved Automatically', {
            'classes': ('collapse',),
            'fields': ("project_code",)
        }),
    )


@admin.register(ALTProject)
class ALTProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'scout_leader_name')
    list_filter = ('scout_leader_name__sub_county__county',)
    search_fields = ('title', 'scout_leader_name__name', 'scout_leader_name__code')
    autocomplete_fields = 'scout_leader_name', 'supervisor'
    list_select_related = ('scout_leader_name', 'supervisor',)
    readonly_fields = ["project_code"]
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': (('title', 'supervisor'), 'scout_leader_name')
        }),
        ('Details', {
            'fields': ('proposal', 'project_description')
        }),
        ('Reports', {
            'classes': ('wide',),
            'fields': (('report1', 'report2', 'report3'),)
        }),
        ('Completion Date', {
            'classes': ('wide',),
            'fields': ('completion_date',)
        }),
        ('Other Details Saved Automatically', {
            'classes': ('collapse',),
            'fields': ("project_code",)
        }),
    )


@admin.register(LTProject)
class LTProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'scout_leader_name')
    list_filter = ('scout_leader_name__sub_county__county',)
    search_fields = ('title', 'scout_leader_name__name', 'scout_leader_name__code')
    autocomplete_fields = 'scout_leader_name', 'supervisor'
    list_select_related = ('scout_leader_name', 'supervisor',)
    readonly_fields = ["project_code"]
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': (('title', 'supervisor'), 'scout_leader_name')
        }),
        ('Details', {
            'fields': ('proposal', 'project_description')
        }),
        ('Reports', {
            'classes': ('wide',),
            'fields': (('report1', 'report2', 'report3'),)
        }),
        ('Completion Date', {
            'classes': ('wide',),
            'fields': ('completion_date',)
        }),
        ('Other Details Saved Automatically', {
            'classes': ('collapse',),
            'fields': ("project_code",)
        }),
    )


@admin.register(UnitProject)
class UnitProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit')
    list_filter = ('unit__sub_county__county',)
    search_fields = ('title', 'unit__name', 'unit__code')
    autocomplete_fields = 'unit', 'coordinator'
    list_select_related = ('unit', 'coordinator',)
    readonly_fields = ["project_code"]
    fieldsets = (
        ('', {
            'classes': ('wide',),
            'fields': (('title', 'coordinator'),)
        }),
        ('Details', {
            'fields': ('detailed_report', 'project_description')
        }),
        ('Other Details Saved Automatically', {
            'classes': ('collapse',),
            'fields': ("project_code",)
        }),
    )
