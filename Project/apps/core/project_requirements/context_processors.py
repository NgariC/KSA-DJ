from apps.core.models import SiteConfig


def site_defaults(request):
    vals = SiteConfig.objects.all()
    return {val.key: val.value for val in vals}