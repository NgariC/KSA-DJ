from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from apps.accounts.views import AccountEmailActivateView, SignUp, CustomLoginView, view_profile, UserUpdate
from apps.core.project_requirements import sitemaps
from apps.core.project_requirements.admins import auto_admin_site, stats_admin_site, strict_admin_site
from apps.core.views import DashboardView, clear

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

    path('', include("apps.accounts.passwords.urls")),
    path("login/", CustomLoginView.as_view(), name="login"),
    path('email/confirm/(<key>[0-9A-Za-z]+)/', AccountEmailActivateView.as_view(), name='email-activate'),
    path('email/resend-activation/', AccountEmailActivateView.as_view(), name='resend-activation'),
    path('sign-up', SignUp.as_view(), name='sign_up'),
    path('profile', view_profile, name='view_profile'),
    path('profile/edit/<int:pk>', UserUpdate.as_view(), name='edit_profile'),
    # path('privacy-policy', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),
    # path('terms-&-conditions', TemplateView.as_view(template_name='terms_&_conditions.html'),
    #      name='terms_&_conditions'),
    path('privacy-policy/', flatpage, {'url': '/privacy-policy/'}, name='privacy_policy'),
    path('terms-and-conditions/', flatpage, {'url': '/terms-and-conditions/'}, name='terms_&_conditions'),

    path('', DashboardView.as_view(), name='home'),

    path('', include('apps.core.urls'), name='core'),
    path('celebrations/', include('apps.celebrations.urls'), name='celebrations'),
    path('competitions/', include('apps.competitions.urls'), name='competitions'),
    path('files/', include('apps.files.urls'), name='files'),
    path('payments/', include('apps.payments.urls'), name='payments'),
    path('api/payments/', include("apps.payments.api.urls"), name='payments_api'),
    path('projects/', include('apps.projects.urls'), name='projects'),
    path('registrations/', include('apps.registrations.urls'), name='registration'),
    path('training-dep/', include('apps.training.urls'), name='training'),
    path('youth-programme-dep/', include('apps.youth_programme.urls'), name='youth_programme'),

    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
)

htmx_urlpatterns = [
    path('clear/', clear, name='clear'),
]

urlpatterns += htmx_urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [re_path('translations/', include('rosetta.urls'))]
