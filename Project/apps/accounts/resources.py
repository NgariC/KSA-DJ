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

    def dehydrate_groups(self, user):
        data = [x.name for x in user.groups.all()]
        return ", ".join(data)

    def dehydrate_user_permissions(self, user):
        data = [x.name for x in user.user_permissions.all()]
        return ", ".join(data)

    def dehydrate_last_login(self, user):
        return user.last_login.strftime('%d-%m-%Y') if user.last_login else ""

    def dehydrate_date_joined(self, user):
        return user.date_joined.strftime('%d-%m-%Y')

    def dehydrate_image(self, user):
        return user.image.url if user.image and hasattr(user.image, 'url') else user.image
