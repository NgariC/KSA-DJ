from django.contrib import admin

from apps.files.models import Document, LegalDocuments, FormTemplate


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_to_cease_showing'
    list_display = ('doc_name', 'date_to_cease_showing')
    search_fields = ('doc_name', 'description')
    list_filter = ('timestamp', 'date_to_cease_showing',)


@admin.register(LegalDocuments)
class LegalDocumentsAdmin(admin.ModelAdmin):
    list_display = ('doc_name',)
    search_fields = ('doc_name',)
    list_filter = ('timestamp',)


@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')
    change_list_template = 'files/form_templates.html'
