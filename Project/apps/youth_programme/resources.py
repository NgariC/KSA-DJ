from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, IntegerWidget, DateWidget, ManyToManyWidget

from apps.jurisdictions.models import SubCounty
from apps.registrations.models import Scout, ScoutLeader
from apps.youth_programme.models import Badge, Investiture, BadgeCamp, ParkHoliday, PLC, RM


class BadgeResource(resources.ModelResource):
    name = fields.Field(column_name='Badge', attribute='name')
    section = fields.Field(column_name='Section', attribute='section')

    class Meta:
        model = Badge
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('name',)
        fields = ('name', 'section')
        export_order = ('name', 'section')


class BResource(resources.ModelResource):
    badges = fields.Field(column_name='Badges', attribute='badges',
                          widget=ManyToManyWidget(Badge, field='name'))


class EResource(resources.ModelResource):
    id = fields.Field(column_name='ID', attribute='id', widget=IntegerWidget())
    report = fields.Field(column_name='Report Link', attribute='report')
    payments = fields.Field(column_name='If paid For', attribute='payments')
    venue = fields.Field(column_name='Coordinates', attribute='venue')
    venue_name = fields.Field(column_name='Venue Name', attribute='venue_name')
    start_date = fields.Field(column_name='Start Date', attribute='start_date', widget=DateWidget(format='%d-%m-%Y'))
    end_date = fields.Field(column_name='End Date', attribute='end_date', widget=DateWidget(format='%d-%m-%Y'))
    sub_county = fields.Field(column_name='SubCounty', attribute='sub_county',
                              widget=ForeignKeyWidget(SubCounty, 'name'))
    director = fields.Field(column_name='Course Director', attribute='director',
                            widget=ForeignKeyWidget(ScoutLeader, 'name'))
    staff = fields.Field(column_name='Support Staff', attribute='staff',
                         widget=ManyToManyWidget(ScoutLeader, field='name'))
    trainees = fields.Field(column_name='Trainees', attribute='trainees',
                            widget=ManyToManyWidget(Scout, field='name'))


class InvestitureResource(EResource):
    class Meta:
        model = Investiture
        skip_unchanged = True
        report_skipped = True
        exclude = ('investor', 'participants', 'support_staff', 'jasiri_participants')
        export_order = ('id', 'sub_county', 'start_date', 'end_date', 'director',
                        'staff', 'trainees', 'report', 'payments', 'venue_name', 'venue')


class BadgeCampResource(EResource, BResource):
    class Meta:
        model = BadgeCamp
        skip_unchanged = True
        report_skipped = True
        exclude = ('examiner', 'participants', 'support_staff')
        export_order = ('id', 'sub_county', 'start_date', 'end_date', 'director', 'staff',
                        'trainees', 'badges', 'report', 'payments', 'venue_name', 'venue')


class ParkHolidayResource(EResource, BResource):
    class Meta:
        model = ParkHoliday
        skip_unchanged = True
        report_skipped = True
        exclude = ('examiner', 'participants', 'support_staff')
        export_order = ('id', 'sub_county', 'start_date', 'end_date', 'director', 'staff',
                        'trainees', 'badges', 'report', 'payments', 'venue_name', 'venue')


class PLCResource(EResource):
    class Meta:
        model = PLC
        skip_unchanged = True
        report_skipped = True
        exclude = ('course_director', 'participants', 'support_staff')
        export_order = ('id', 'sub_county', 'start_date', 'end_date', 'director',
                        'staff', 'trainees', 'report', 'payments', 'venue_name', 'venue')


class RMResource(EResource):
    class Meta:
        model = RM
        skip_unchanged = True
        report_skipped = True
        exclude = ('course_director', 'participants', 'support_staff')
        export_order = ('id', 'sub_county', 'start_date', 'end_date', 'director',
                        'staff', 'trainees', 'report', 'payments', 'venue_name', 'venue')
