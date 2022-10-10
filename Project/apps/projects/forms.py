from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Row, Column, Submit, ButtonHolder
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect, AutocompleteSelectMultiple
from tinymce.widgets import TinyMCE

from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.querysets import ScoutQ, ScoutLeaderQ, UnitQ
from apps.projects.models import CSAProject, ALTProject, LTProject, UnitProject


class CSAProjectForm(forms.ModelForm):
    jasiri_scouts = forms.ModelChoiceField(
        widget=AutocompleteSelectMultiple(CSAProject._meta.get_field('jasiri_scouts'),
                                          auto_admin_site),
        queryset=ScoutQ,
        help_text="Only active Jasiri Scouts who are invested are valid options")
    project_description = forms.CharField(widget=TinyMCE())

    class Meta:
        model = CSAProject
        fields = ['title', 'jasiri_scouts', 'proposal', 'project_description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a Jasiri CSA Project',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('title', css_class='form-group col-md-6 mb-0'),
                         Column('jasiri_scouts', css_class='form-group col-md-6 mb-0'),
                         Column('proposal', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                        <hr>
                        """
                          ),
                     'project_description',
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class ALTProjectForm(forms.ModelForm):
    scout_leader_name = forms.ModelChoiceField(
        widget=AutocompleteSelect(ALTProject._meta.get_field('scout_leader_name'),
                                  auto_admin_site),
        queryset=ScoutLeaderQ,
        help_text="Only active Scout Leaders with training "
                  "level of Two Beads are valid options")
    project_description = forms.CharField(widget=TinyMCE())

    class Meta:
        model = ALTProject
        fields = ['scout_leader_name', 'title', 'project_description', 'proposal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a ScoutLeader ALT Project',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('title', css_class='form-group col-md-6 mb-0'),
                         Column('scout_leader_name', css_class='form-group col-md-6 mb-0'),
                         Column('proposal', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                        <hr>
                        """
                          ),
                     'project_description',
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class LTProjectForm(forms.ModelForm):
    scout_leader_name = forms.ModelChoiceField(widget=AutocompleteSelect(LTProject._meta.get_field('scout_leader_name'),
                                                                         auto_admin_site),
                                               queryset=ScoutLeaderQ,
                                               help_text="Only active Scout Leaders with training level "
                                                         "of Three Beads are valid options")
    project_description = forms.CharField(widget=TinyMCE())

    class Meta:
        model = LTProject
        fields = ['scout_leader_name', 'title', 'project_description', 'proposal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a ScoutLeader LT Project',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('title', css_class='form-group col-md-6 mb-0'),
                         Column('scout_leader_name', css_class='form-group col-md-6 mb-0'),
                         Column('proposal', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                        <hr>
                        """
                          ),
                     'project_description',
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class UnitProjectForm(forms.ModelForm):
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(UnitProject._meta.get_field('unit'),
                                                            auto_admin_site),
                                  queryset=UnitQ,
                                  help_text="Only verified Units are valid options")
    project_description = forms.CharField(widget=TinyMCE())
    coordinator = forms.ModelChoiceField(widget=AutocompleteSelect(UnitProject._meta.get_field('coordinator'),
                                                                   auto_admin_site),
                                         queryset=ScoutLeaderQ,
                                         help_text="Only active Scout Leaders are valid options")

    class Meta:
        model = UnitProject
        fields = ['unit', 'title', 'project_description', 'detailed_report', 'coordinator']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a Unit Project',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('title', css_class='form-group col-md-6 mb-0'),
                         Column('unit', css_class='form-group col-md-6 mb-0'),
                         Column('coordinator', css_class='form-group col-md-6 mb-0'),
                         Column('detailed_report', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                        <hr>
                        """
                          ),
                     'project_description',
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )
