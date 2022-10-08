from import_export import resources
from import_export.fields import Field

from apps.accounts.models import User


class UserResource(resources.ModelResource):
    groups = Field()
    user_permissions = Field()
    last_login = Field()
    date_joined = Field()

    class Meta:
        model = User
        skip_unchanged = True
        skip_diff = True
        report_skipped = False
        export_order = ('id', 'first_name', 'last_name', 'email',
                        'is_active', 'is_staff', 'is_superuser',
                        'groups', 'user_permissions',
                        'last_login', 'date_joined')

    @staticmethod
    def dehydrate_groups(self, obj):
        data = [x.name for x in obj.groups.all()]
        return ", ".join(data)

    @staticmethod
    def dehydrate_user_permissions(self, obj):
        data = [x.name for x in obj.user_permissions.all()]
        return ", ".join(data)

    @staticmethod
    def dehydrate_last_login(self, obj):
        return obj.last_login.strftime('%d-%m-%Y')

    @staticmethod
    def dehydrate_date_joined(self, obj):
        return obj.date_joined.strftime('%d-%m-%Y')
