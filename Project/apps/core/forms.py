from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, ButtonHolder, HTML, Row, Column
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect, AutocompleteSelectMultiple
from tinymce.widgets import TinyMCE

from apps.accounts.models import User
from apps.core.project_requirements.admins import auto_admin_site
from apps.core.models import ComingEvent, Registration
from apps.core.project_requirements.querysets import CountyQ, ScoutLeaderQ, SubCountyQ, ComingEventQ


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Contact Us',
                'from_email',
                'subject',
                'message',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )
        super().__init__(*args, **kwargs)


class ComingEventForm(forms.ModelForm):
    county = forms.ModelChoiceField(widget=AutocompleteSelect(ComingEvent._meta.get_field('county'), auto_admin_site),
                                    queryset=CountyQ)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    registration_deadline_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                                                   required=False)
    requirement = forms.CharField(widget=TinyMCE())
    event_coordinators = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(ComingEvent._meta.get_field('event_coordinators'), auto_admin_site),
        queryset=ScoutLeaderQ,
        help_text="Only active Scout Leaders are valid options")

    class Meta:
        model = ComingEvent
        fields = ['event_type', 'start_date', 'end_date', 'requirement', 'county', 'venue_name', 'venue',
                  'event_coordinators', 'enable_registration', 'registration_deadline_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Add a new Upcoming Event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('event_type', css_class='form-group col-md-6 mb-0'),
                         Column('county', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('event_coordinators', css_class='form-group col-md-6 mb-0'),
                         Column('enable_registration', css_class='form-group col-md-6 mb-0'),
                         Column('registration_deadline_at', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                        <hr>
                        """
                          ),
                     'requirement',
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


class RegistrationForm(forms.ModelForm):
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(Registration._meta.get_field('sub_county'),
                                                                  auto_admin_site),
                                        queryset=SubCountyQ)
    event = forms.ModelChoiceField(widget=AutocompleteSelect(Registration._meta.get_field('event'),
                                                             auto_admin_site),
                                   queryset=ComingEventQ)

    class Meta:
        model = Registration
        fields = ['event', 'first_name', 'last_name', 'phone_number', 'email', 'sub_county', 'message'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset('Register to attend an Upcoming Event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('event', css_class='form-group col-md-6 mb-0'),
                         Column('first_name', css_class='form-group col-md-6 mb-0'),
                         Column('last_name', css_class='form-group col-md-6 mb-0'),
                         Column('phone_number', css_class='form-group col-md-6 mb-0'),
                         Column('email', css_class='form-group col-md-6 mb-0'),
                         Column('sub_county', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     HTML("""
                        <hr>
                        """
                          ),
                     'message',
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction')
            )
        )


class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    link_to_scout_leader = forms.ModelChoiceField(widget=AutocompleteSelect(
        User._meta.get_field('link_to_scout_leader'), auto_admin_site),
        queryset=ScoutLeaderQ)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'link_to_scout_leader',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-myForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset('User Profile Details',
                     Row(
                         Column('email', css_class='form-group col-md-6 mb-0'),
                         Column('first_name', css_class='form-group col-md-6 mb-0'),
                         Column('last_name', css_class='form-group col-md-6 mb-0'),
                         Column('link_to_scout_leader', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('submit', 'Update', css_class='primaryAction')
            ),
        )
