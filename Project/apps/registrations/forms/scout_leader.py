from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Row, Column, ButtonHolder, Submit
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.forms import inlineformset_factory

from apps.core.project_requirements.utilities import years_back_100, years_back_26
from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.querysets import UnitQ, SubCountyQ
from apps.jurisdictions.models import Rank
from apps.registrations.forms.scout import GENDER
from apps.registrations.models import ScoutLeader, ScoutLeaderCert
from apps.registrations.models.scout_leaders import TRAINING


class ScoutLeaderCertForm(forms.ModelForm):
    class Meta:
        model = ScoutLeaderCert
        fields = ('name', 'code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset('Register a new Scout Leader',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('name', css_class='form-group col-md-6 mb-0'),
                         Column('code', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


ScoutLeaderCertFormSet = inlineformset_factory(
    ScoutLeader,
    ScoutLeaderCert,
    ScoutLeaderCertForm,
    can_delete=False,
    min_num=1,
    extra=0
)


class ScoutLeaderForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(years_back_100, years_back_26), ))
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(ScoutLeader._meta.get_field('sub_county'),
                                                                  auto_admin_site),
                                        queryset=SubCountyQ)
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(ScoutLeader._meta.get_field('unit'), auto_admin_site),
                                  queryset=UnitQ)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)
    training = forms.ChoiceField(choices=TRAINING, widget=forms.RadioSelect)
    phone_number = forms.NumberInput()
    rank = forms.ModelChoiceField(queryset=Rank.objects.filter(level='Unit').distinct(), initial='Unit-Leader',
                                  help_text="""Due to the controlled nature of KSA positions, ranks higher than 
                                  those within the unit level can only be selected by the secretariat in the 
                                  Training or Programme department""",
                                  widget=forms.RadioSelect)

    class Meta:
        model = ScoutLeader
        fields = ('first_name', 'middle_name', 'surname', 'gender', 'date_of_birth', 'image',
                  'national_id', 'tsc_number', 'email', 'phone_number', 'rank',
                  'sub_county', 'unit', 'training')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['phone_number'].initial = '07'
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset('Register a new Scout Leader',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('first_name', css_class='form-group col-md-6 mb-0'),
                         Column('middle_name', css_class='form-group col-md-6 mb-0'),
                         Column('surname', css_class='form-group col-md-6 mb-0'),
                         Column(InlineRadios('gender'), css_class='form-group col-md-6 mb-0'),
                         Column('date_of_birth', css_class='form-group col-md-6 mb-0'),
                         Column('sub_county', css_class='form-group col-md-6 mb-0'),
                         Column('image', css_class='form-group col-md-6 mb-0'),
                         Column('national_id', css_class='form-group col-md-6 mb-0'),
                         Column('email', css_class='form-group col-md-6 mb-0'),
                         Column('phone_number', css_class='form-group col-md-6 mb-0'),
                         Column('unit', css_class='form-group col-md-6 mb-0'),
                         Column(InlineRadios('rank'), css_class='form-group col-md-6 mb-0'),
                         Column('tsc_number', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),

                     HTML("""
                       <h4><strong>Note:</strong></h4>
                       <p>Fill in the following details with the highest level attained.</p>
                       """
                          ),
                     Row(
                         Column(InlineRadios('training'), css_class='form-group col-md-12 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('another', 'Submit and Add Another', css_class='another primaryAction'),
                Submit('submit', 'Submit', css_class='itself primaryAction'),
            )
        )
