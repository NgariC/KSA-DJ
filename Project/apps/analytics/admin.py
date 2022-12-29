from django.contrib import admin

from apps.analytics.models import ObjectViewed, TaggedItem, Client, PersonClient, CompanyClient, Message, \
    MessageRecipient


class ObjectViewedAdmin(admin.ModelAdmin):
    list_display = ("user", 'content_type', 'object_id', 'content_object')
    # autocomplete_fields = ['content_object']


admin.site.register(ObjectViewed, ObjectViewedAdmin)
admin.site.register(TaggedItem)
admin.site.register(PersonClient)
admin.site.register(CompanyClient)
admin.site.register(Message)
admin.site.register(MessageRecipient)
