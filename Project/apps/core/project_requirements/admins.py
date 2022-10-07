from django.contrib.admin import AdminSite


class AutoAdminSite(AdminSite):
    site_header = "Portal"
    site_title = "Portal"
    index_title = "KSA Portal"
    empty_value_display = "-----"
    enable_nav_sidebar = False
    index_template = "admin/my_index.html"

    def has_permission(self, request):
        return request.user.is_active


auto_admin_site = AutoAdminSite(name='auto_admin')


class StrictAdminSite(AdminSite):
    site_header = "KSA Super Portal"
    site_title = "KSA Portal"
    index_title = "KSA Super Portal"
    empty_value_display = "-----"
    enable_nav_sidebar = True
    index_template = "admin/my_index.html"

    def has_permission(self, request):
        return request.user.is_superuser


strict_admin_site = StrictAdminSite(name='strict_admin')


class StatsAdminSite(AdminSite):
    site_header = "KSA Portal's Statistics"
    site_title = "KSA Portal's Statistics"
    index_title = "KSA Statistic's Portal"
    empty_value_display = "-----"
    enable_nav_sidebar = False
    index_template = "admin/my_index.html"


stats_admin_site = StatsAdminSite(name='stats_admin')
