from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Row, Column, Submit, ButtonHolder
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect, AutocompleteSelectMultiple

from apps.core.project_requirements.utilities import report_template
from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.querysets import ScoutLeaderQ, CountyQ, SubCountyQ, UnitQ
from apps.geoposition.fields import GeopositionField
from apps.training.models import ITC, PTC, WBI, WBII, WBIII, ALT, LT, SLSpecialEvent


class ITCForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='ITC'))
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(ITC._meta.get_field('sub_county'), auto_admin_site),
                                        queryset=SubCountyQ)
    course_director = forms.ModelChoiceField(widget=AutocompleteSelect(ITC._meta.get_field('course_director'),
                                                                       auto_admin_site),
                                             queryset=ScoutLeaderQ,
                                             help_text="""Only active Scout Leaders with training level of
                                             Two Beads and above are valid options""")
    support_staff = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(ITC._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ)
    participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(ITC._meta.get_field('participants'), auto_admin_site),
        queryset=ScoutLeaderQ)
    start_date = forms.DateField(label="ITC Date", widget=forms.DateInput(attrs={'type': 'date'}))
    venue = GeopositionField()

    class Meta:
        model = ITC
        fields = ['course_director', 'support_staff', 'participants',
                  'start_date', 'report', 'sub_county', 'venue_name', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add an ITC event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('course_director', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('sub_county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('support_staff', css_class='form-group col-md-6 mb-0'),
                         Column('participants', css_class='form-group col-md-6 mb-0'),
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


class PTCForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='PTC'))
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(PTC._meta.get_field('sub_county'), auto_admin_site),
                                        queryset=SubCountyQ)
    course_director = forms.ModelChoiceField(widget=AutocompleteSelect(PTC._meta.get_field('course_director'),
                                                                       auto_admin_site),
                                             queryset=ScoutLeaderQ,
                                             help_text="""Only active Scout Leaders with training level of
                                             Three Beads and above are valid options""")
    support_staff = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PTC._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ)
    participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PTC._meta.get_field('participants'), auto_admin_site),
        queryset=ScoutLeaderQ)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    venue = GeopositionField()

    class Meta:
        model = PTC
        fields = ['course_director', 'support_staff', 'participants',
                  'start_date', 'end_date', 'report', 'sub_county', 'venue_name', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a PTC event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('course_director', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('sub_county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('support_staff', css_class='form-group col-md-6 mb-0'),
                         Column('participants', css_class='form-group col-md-6 mb-0'),
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


class WBIForm(forms.ModelForm):
    scout_leader = forms.ModelChoiceField(widget=AutocompleteSelect(WBI._meta.get_field('scout_leader'),
                                                                    auto_admin_site),
                                          queryset=ScoutLeaderQ)

    class Meta:
        model = WBI
        fields = ['scout_leader', 'theory_book']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a WoodBadge camp phase event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('scout_leader', css_class='form-group col-md-6 mb-0'),
                         Column('theory_book', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class WBIIForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='WoodBadge Course'))
    county = forms.ModelChoiceField(widget=AutocompleteSelect(WBII._meta.get_field('county'), auto_admin_site),
                                    queryset=CountyQ)
    course_director = forms.ModelChoiceField(widget=AutocompleteSelect(WBII._meta.get_field('course_director'),
                                                                       auto_admin_site),
                                             queryset=ScoutLeaderQ,
                                             help_text="""Only active Scout Leaders with training level of
                                             Four Beads are valid options""")
    support_staff = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(WBII._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ)
    participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(WBII._meta.get_field('participants'), auto_admin_site),
        queryset=ScoutLeaderQ)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    venue = GeopositionField()

    class Meta:
        model = WBII
        fields = ['number', 'course_director', 'support_staff', 'participants',
                  'start_date', 'end_date', 'report', 'county', 'venue_name', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a WoodBadge camp phase event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('number', css_class='form-group col-md-6 mb-0'),
                         Column('course_director', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('support_staff', css_class='form-group col-md-6 mb-0'),
                         Column('participants', css_class='form-group col-md-6 mb-0'),
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


class WBIIIForm(forms.ModelForm):
    unit = forms.ModelChoiceField(widget=AutocompleteSelect(WBIII._meta.get_field('unit'), auto_admin_site),
                                  queryset=UnitQ)
    scout_leader = forms.ModelChoiceField(widget=AutocompleteSelect(WBIII._meta.get_field('scout_leader'),
                                                                    auto_admin_site),
                                          queryset=ScoutLeaderQ,
                                          help_text="""Only active Scout Leaders with training
                                          level of WB Course are valid options""")

    class Meta:
        model = WBIII
        fields = ['unit', 'scout_leader', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('WoodBadge Assessment Application',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('scout_leader', css_class='form-group col-md-6 mb-0'),
                         Column('unit', css_class='form-group col-md-6 mb-0'),
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


class ALTForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='ALT'))
    county = forms.ModelChoiceField(widget=AutocompleteSelect(ALT._meta.get_field('county'), auto_admin_site),
                                    queryset=CountyQ)
    course_director = forms.ModelChoiceField(widget=AutocompleteSelect(ALT._meta.get_field('course_director'),
                                                                       auto_admin_site),
                                             queryset=ScoutLeaderQ,
                                             help_text="""Only active Scout Leaders with training level of
                                             Four Beads are valid options""")
    support_staff = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(ALT._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ)
    participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(ALT._meta.get_field('participants'), auto_admin_site),
        queryset=ScoutLeaderQ)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    venue = GeopositionField()

    class Meta:
        model = ALT
        fields = ['number', 'course_director', 'support_staff', 'participants',
                  'start_date', 'end_date', 'report', 'county', 'venue_name', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add an Assistant Leader Trainer course event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('number', css_class='form-group col-md-6 mb-0'),
                         Column('course_director', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('support_staff', css_class='form-group col-md-6 mb-0'),
                         Column('participants', css_class='form-group col-md-6 mb-0'),
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


class LTForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='LT'))
    county = forms.ModelChoiceField(widget=AutocompleteSelect(LT._meta.get_field('county'), auto_admin_site),
                                    queryset=CountyQ)
    course_director = forms.ModelChoiceField(widget=AutocompleteSelect(LT._meta.get_field('course_director'),
                                                                       auto_admin_site),
                                             queryset=ScoutLeaderQ,
                                             help_text="""Only active Scout Leaders with training level of
                                             Four Beads are valid options""")
    support_staff = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(LT._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ)
    participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(LT._meta.get_field('participants'), auto_admin_site),
        queryset=ScoutLeaderQ)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    venue = GeopositionField()

    class Meta:
        model = LT
        fields = ['number', 'course_director', 'support_staff', 'participants',
                  'start_date', 'end_date', 'report', 'county', 'venue_name', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a Leader Trainer course event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('number', css_class='form-group col-md-6 mb-0'),
                         Column('course_director', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('support_staff', css_class='form-group col-md-6 mb-0'),
                         Column('participants', css_class='form-group col-md-6 mb-0'),
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


class SLSpecialEventForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='SL Special Event'))
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(SLSpecialEvent._meta.get_field('sub_county'),
                                                                  auto_admin_site),
                                        queryset=SubCountyQ)
    course_director = forms.ModelChoiceField(
        widget=AutocompleteSelect(SLSpecialEvent._meta.get_field('course_director'),
                                  auto_admin_site),
        queryset=ScoutLeaderQ,
        help_text="""Only active Scout Leaders with training level of
                                             Four Beads are valid options""")
    support_staff = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(SLSpecialEvent._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ)
    participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(SLSpecialEvent._meta.get_field('participants'), auto_admin_site),
        queryset=ScoutLeaderQ)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    venue = GeopositionField()

    class Meta:
        model = SLSpecialEvent
        fields = ['event_name', 'course_director', 'support_staff', 'participants',
                  'start_date', 'end_date', 'report', 'sub_county', 'venue_name', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a Scout Leader Special event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('event_name', css_class='form-group col-md-6 mb-0'),
                         Column('course_director', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('sub_county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('support_staff', css_class='form-group col-md-6 mb-0'),
                         Column('participants', css_class='form-group col-md-6 mb-0'),
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
