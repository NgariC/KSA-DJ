from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Fieldset, Row, Column, Submit, ButtonHolder
from django import forms
from django.contrib.admin.widgets import AutocompleteSelectMultiple

from apps.competitions.models import Competition
from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.querysets import CompetitionTeamQ


class CompetitionUpdateForm(forms.ModelForm):
    competing_teams = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(Competition._meta.get_field('competing_teams'), auto_admin_site),
        queryset=CompetitionTeamQ,  required=False,
        help_text="Only teams registered in the year of competition are valid options")

    class Meta:
        model = Competition
        fields = ['competing_teams']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Update a Sub-County competition teams',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('competing_teams', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )
