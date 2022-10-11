from crispy_forms.bootstrap import TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Column, HTML, Row, Submit, ButtonHolder
from django import forms
from django.contrib.admin.widgets import AutocompleteSelectMultiple

from apps.core.project_requirements.admins import auto_admin_site
from apps.payments.models import PaymentsList

from apps.registrations.models import Unit, Scout, ScoutLeader
from apps.training.models import ITC, PTC
from apps.youth_programme.models import Investiture, BadgeCamp, ParkHoliday, PLC, RM


class RegistrationForm(forms.ModelForm):
    units = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('units'), auto_admin_site),
        queryset=Unit.objects.all(), required=False,
        help_text="Kshs 500 will be charged for every Unit selected")
    scouts = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('scouts'), auto_admin_site),
        queryset=Scout.objects.all(), required=False,
        help_text="Kshs 100 will be charged for every Scout selected")
    scout_leaders = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('scout_leaders'), auto_admin_site),
        queryset=ScoutLeader.objects.all(), required=False,
        help_text='''Scout Leaders charges are distributed in levels of thier positions as follows
                  National Level --> Kshs 2000
                  Regional & County Level --> Kshs 1000
                  SubCounty Level --> Kshs 500
                  Zonal & Unit Level --> Kshs 300''')

    class Meta:
        model = PaymentsList
        fields = ['units', 'scouts', 'scout_leaders']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Units, Scouts & Scout Leaders to pay for',
                     Row(
                         Column('units', css_class='form-group col-md-6 mb-0'),
                         Column('scouts', css_class='form-group col-md-6 mb-0'),
                         Column('scout_leaders', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction'),
            )
        )


class PaymentsForm(forms.ModelForm):
    units = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('units'), auto_admin_site),
        queryset=Unit.objects.all(), required=False,
        help_text="Kshs 500 will be charged for every Unit selected")
    scouts = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('scouts'), auto_admin_site),
        queryset=Scout.objects.all(), required=False,
        help_text="Kshs 100 will be charged for every Scout selected")
    scout_leaders = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('scout_leaders'), auto_admin_site),
        queryset=ScoutLeader.objects.all(), required=False,
        help_text='''Scout Leaders charges are distributed in levels of their positions as follows
                  National Level --> Kshs 2000
                  Regional & County Level --> Kshs 1000
                  SubCounty Level --> Kshs 500
                  Zonal & Unit Level --> Kshs 300''')
    itcs = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('itcs'), auto_admin_site),
        queryset=ITC.objects.all(), required=False,
        help_text="Kshs 100 will be charged for every trainee in the ITC events selected")
    ptcs = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('ptcs'), auto_admin_site),
        queryset=PTC.objects.all(), required=False,
        help_text="Kshs 100 will be charged for every trainee in the PTC events selected")
    investitures = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('investitures'), auto_admin_site),
        queryset=Investiture.objects.all(), required=False,
        help_text="Kshs 50 will be charged for every trainee in the Investiture events selected")
    badge_camps = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('badge_camps'), auto_admin_site),
        queryset=BadgeCamp.objects.all(), required=False,
        help_text="Kshs 50 will be charged for every trainee in the Badge Camp events selected")
    park_holidays = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('park_holidays'), auto_admin_site),
        queryset=ParkHoliday.objects.all(), required=False,
        help_text="Kshs 50 will be charged for every trainee in the ParkHoliday events selected")
    plcs = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('plcs'), auto_admin_site),
        queryset=PLC.objects.all(), required=False,
        help_text="Kshs 50 will be charged for every trainee in the PLC events selected")
    rover_mates = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PaymentsList._meta.get_field('rover_mates'), auto_admin_site),
        queryset=RM.objects.all(), required=False,
        help_text="Kshs 50 will be charged for every trainee in the Rovermate events selected")

    class Meta:
        model = PaymentsList
        fields = ['units', 'scouts', 'scout_leaders', 'itcs', 'ptcs', 'investitures', 'badge_camps',
                  'park_holidays', 'plcs', 'rover_mates']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            TabHolder(
                Tab('Registration',
                    Row(
                        Column('units', css_class='form-group col-md-6 mb-0'),
                        Column('scouts', css_class='form-group col-md-6 mb-0'),
                        Column('scout_leaders', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    ),
                Tab('Scout Leaders Courses',
                    Row(
                        Column('itcs', css_class='form-group col-md-6 mb-0'),
                        Column('ptcs', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    ),
                Tab('Scouts Events',
                    Row(
                        Column('investitures', css_class='form-group col-md-6 mb-0'),
                        Column('badge_camps', css_class='form-group col-md-6 mb-0'),
                        Column('park_holidays', css_class='form-group col-md-6 mb-0'),
                        Column('plcs', css_class='form-group col-md-6 mb-0'),
                        Column('rover_mates', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    ),
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction'),
            )
        )
