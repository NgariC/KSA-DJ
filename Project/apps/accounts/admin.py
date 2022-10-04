from typing import Set

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils.crypto import get_random_string
from apps.accounts.resources import UserResource
from import_export.admin import ImportExportModelAdmin

from apps.accounts.models import User, Groups, EmailActivation

USERNAME_FIELD = get_user_model().USERNAME_FIELD

REQUIRED_FIELDS = (USERNAME_FIELD,) + tuple(get_user_model().REQUIRED_FIELDS)

BASE_FIELDS = (None, {
    'fields': REQUIRED_FIELDS + ('password',),
})

SIMPLE_PERMISSION_FIELDS = ('Permissions', {
    'fields': ('is_active', 'is_staff', 'is_superuser',),
})


def my_excludes(db_field, kwargs):
    qs = kwargs.get('queryset', db_field.remote_field.model.objects)
    qs = qs.exclude(Q(codename__in=(
        'add_permission',
        'change_permission',
        'delete_permission',
        'view_permission',

        'add_group',
        'change_group',
        'delete_group',
        'view_group',

        'add_contenttype',
        'change_contenttype',
        'delete_contenttype',
        'view_contenttype',

        'add_session',
        'delete_session',
        'change_session',
        'view_session',

        'add_logentry',
        'change_logentry',
        'delete_logentry',
        'view_logentry',

        'add_site',
        'change_site',
        'delete_site',
        'view_site',
    )))
    # Avoid a major performance hit resolving permission names which
    # triggers a content_type load:
    kwargs['queryset'] = qs.select_related('content_type')


class CUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super().clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2


class StrippedUserAdmin(UserAdmin):
    add_form_template = None
    add_form = CUserCreationForm
    form = UserChangeForm
    list_display = ('is_active', USERNAME_FIELD, 'is_superuser', 'is_staff',)
    list_filter = ('is_superuser', 'is_staff', 'is_active',)
    fieldsets = (
        BASE_FIELDS,
        SIMPLE_PERMISSION_FIELDS,
    )
    add_fieldsets = (
        (None, {
            'fields': REQUIRED_FIELDS + (
                'password1',
                'password2',
            ),
        }),
    )
    search_fields = (USERNAME_FIELD,)
    ordering = None
    filter_horizontal = tuple()
    readonly_fields = ('last_login', 'date_joined')


class CustomUserAdmin(StrippedUserAdmin, ImportExportModelAdmin):
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'user_permissions':
            my_excludes(db_field, kwargs)
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)

    
    resource_class = UserResource
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('get_full_name', 'email', 'is_staff', 'last_login')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    readonly_fields = ['last_login', 'date_joined']
    add_form = CUserCreationForm
    add_fieldsets = (
        (None, {
            'description': (
                "Enter the new user's name and email address and click save."
                " The user will be emailed a link allowing them to login to"
                " the site and set their password."
            ),
            'fields': ('email', 'first_name', 'last_name'),
        }),
        ('Password', {
            'description': "Optionally, you may set the user's password here.",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change and (not form.cleaned_data['password1'] or not obj.has_usable_password()):
            obj.set_password(get_random_string(12))
            reset_password = True
        else:
            reset_password = False

        super().save_model(request, obj, form, change)

        if reset_password:
            reset_form = PasswordResetForm({'email': obj.email})
            assert reset_form.is_valid()
            reset_form.save(
                request=request,
                use_https=request.is_secure(),
                subject_template_name="registration/account_creation_subject.txt",
                email_template_name="registration/account_creation_email.html",
            )

    fieldsets = (
        ('Personal info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'image')
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'classes': ('wide',),
            'fields': ("last_login", 'date_joined')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        if not request.user.is_superuser:
            disabled_fields |= {
                'email',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

            if obj is not None and obj == request.user:
                disabled_fields |= {
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


class CustomGroupAdmin(GroupAdmin, ImportExportModelAdmin):
    fields = 'name', 'description', 'permissions'

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            my_excludes(db_field, kwargs)
        return super().formfield_for_manytomany(
            db_field, request=request, **kwargs)


class EmailActivationAdmin(admin.ModelAdmin):
    list_display = ('email', 'activated')
    search_fields = ['email']

    class Meta:
        model = EmailActivation


# admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Groups, CustomGroupAdmin)
admin.site.register(EmailActivation, EmailActivationAdmin)
