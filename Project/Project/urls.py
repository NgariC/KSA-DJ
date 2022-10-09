from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from apps.core.project_requirements.admins import auto_admin_site, stats_admin_site, strict_admin_site

admin.site.site_header = "KSA Portal Administration"
admin.site.site_title = "KSA Administrator"
admin.site.index_title = "KSA Administrator's Portal"
admin.site.empty_value_display = "-----"
admin.site.enable_nav_sidebar = False
# admin.site.save_as = True

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('mhgfhjkghjksiuruyfdmbjkdsfghjgkajkljdfhjgyuegfuygjsdbcjhguds', auto_admin_site.urls),
]

urlpatterns += i18n_patterns(
    path('strict/doc/', include('django.contrib.admindocs.urls')),
    path('ksa-hq/', admin.site.urls),
    path('stats/', stats_admin_site.urls),
    path('strict/', strict_admin_site.urls),
    path('tinymce/', include('tinymce.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [re_path('translations/', include('rosetta.urls'))]
