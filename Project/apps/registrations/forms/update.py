from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Row, Column, Submit, ButtonHolder
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect

from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.querysets import UnitQ
from apps.registrations.models import Scout, ScoutLeader
# from apps.registrations.utilities import SECTION

SECTION_1 = (
    ('Chipukizi', 'Chipukizi'),
)
SECTION_2 = (
    ('Mwamba', 'Mwamba'),
)
SECTION_3 = (
    ('Jasiri', 'Jasiri'),
)


class ScoutUnitUpdateForm(forms.ModelForm):
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(Scout._meta.get_field('unit'), auto_admin_site),
                                  queryset=UnitQ)

    class Meta:
        model = Scout
        fields = ['unit', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset('Scout Unit update application',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('unit', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class ScoutSectionUpdateForm(forms.ModelForm):
    # section = forms.ChoiceField(choices=SECTION, widget=forms.RadioSelect)

    class Meta:
        model = Scout
        fields = ['section', 'email', 'national_id', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial['section'] == "Sungura":
            SECTION = SECTION_1
            del self.fields['email']
            del self.fields['national_id']
            del self.fields['phone_number']
        elif self.initial['section'] == "Chipukizi":
            del self.fields['email']
            del self.fields['national_id']
            del self.fields['phone_number']
            SECTION = SECTION_2
        else:
            SECTION = SECTION_3
        self.fields['section'].widget = forms.RadioSelect()
        self.fields['section'].choices = SECTION
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset('Scout Section update application',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column(InlineRadios('section'), css_class='form-group col-md-6 mb-0'),
                         Column('phone_number', css_class='form-group col-md-6 mb-0'),
                         Column('email', css_class='form-group col-md-6 mb-0'),
                         Column('national_id', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class ScoutLeaderUnitUpdateForm(forms.ModelForm):
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(ScoutLeader._meta.get_field('unit'), auto_admin_site),
                                  queryset=UnitQ)

    class Meta:
        model = ScoutLeader
        fields = ['unit', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset('Scout Leader Unit update application',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('unit', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )
