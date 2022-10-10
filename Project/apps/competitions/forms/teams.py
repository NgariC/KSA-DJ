from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Fieldset, Row, Column, Submit, ButtonHolder
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect, AutocompleteSelectMultiple

from apps.competitions.models import CompetitionTeam
from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.querysets import ScoutLeaderQ, UnitQ, ScoutQ, SpecialTeamsCategoriesQ
from apps.registrations.forms.scout import GENDER

SECTION = (
    ('Chipukizi', 'Chipukizi'),
    ('Mwamba', 'Mwamba'),
    ('Jasiri', 'Jasiri'),
)


class SectionSelectForm(forms.Form):
    team_section = forms.ChoiceField(choices=SECTION, widget=forms.RadioSelect)

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
                         Column(InlineRadios('team_section'), css_class='form-group col-md-8 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class CPForm(forms.ModelForm):
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(CompetitionTeam._meta.get_field('unit'), auto_admin_site),
                                  queryset=UnitQ,
                                  help_text="Only verified Units that have Chipukizi Scouts are valid options")
    team_leaders = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(CompetitionTeam._meta.get_field('team_leaders'), auto_admin_site),
        queryset=ScoutLeaderQ,
        help_text="Only active Scout Leaders are valid options")
    chipukizi_competitors = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(CompetitionTeam._meta.get_field('chipukizi_competitors'), auto_admin_site),
        queryset=ScoutQ,
        help_text="Only active & invested Chipukizi Scouts are valid options")
    special_category = forms.ModelChoiceField(
        widget=AutocompleteSelect(CompetitionTeam._meta.get_field('special_category'), auto_admin_site),
        queryset=SpecialTeamsCategoriesQ,
        required=False)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)

    class Meta:
        model = CompetitionTeam
        fields = ['name', 'chipukizi_competitors', 'unit', 'team_leaders', 'gender', 'special', 'special_category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a competing Chipukizi patrol',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('name', css_class='form-group col-md-6 mb-0'),
                         Column('unit', css_class='form-group col-md-6 mb-0'),
                         Column(InlineRadios('gender'), css_class='form-group col-md-6 mb-0'),
                         Column('special', css_class='form-group col-md-6 mb-0'),
                         Column('special_category', css_class='form-group col-md-6 mb-0'),
                         Column('team_leaders', css_class='form-group col-md-6 mb-0'),
                         Column('chipukizi_competitors', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class MPForm(forms.ModelForm):
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(CompetitionTeam._meta.get_field('unit'), auto_admin_site),
                                  queryset=UnitQ,
                                  help_text="Only verified Units that have Mwamba Scouts are valid options")
    team_leaders = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(CompetitionTeam._meta.get_field('team_leaders'), auto_admin_site),
        queryset=ScoutLeaderQ,
        help_text="Only active Scout Leaders are valid options")
    mwamba_competitors = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(CompetitionTeam._meta.get_field('mwamba_competitors'), auto_admin_site),
        queryset=ScoutQ, help_text="Only active & invested Mwamba Scouts are valid options")
    special_category = forms.ModelChoiceField(
        widget=AutocompleteSelect(CompetitionTeam._meta.get_field('special_category'), auto_admin_site),
        queryset=SpecialTeamsCategoriesQ,
        required=False)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)

    class Meta:
        model = CompetitionTeam
        fields = ['name', 'mwamba_competitors', 'unit', 'team_leaders', 'gender', 'special', 'special_category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a competing Mwamba patrol',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('name', css_class='form-group col-md-6 mb-0'),
                         Column('unit', css_class='form-group col-md-6 mb-0'),
                         Column(InlineRadios('gender'), css_class='form-group col-md-6 mb-0'),
                         Column('special', css_class='form-group col-md-6 mb-0'),
                         Column('special_category', css_class='form-group col-md-6 mb-0'),
                         Column('team_leaders', css_class='form-group col-md-6 mb-0'),
                         Column('mwamba_competitors', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class JCForm(forms.ModelForm):
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(CompetitionTeam._meta.get_field('unit'), auto_admin_site),
                                  queryset=UnitQ,
                                  help_text="Only verified Units that have Jasiri Scouts are valid options")
    team_leaders = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(CompetitionTeam._meta.get_field('team_leaders'), auto_admin_site),
        queryset=ScoutLeaderQ,
        help_text="Only active Scout Leaders are valid options")
    jasiri_competitors = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(CompetitionTeam._meta.get_field('jasiri_competitors'), auto_admin_site),
        queryset=ScoutQ, help_text="Only active & invested Jasiri Scouts are valid options")
    special_category = forms.ModelChoiceField(
        widget=AutocompleteSelect(CompetitionTeam._meta.get_field('special_category'), auto_admin_site),
        queryset=SpecialTeamsCategoriesQ,
        required=False)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)

    class Meta:
        model = CompetitionTeam
        fields = ['name', 'jasiri_competitors', 'unit', 'team_leaders', 'gender', 'special', 'special_category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a competing Jasiri crew',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('name', css_class='form-group col-md-6 mb-0'),
                         Column('unit', css_class='form-group col-md-6 mb-0'),
                         Column(InlineRadios('gender'), css_class='form-group col-md-6 mb-0'),
                         Column('special', css_class='form-group col-md-6 mb-0'),
                         Column('special_category', css_class='form-group col-md-6 mb-0'),
                         Column('team_leaders', css_class='form-group col-md-6 mb-0'),
                         Column('jasiri_competitors', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )
