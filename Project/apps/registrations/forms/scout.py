from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Row, Column, Submit, ButtonHolder
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect

from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.querysets import UnitQ
from apps.core.project_requirements.utilities import years_back_27, years_back_18, years_back_3, GENDER
from apps.registrations.models import Scout
from apps.registrations.utilities import SECTION


class SectionSelectForm(forms.Form):
    section = forms.ChoiceField(choices=SECTION, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset("Section selection form",
                     HTML("""
                            <br>
                            """
                          ),
                     Row(
                         Column(InlineRadios('section'), css_class='form-group col-md-8 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class SunguraForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(years_back_18, years_back_3), ))
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(Scout._meta.get_field('unit'), auto_admin_site),
                                  queryset=UnitQ)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)

    class Meta:
        model = Scout
        fields = ['first_name', 'middle_name', 'surname', 'date_of_birth',
                  'birth_certificate_number', 'gender', 'image',
                  'unit', 'investiture', 'nyota_i', 'nyota_ii', 'nyota_iii', 'link_badge_award']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset('Sungura Scout Registration',
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
                         Column('birth_certificate_number', css_class='form-group col-md-6 mb-0'),
                         Column('unit', css_class='form-group col-md-6 mb-0'),
                         Column('image', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                       <h3><strong>Note:</strong></h3>
                       <p>Fill in the following details with the level attained.</p>
                       """
                          ),
                     Row(
                         Column('investiture', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('nyota_i', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('nyota_ii', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('nyota_iii', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('link_badge_award', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('another', 'Submit and Add Another', css_class='another primaryAction'),
                Submit('submit', 'Submit', css_class='itself primaryAction'),
            )
        )


class ChipukiziForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(years_back_18, years_back_3), ))
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(Scout._meta.get_field('unit'), auto_admin_site),
                                  queryset=UnitQ)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)

    class Meta:
        model = Scout
        fields = ['first_name', 'middle_name', 'surname', 'date_of_birth',
                  'birth_certificate_number', 'gender', 'image', 'section',
                  'unit', 'investiture', 'zizi', 'shina', 'tawi', 'chui_badge_award']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset('Chipukizi Scout Registration',
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
                         Column('birth_certificate_number', css_class='form-group col-md-6 mb-0'),
                         Column('unit', css_class='form-group col-md-6 mb-0'),
                         Column('image', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                       <h3><strong>Note:</strong></h3>
                       <p>Fill in the following details with the level attained.</p>
                       """
                          ),
                     Row(
                         Column('investiture', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('zizi', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('shina', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('tawi', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('chui_badge_award', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('another', 'Submit and Add Another', css_class='another primaryAction'),
                Submit('submit', 'Submit', css_class='itself primaryAction'),
            )
        )


class MwambaForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(years_back_18, years_back_3), ))
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(Scout._meta.get_field('unit'), auto_admin_site),
                                  queryset=UnitQ)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)

    class Meta:
        model = Scout
        fields = ['first_name', 'middle_name', 'surname', 'date_of_birth',
                  'birth_certificate_number', 'gender', 'image',
                  'unit', 'investiture', 'mwanzo', 'mwangaza', 'kilele', 'simba_badge_award']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset('Mwamba Scout Registration',
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
                         Column('birth_certificate_number', css_class='form-group col-md-6 mb-0'),
                         Column('unit', css_class='form-group col-md-6 mb-0'),
                         Column('image', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                       <h3><strong>Note:</strong></h3>
                       <p>Fill in the following details with the level attained.</p>
                       """
                          ),
                     Row(
                         Column('investiture', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('mwanzo', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('mwangaza', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('kilele', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('simba_badge_award', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('another', 'Submit and Add Another', css_class='another primaryAction'),
                Submit('submit', 'Submit', css_class='itself primaryAction'),
            )
        )


class JasiriForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(years_back_27, years_back_18), ))
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(Scout._meta.get_field('unit'), auto_admin_site),
                                  queryset=UnitQ)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)
    email = forms.EmailField(required=True)
    national_id = forms.CharField(required=True)
    phone_number = forms.NumberInput()

    class Meta:
        model = Scout
        fields = ['first_name', 'middle_name', 'surname', 'gender', 'date_of_birth',
                  'image', 'national_id', 'email', 'phone_number', 'unit', 'jasiri_investiture', 'csa_award']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].initial = '07'
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset('Register a new Jasiri Scout',
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
                         Column('phone_number', css_class='form-group col-md-6 mb-0'),
                         Column('email', css_class='form-group col-md-6 mb-0'),
                         Column('national_id', css_class='form-group col-md-6 mb-0'),
                         Column('unit', css_class='form-group col-md-6 mb-0'),
                         Column('image', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                       <h3><strong>Note:</strong></h3>
                       <p>Fill in the following details with the highest level attained.</p>
                       """
                          ),
                     Row(
                         Column('jasiri_investiture', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         Column('csa_award', css_class='form-group col-md-2 col-sm-4 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('another', 'Submit and Add Another', css_class='another primaryAction'),
                Submit('submit', 'Submit', css_class='itself primaryAction'),
            )
        )
