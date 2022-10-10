from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Fieldset, Row, Column, Submit, ButtonHolder
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect, AutocompleteSelectMultiple

from apps.core.project_requirements.utilities import report_template
from apps.competitions.models import Competition
from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.querysets import SubCountyQ, ScoutLeaderQ, CompetitionTeamQ

LEVELS1 = (
    ('SubCounty', 'SubCounty'),
)


class LevelSelectForm1(forms.Form):
    level = forms.ChoiceField(choices=LEVELS1, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset("Competition Level selection form",
                     HTML("""
                            <br>
                            """
                          ),
                     Row(
                         Column(InlineRadios('level'), css_class='form-group col-md-8 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


LEVELS2 = (
    ('SubCounty', 'SubCounty'),
    ('County', 'County'),
)


class LevelSelectForm2(forms.Form):
    level = forms.ChoiceField(choices=LEVELS2, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset("Competition Level selection form",
                     HTML("""
                            <br>
                            """
                          ),
                     Row(
                         Column(InlineRadios('level'), css_class='form-group col-md-8 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


LEVELS3 = (
    ('SubCounty', 'SubCounty'),
    ('County', 'County'),
    ('Regional', 'Regional'),
)


class LevelSelectForm3(forms.Form):
    level = forms.ChoiceField(choices=LEVELS3, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset("Competition Level selection form",
                     HTML("""
                            <br>
                            """
                          ),
                     Row(
                         Column(InlineRadios('level'), css_class='form-group col-md-8 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class SCCForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='Competition'))
    chief_assessor = forms.ModelChoiceField(widget=AutocompleteSelect(Competition._meta.get_field('chief_assessor'),
                                                                      auto_admin_site),
                                            queryset=ScoutLeaderQ,
                                            help_text="Only active Scout Leaders are valid options")
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(Competition._meta.get_field('sub_county'),
                                                                  auto_admin_site),
                                        queryset=SubCountyQ,
                                        help_text="The SubCounty from which the competition is taking place")
    assistant_assessors = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(Competition._meta.get_field('assistant_assessors'), auto_admin_site),
        queryset=ScoutLeaderQ,
        required=False,
        help_text="Only active Scout Leaders are valid options")
    competing_teams = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(Competition._meta.get_field('competing_teams'), auto_admin_site),
        queryset=CompetitionTeamQ,
        required=False,
        help_text="Only teams registered in the year of competition are valid options")

    class Meta:
        model = Competition
        fields = ['chief_assessor', 'assistant_assessors',
                  'competing_teams', 'start_date', 'end_date',
                  'report', 'sub_county', 'venue_name', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a Sub-County competition event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('chief_assessor', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('sub_county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('assistant_assessors', css_class='form-group col-md-6 mb-0'),
                         Column('competing_teams', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                        <hr>
                        """
                          ),
                     'venue',
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class CCForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='Competition'))
    chief_assessor = forms.ModelChoiceField(widget=AutocompleteSelect(Competition._meta.get_field('chief_assessor'),
                                                                      auto_admin_site),
                                            queryset=ScoutLeaderQ,
                                            help_text="Only active Scout Leaders are valid options")
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(Competition._meta.get_field('sub_county'),
                                                                  auto_admin_site),
                                        queryset=SubCountyQ,
                                        help_text="The SubCounty from which the competition is taking place")
    assistant_assessors = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(Competition._meta.get_field('assistant_assessors'), auto_admin_site),
        queryset=ScoutLeaderQ,
        required=False,
        help_text="Only active Scout Leaders are valid options")
    competing_teams = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(Competition._meta.get_field('competing_teams'), auto_admin_site),
        queryset=CompetitionTeamQ,
        required=False,
        help_text="Only teams registered in the year of competition "
                  "and proceeded to the county level are valid options")

    class Meta:
        model = Competition
        fields = ['chief_assessor', 'assistant_assessors',
                  'competing_teams', 'start_date', 'end_date',
                  'report', 'sub_county', 'venue_name', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a County Competition event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('chief_assessor', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('sub_county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('assistant_assessors', css_class='form-group col-md-6 mb-0'),
                         Column('competing_teams', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                        <hr>
                        """
                          ),
                     'venue',
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class RCForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='Competition'))
    chief_assessor = forms.ModelChoiceField(widget=AutocompleteSelect(Competition._meta.get_field('chief_assessor'),
                                                                      auto_admin_site),
                                            queryset=ScoutLeaderQ,
                                            help_text="Only active Scout Leaders are valid options")
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(Competition._meta.get_field('sub_county'),
                                                                  auto_admin_site),
                                        queryset=SubCountyQ,
                                        help_text="The SubCounty from which the competition is taking place")
    assistant_assessors = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(Competition._meta.get_field('assistant_assessors'), auto_admin_site),
        queryset=ScoutLeaderQ,
        help_text="Only active Scout Leaders are valid options")
    competing_teams = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(Competition._meta.get_field('competing_teams'), auto_admin_site),
        queryset=CompetitionTeamQ,
        required=False,
        help_text="Only teams registered in the year of competition "
                  "and proceeded to the regional level are valid options")

    class Meta:
        model = Competition
        fields = ['chief_assessor', 'assistant_assessors',
                  'competing_teams', 'start_date', 'end_date',
                  'report', 'sub_county', 'venue_name', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a Regional Competitions event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('chief_assessor', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('sub_county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('assistant_assessors', css_class='form-group col-md-6 mb-0'),
                         Column('competing_teams', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                        <hr>
                        """
                          ),
                     'venue',
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )
