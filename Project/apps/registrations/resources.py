from import_export import fields, resources
from import_export.widgets import DateTimeWidget, ForeignKeyWidget, SimpleArrayWidget, IntegerWidget, DateWidget

from apps.jurisdictions.models import SubCounty, Rank
from apps.registrations.models import Unit, Scout, ScoutLeader


class UnitResource(resources.ModelResource):
    id = fields.Field(column_name='ID', attribute='id', widget=IntegerWidget())
    name = fields.Field(column_name='Name', attribute='name')
    sponsoring_authority = fields.Field(column_name='Sponsoring Authority', attribute='sponsoring_authority')
    active = fields.Field(column_name='Activeness', attribute='active')
    sections = fields.Field(column_name='Sections', attribute='sections', widget=SimpleArrayWidget(separator=','))
    date_warranted = fields.Field(column_name='Date Warranted', attribute='date_warranted', widget=DateTimeWidget())
    sub_county = fields.Field(column_name='SubCounty', attribute='sub_county',
                              widget=ForeignKeyWidget(SubCounty, 'name'))

    class Meta:
        model = Unit
        skip_unchanged = True
        skip_diff = True
        report_skipped = False
        export_order = ('id', 'name', 'sponsoring_authority', 'sections', 'date_warranted',
                        'sub_county', 'active')


class ScoutResource(resources.ModelResource):
    id = fields.Field(column_name='PK', attribute='id', widget=IntegerWidget())
    first_name = fields.Field(column_name='First Name', attribute='first_name')
    middle_name = fields.Field(column_name='Middle Name', attribute='middle_name')
    surname = fields.Field(column_name='SurName', attribute='surname')
    gender = fields.Field(column_name='Gender', attribute='get_gender_display')
    section = fields.Field(column_name='Section', attribute='section')
    date_of_birth = fields.Field(column_name='Date of Birth', attribute='date_of_birth', widget=DateWidget())
    birth_certificate_number = fields.Field(column_name='Birth Certificate No.', attribute='birth_certificate_number')
    national_id = fields.Field(column_name='ID/Passport', attribute='national_id')
    email = fields.Field(column_name='Email', attribute='email')
    phone_number = fields.Field(column_name='Phone Number', attribute='phone_number')
    unit = fields.Field(column_name='Unit', attribute='unit', widget=ForeignKeyWidget(Unit, 'name'))
    investiture = fields.Field(column_name='Investiture', attribute='investiture')
    jasiri_investiture = fields.Field(column_name='Jasiri Investiture', attribute='jasiri_investiture')
    link_badge_award = fields.Field(column_name='Link Badge Award', attribute='link_badge_award')
    chui_badge_award = fields.Field(column_name='Chui Badge Award', attribute='chui_badge_award')
    simba_badge_award = fields.Field(column_name='Simba Badge Award', attribute='simba_badge_award')
    csa_award = fields.Field(column_name='CSA Award', attribute='csa_award')
    active = fields.Field(column_name='If active', attribute='active')
    registration_date = fields.Field(column_name='Registration Date', attribute='registration_date',
                                     widget=DateTimeWidget())

    class Meta:
        model = Scout
        skip_unchanged = True
        skip_diff = True
        report_skipped = False
        export_order = ('id', 'first_name', 'middle_name', 'surname', 'gender', 'date_of_birth',
                        'birth_certificate_number', 'national_id', 'email',
                        'phone_number', 'unit', 'section', 'active',
                        'investiture', 'jasiri_investiture', 'link_badge_award', 'chui_badge_award',
                        'simba_badge_award',
                        'registration_date')


class ScoutLeaderResource(resources.ModelResource):
    id = fields.Field(column_name='ID', attribute='id', widget=IntegerWidget())
    first_name = fields.Field(column_name='First Name', attribute='first_name')
    middle_name = fields.Field(column_name='Middle Name', attribute='middle_name')
    surname = fields.Field(column_name='SurName', attribute='surname')
    gender = fields.Field(column_name='Gender', attribute='gender')
    date_of_birth = fields.Field(column_name='Date of Birth', attribute='date_of_birth', widget=DateWidget())
    national_id = fields.Field(column_name='ID/Passport', attribute='national_id')
    tsc_number = fields.Field(column_name='TSC Number', attribute='tsc_number', widget=IntegerWidget())
    email = fields.Field(column_name='Email', attribute='email')
    phone_number = fields.Field(column_name='Phone Number', attribute='phone_number')
    unit = fields.Field(column_name='Unit', attribute='unit', widget=ForeignKeyWidget(Unit, 'name'))
    rank = fields.Field(column_name='Rank', attribute='rank', widget=ForeignKeyWidget(Rank, 'name'))
    training = fields.Field(column_name='Level of Training', attribute='training')
    active = fields.Field(column_name='If active', attribute='active')
    life_member = fields.Field(column_name='If life_member', attribute='life_member')
    registration_date = fields.Field(column_name='Registration Date', attribute='registration_date',
                                     widget=DateTimeWidget())
    sub_county = fields.Field(column_name='SubCounty', attribute='sub_county',
                              widget=ForeignKeyWidget(SubCounty, 'name'))

    class Meta:
        model = ScoutLeader
        skip_unchanged = True
        skip_diff = True
        report_skipped = False
        export_order = ('id', 'first_name', 'middle_name', 'surname', 'gender', 'date_of_birth', 'national_id',
                        'tsc_number', 'email', 'phone_number', 'sub_county', 'unit', 'rank', 'active', 'life_member',
                        'training', 'registration_date')
