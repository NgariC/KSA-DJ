from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, IntegerWidget, DateWidget, ManyToManyWidget

from apps.jurisdictions.models import County, SubCounty
from apps.registrations.models import ScoutLeader
from apps.training.models import ITC, PTC, WBI, WBII, WBIII, ALT, LT, SLSpecialEvent


class SubCountyResource(resources.ModelResource):
    sub_county = fields.Field(column_name='SubCounty', attribute='sub_county',
                              widget=ForeignKeyWidget(SubCounty, 'name'))


class CountyResource(resources.ModelResource):
    county = fields.Field(column_name='County', attribute='county',
                          widget=ForeignKeyWidget(County, 'name'))


class SLResource(resources.ModelResource):
    id = fields.Field(column_name='ID', attribute='id', widget=IntegerWidget())
    report = fields.Field(column_name='Report Link', attribute='report')
    payments = fields.Field(column_name='If paid For', attribute='payments')
    venue = fields.Field(column_name='Coordinates', attribute='venue')
    venue_name = fields.Field(column_name='Venue Name', attribute='venue_name')
    start_date = fields.Field(column_name='Start Date', attribute='start_date', widget=DateWidget(format='%d-%m-%Y'))
    end_date = fields.Field(column_name='End Date', attribute='end_date', widget=DateWidget(format='%d-%m-%Y'))
    director = fields.Field(column_name='Course Director', attribute='director',
                            widget=ForeignKeyWidget(ScoutLeader, 'name'))
    staff = fields.Field(column_name='Support Staff', attribute='staff',
                         widget=ManyToManyWidget(ScoutLeader, field='name'))
    trainees = fields.Field(column_name='Trainees', attribute='trainees',
                            widget=ManyToManyWidget(ScoutLeader, field='name'))


class ITCResource(SLResource, SubCountyResource):
    class Meta:
        model = ITC
        skip_unchanged = True
        report_skipped = True
        exclude = ('course_director', 'participants', 'support_staff')
        export_order = ('id', 'sub_county', 'start_date', 'end_date', 'director',
                        'staff', 'trainees', 'report', 'payments',
                        'venue_name', 'venue')


class PTCResource(SLResource, SubCountyResource):
    class Meta:
        model = PTC
        skip_unchanged = True
        report_skipped = True
        exclude = ('course_director', 'participants', 'support_staff')
        export_order = ('id', 'sub_county', 'start_date', 'end_date', 'director',
                        'staff', 'trainees', 'report', 'payments',
                        'venue_name', 'venue')


class WBIResource(resources.ModelResource):
    class Meta:
        model = WBI
        skip_unchanged = True
        report_skipped = True
        export_order = ('id', 'scout_leader_name', 'marker_name', 'theory_book', 'comments',
                        'submission_date', 'payments')


class WBIIResource(SLResource, CountyResource):
    class Meta:
        model = WBII
        skip_unchanged = True
        report_skipped = True
        exclude = ('course_director', 'participants', 'support_staff')
        export_order = ('id', 'county', 'start_date', 'end_date', 'director',
                        'staff', 'trainees', 'report', 'payments',
                        'venue_name', 'venue')


class WBIIIResource(resources.ModelResource):
    class Meta:
        model = WBIII
        skip_unchanged = True
        report_skipped = True
        export_order = ('id', 'unit', 'scout_leader_name', 'assessor_name', 'report', 'assessment_date',
                        'payments', 'venue')


class ALTResource(SLResource, CountyResource):
    class Meta:
        model = ALT
        skip_unchanged = True
        report_skipped = True
        exclude = ('course_director', 'participants', 'support_staff')
        export_order = ('id', 'county', 'start_date', 'end_date', 'director',
                        'staff', 'trainees', 'report', 'payments',
                        'venue_name', 'venue')


class LTResource(SLResource, CountyResource):
    class Meta:
        model = LT
        skip_unchanged = True
        report_skipped = True
        exclude = ('course_director', 'participants', 'support_staff')
        export_order = ('id', 'county', 'start_date', 'end_date', 'director',
                        'staff', 'trainees', 'report', 'payments',
                        'venue_name', 'venue')


class SLSpecialEventResource(SLResource, SubCountyResource):
    class Meta:
        model = SLSpecialEvent
        skip_unchanged = True
        report_skipped = True
        exclude = ('course_director', 'participants', 'support_staff')
        export_order = ('id', 'sub_county', 'start_date', 'end_date', 'director',
                        'staff', 'trainees', 'report', 'payments',
                        'venue_name', 'venue')
