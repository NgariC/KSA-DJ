from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Submit, Column, Row, Fieldset, Layout, ButtonHolder
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect

from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.querysets import SubCountyQ
from apps.registrations.models import Unit


class UnitForm(forms.ModelForm):
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(Unit._meta.get_field('sub_county'), auto_admin_site),
                                        queryset=SubCountyQ)

    class Meta:
        model = Unit
        fields = ['name', 'sponsoring_authority', 'sections', 'sub_county']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-unitForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset('Register a new unit by filling the form bellow',
                     Row(
                         Column('name', css_class='form-group col-md-6 mb-0'),
                         Column('sponsoring_authority', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     Row(
                         Column('sub_county', css_class='form-group col-md-6 mb-0', autocomplete='on'),
                         Column(InlineCheckboxes('sections'), css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ButtonHolder(
                         Submit('another', 'Submit and Add Another', css_class='another primaryAction'),
                         Submit('submit', 'Submit', css_class='itself primaryAction'),
                     ),
                     HTML("""<h3><strong>Note:</strong></h3> 
                     <p>The unit will only appear in the Units list once it has been paid for and payments verified.</p>
                     <p>This notwithstanding, it is possible to register Scouts and Scout Leaders attached to this 
                     specific unit.</p> """
                          )
                     )
        )
