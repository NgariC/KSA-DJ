from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from apps.jurisdictions.models import Country, Region, County, SubCounty, Zone, Rank


class CountryResource(resources.ModelResource):
    code = Field(column_name='Code', attribute='code')
    name = Field(column_name='Country', attribute='name')

    class Meta:
        model = Country
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('code',)
        fields = ('name', 'code')
        export_order = ('name', 'code')


class RegionResource(resources.ModelResource):
    name = Field(column_name='Region', attribute='name')
    country = Field(column_name='Country', attribute='country', widget=ForeignKeyWidget(Country, 'name'),
                    default='Kenya')

    class Meta:
        model = Region
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('name',)
        fields = ('name', 'country')
        export_order = ('name', 'country')


class CountyResource(resources.ModelResource):
    code = Field(column_name='Code', attribute='code')
    name = Field(column_name='County', attribute='name')
    region = Field(column_name='Region', attribute='region', widget=ForeignKeyWidget(Region, 'name'))

    class Meta:
        model = County
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('code',)
        fields = ('code', 'name', 'region')
        export_order = ('code', 'name', 'region')


class SubCountyResource(resources.ModelResource):
    name = Field(column_name='SubCounty', attribute='name')
    county = Field(column_name='County', attribute='county', widget=ForeignKeyWidget(County, 'name'))

    class Meta:
        model = SubCounty
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('name',)
        fields = ('name', 'county')
        export_order = ('name', 'county')


class ZoneResource(resources.ModelResource):
    name = Field(column_name='Zone', attribute='name')
    sub_county = Field(column_name='SubCounty', attribute='sub_county', widget=ForeignKeyWidget(SubCounty, 'name'))

    class Meta:
        model = Zone
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('name',)
        fields = ('name', 'sub_county')
        export_order = ('name', 'sub_county')


class RankResource(resources.ModelResource):
    code = Field(column_name='Code', attribute='code')
    name = Field(column_name='Rank', attribute='name')
    level = Field(column_name='Level', attribute='level')

    class Meta:
        model = Rank
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('code',)
        fields = ('name', 'code', 'level')
        export_order = ('name', 'code', 'level')
