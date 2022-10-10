from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Column, HTML, Row, Submit, ButtonHolder
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect, AutocompleteSelectMultiple

from apps.celebrations.models import Founderee, CountyParticipants
from apps.core.project_requirements.utilities import report_template
from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.querysets import ScoutLeaderQ, CountyQ, ScoutQ


class FoundereeForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='Founderee'))
    camp_chief = forms.ModelChoiceField(widget=AutocompleteSelect(Founderee._meta.get_field('camp_chief'),
                                                                  auto_admin_site),
                                        queryset=ScoutLeaderQ,
                                        help_text="Only active Scout Leaders are valid options")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    county = forms.ModelChoiceField(widget=AutocompleteSelect(Founderee._meta.get_field('county'), auto_admin_site),
                                    queryset=CountyQ)
    support_staff = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(Founderee._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ,
        help_text="Only active Scout Leaders are valid options")

    class Meta:
        model = Founderee
        fields = ['camp_chief', 'support_staff',
                  'start_date',
                  'end_date',
                  'report', 'county', 'venue_name', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a new founderee event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('camp_chief', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('support_staff', css_class='form-group col-md-6 mb-0'),
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


class CountyParticipantsForm(forms.ModelForm):
    county = forms.ModelChoiceField(widget=AutocompleteSelect(CountyParticipants._meta.get_field('county'),
                                                              auto_admin_site),
                                    queryset=CountyQ)
    sungura_scouts = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(CountyParticipants._meta.get_field('sungura_scouts'), auto_admin_site),
        queryset=ScoutQ,
        help_text="Only active Sungura Scouts are valid options")
    chipukizi_scouts = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(CountyParticipants._meta.get_field('chipukizi_scouts'), auto_admin_site),
        queryset=ScoutQ,
        help_text="Only active Chipukizi Scouts are valid options")
    mwamba_scouts = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(CountyParticipants._meta.get_field('mwamba_scouts'), auto_admin_site),
        queryset=ScoutQ,
        help_text="Only active Mwamba Scouts are valid options")
    jasiri_scouts = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(CountyParticipants._meta.get_field('jasiri_scouts'), auto_admin_site),
        queryset=ScoutQ,
        help_text="Only active Jasiri Scouts are valid options")
    scout_leaders = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(CountyParticipants._meta.get_field('scout_leaders'), auto_admin_site),
        queryset=ScoutLeaderQ,
        help_text="Only active Scout Leaders are valid options")

    class Meta:
        model = CountyParticipants
        fields = ['county', 'sungura_scouts', 'chipukizi_scouts', 'mwamba_scouts', 'jasiri_scouts', 'scout_leaders']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add participants to the Patrons Day who are not awardees',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('county', css_class='form-group col-md-6 mb-0'),
                         Column('sungura_scouts', css_class='form-group col-md-6 mb-0'),
                         Column('chipukizi_scouts', css_class='form-group col-md-6 mb-0'),
                         Column('mwamba_scouts', css_class='form-group col-md-6 mb-0'),
                         Column('jasiri_scouts', css_class='form-group col-md-6 mb-0'),
                         Column('scout_leaders', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )
