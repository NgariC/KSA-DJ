from apps.core.project_requirements.filters_mixin import EventFilterNational, EventFilterRegion, EventFilterCounty, EventFilterSubCounty
from apps.youth_programme.models import Investiture, BadgeCamp, ParkHoliday, PLC, RM


class InvestitureFilterNational(EventFilterNational):

    class Meta:
        model = Investiture
        fields = ['venue_name', 'start_date', 'end_date', 'region', 'county', 'sub_county']


class InvestitureFilterRegion(EventFilterRegion):

    class Meta:
        model = Investiture
        fields = ['venue_name', 'start_date', 'end_date', 'county', 'sub_county']


class InvestitureFilterCounty(EventFilterCounty):

    class Meta:
        model = Investiture
        fields = ['venue_name', 'start_date', 'end_date', 'sub_county']


class InvestitureFilterSubCounty(EventFilterSubCounty):

    class Meta:
        model = Investiture
        fields = ['venue_name', 'start_date', 'end_date']


class BadgecampFilterNational(EventFilterNational):

    class Meta:
        model = BadgeCamp
        fields = ['venue_name', 'start_date', 'end_date', 'region', 'county', 'sub_county']


class BadgecampFilterRegion(EventFilterRegion):

    class Meta:
        model = BadgeCamp
        fields = ['venue_name', 'start_date', 'end_date', 'county', 'sub_county']


class BadgecampFilterCounty(EventFilterCounty):

    class Meta:
        model = BadgeCamp
        fields = ['venue_name', 'start_date', 'end_date', 'sub_county']


class BadgecampFilterSubCounty(EventFilterSubCounty):

    class Meta:
        model = BadgeCamp
        fields = ['venue_name', 'start_date', 'end_date']


class ParkholidayFilterNational(EventFilterNational):

    class Meta:
        model = ParkHoliday
        fields = ['venue_name', 'start_date', 'end_date', 'region', 'county', 'sub_county']


class ParkholidayFilterRegion(EventFilterRegion):

    class Meta:
        model = ParkHoliday
        fields = ['venue_name', 'start_date', 'end_date', 'county', 'sub_county']


class ParkholidayFilterCounty(EventFilterCounty):

    class Meta:
        model = ParkHoliday
        fields = ['venue_name', 'start_date', 'end_date', 'sub_county']


class ParkholidayFilterSubCounty(EventFilterSubCounty):

    class Meta:
        model = ParkHoliday
        fields = ['venue_name', 'start_date', 'end_date']


class PlcFilterNational(EventFilterNational):

    class Meta:
        model = PLC
        fields = ['venue_name', 'start_date', 'end_date', 'region', 'county', 'sub_county']


class PlcFilterRegion(EventFilterRegion):

    class Meta:
        model = PLC
        fields = ['venue_name', 'start_date', 'end_date', 'county', 'sub_county']


class PlcFilterCounty(EventFilterCounty):

    class Meta:
        model = PLC
        fields = ['venue_name', 'start_date', 'end_date', 'sub_county']


class PlcFilterSubCounty(EventFilterSubCounty):

    class Meta:
        model = PLC
        fields = ['venue_name', 'start_date', 'end_date']


class RmFilterNational(EventFilterNational):

    class Meta:
        model = RM
        fields = ['venue_name', 'start_date', 'end_date', 'region', 'county', 'sub_county']


class RmFilterRegion(EventFilterRegion):

    class Meta:
        model = RM
        fields = ['venue_name', 'start_date', 'end_date', 'county', 'sub_county']


class RmFilterCounty(EventFilterCounty):

    class Meta:
        model = RM
        fields = ['venue_name', 'start_date', 'end_date', 'sub_county']


class RmFilterSubCounty(EventFilterSubCounty):

    class Meta:
        model = RM
        fields = ['venue_name', 'start_date', 'end_date']
