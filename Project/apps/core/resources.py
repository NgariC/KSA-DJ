from import_export import fields, resources
from import_export.widgets import IntegerWidget, ForeignKeyWidget

from apps.jurisdictions.models import SubCounty
from apps.core.models import ScoutsCenter


class ScoutsCenterResource(resources.ModelResource):
    id = fields.Field(column_name='ID', attribute='id', widget=IntegerWidget())
    name = fields.Field(column_name='Name', attribute='name')
    camp_warden = fields.Field(column_name='Camp Warden', attribute='camp_warden')
    email = fields.Field(column_name='Email', attribute='email')
    phone_number = fields.Field(column_name='Phone Number', attribute='phone_number')
    description = fields.Field(column_name='Description', attribute='description')
    services = fields.Field(column_name='Services', attribute='services')
    payments = fields.Field(column_name='Payments', attribute='payments')
    exact_place = fields.Field(column_name='Coordinates', attribute='exact_place')
    sub_county = fields.Field(column_name='SubCounty', attribute='sub_county',
                              widget=ForeignKeyWidget(SubCounty, 'name'), )

    class Meta:
        model = ScoutsCenter
        skip_unchanged = True
        report_skipped = True
        export_order = ('id', 'name', 'camp_warden', 'email', 'phone_number', 'description', 'services', 'payments',
                        'sub_county', 'exact_place')
