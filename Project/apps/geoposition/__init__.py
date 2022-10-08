from decimal import Decimal

default_app_config = 'apps.geoposition.apps.GeoPositionConfig'


class Geoposition(object):
    def __init__(self, latitude, longitude):
        if isinstance(latitude, (float, int)):
            latitude = str(latitude)
        if isinstance(longitude, (float, int)):
            longitude = str(longitude)

        self.latitude = Decimal(latitude)
        self.longitude = Decimal(longitude)

    def __str__(self):
        return f"{self.latitude},{self.longitude}"

    def __repr__(self):
        return f"Geoposition({str(self)})"

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        return isinstance(other, Geoposition) and self.latitude == other.latitude and self.longitude == other.longitude

    def __ne__(self, other):
        return not isinstance(other, Geoposition) or self.latitude != other.latitude or self.longitude != other.longitude
