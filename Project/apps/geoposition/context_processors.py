from django.conf import settings


def google_map_key(request):
    return {'GOOGLE_MAP_KEY': f"https://maps.googleapis.com/maps/api/js?key={settings.GEOPOSITION_GOOGLE_MAPS_API_KEY}&callback=initMap"}

