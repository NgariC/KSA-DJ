from crispy_forms.bootstrap import TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Row, Column, Submit, ButtonHolder
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect, AutocompleteSelectMultiple

from apps.core.project_requirements.utilities import report_template
from apps.core.project_requirements.admins import auto_admin_site
from apps.core.project_requirements.querysets import ScoutQ, ScoutLeaderQ, SubCountyQ
from apps.geoposition.fields import GeopositionField
from apps.youth_programme.models import Investiture, BadgeCamp, Badge, ParkHoliday, PLC, RM


class InvestitureForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='Investiture'))
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(Investiture._meta.get_field('sub_county'),
                                                                  auto_admin_site),
                                        queryset=SubCountyQ)
    investor = forms.ModelChoiceField(widget=AutocompleteSelect(Investiture._meta.get_field('investor'),
                                                                auto_admin_site),
                                      queryset=ScoutLeaderQ,
                                      help_text="""Only active Scout Leaders with training level of
                                      Two Beads and above are valid options""")
    support_staff = forms.ModelMultipleChoiceField(
        label='Witnesses',
        widget=AutocompleteSelectMultiple(Investiture._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ)
    participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(Investiture._meta.get_field('participants'), auto_admin_site),
        required=False, queryset=ScoutQ)
    jasiri_participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(Investiture._meta.get_field('jasiri_participants'), auto_admin_site),
        required=False, queryset=ScoutQ)
    start_date = forms.DateField(label="Investiture Date", widget=forms.DateInput(attrs={'type': 'date'}))
    venue = GeopositionField()

    class Meta:
        model = Investiture
        fields = ['investor', 'support_staff', 'participants', 'jasiri_participants',
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
            Fieldset('Add an investiture event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('investor', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('sub_county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('support_staff', css_class='form-group col-md-6 mb-0'),
                         Column('participants', css_class='form-group col-md-6 mb-0'),
                         Column('jasiri_participants', css_class='form-group col-md-6 mb-0'),
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


class BadgeCampForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='Badge Camp'))
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(BadgeCamp._meta.get_field('sub_county'),
                                                                  auto_admin_site),
                                        queryset=SubCountyQ)
    examiner = forms.ModelChoiceField(widget=AutocompleteSelect(BadgeCamp._meta.get_field('examiner'),
                                                                auto_admin_site),
                                      queryset=ScoutLeaderQ,
                                      help_text="""Only active Scout Leaders with training level of
                                      Two Beads and above are valid options""")
    support_staff = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(BadgeCamp._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ, required=False)
    nyota_i_participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(BadgeCamp._meta.get_field('nyota_i_participants'), auto_admin_site),
        queryset=ScoutQ, required=False)
    nyota_ii_participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(BadgeCamp._meta.get_field('nyota_ii_participants'), auto_admin_site),
        queryset=ScoutQ, required=False)
    nyota_iii_participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(BadgeCamp._meta.get_field('nyota_iii_participants'), auto_admin_site),
        queryset=ScoutQ, required=False)
    zizi_participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(BadgeCamp._meta.get_field('zizi_participants'), auto_admin_site),
        queryset=ScoutQ, required=False)
    shina_participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(BadgeCamp._meta.get_field('shina_participants'), auto_admin_site),
        queryset=ScoutQ, required=False)
    tawi_participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(BadgeCamp._meta.get_field('tawi_participants'), auto_admin_site),
        queryset=ScoutQ, required=False)
    mwanzo_participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(BadgeCamp._meta.get_field('mwanzo_participants'), auto_admin_site),
        queryset=ScoutQ, required=False)
    mwangaza_participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(BadgeCamp._meta.get_field('mwangaza_participants'), auto_admin_site),
        queryset=ScoutQ, required=False)
    kilele_participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(BadgeCamp._meta.get_field('kilele_participants'), auto_admin_site),
        queryset=ScoutQ, required=False)
    # badges = forms.ModelMultipleChoiceField(
    #     widget=AutocompleteSelectMultiple(BadgeCamp._meta.get_field('badges'), auto_admin_site),
    #     queryset=Badge.objects.all())
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = BadgeCamp
        fields = ['examiner', 'support_staff', 'nyota_i_participants', 'nyota_ii_participants',
                  'nyota_iii_participants', 'zizi_participants', 'shina_participants', 'tawi_participants',
                  'mwanzo_participants', 'mwangaza_participants', 'kilele_participants',
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
            Fieldset('Add a Badge camp event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('examiner', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('sub_county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('support_staff', css_class='form-group col-md-6 mb-0'),

                     ),
                     TabHolder(
                         Tab('Sungura Scouts',
                             Row(
                                 Column('nyota_i_participants', css_class='form-group col-md-6 mb-0'),
                                 Column('nyota_ii_participants', css_class='form-group col-md-6 mb-0'),
                                 Column('nyota_iii_participants', css_class='form-group col-md-6 mb-0'),
                                 css_class='form-row'
                             ),
                             ),
                         Tab('Chipukizi Scouts',
                             Row(
                                 Column('zizi_participants', css_class='form-group col-md-6 mb-0'),
                                 Column('shina_participants', css_class='form-group col-md-6 mb-0'),
                                 Column('tawi_participants', css_class='form-group col-md-6 mb-0'),
                                 css_class='form-row'
                             ),
                             ),
                         Tab('Mwamba Scouts',
                             Row(
                                 Column('mwanzo_participants', css_class='form-group col-md-6 mb-0'),
                                 Column('mwangaza_participants', css_class='form-group col-md-6 mb-0'),
                                 Column('kilele_participants', css_class='form-group col-md-6 mb-0'),
                                 css_class='form-row'
                             ),
                             ),
                     ),
                     # Column('badges', css_class='form-group col-md-6 mb-0'),
                     css_class='form-row'
                     ),
            Fieldset('',
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


class ParkHolidayForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='Park Holiday'))
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(ParkHoliday._meta.get_field('sub_county'),
                                                                  auto_admin_site),
                                        queryset=SubCountyQ)
    examiner = forms.ModelChoiceField(widget=AutocompleteSelect(ParkHoliday._meta.get_field('examiner'),
                                                                auto_admin_site),
                                      queryset=ScoutLeaderQ,
                                      help_text="""Only active Scout Leaders with training level of
                                      Two Beads and above are valid options""")
    support_staff = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(ParkHoliday._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ, required=False)
    participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(ParkHoliday._meta.get_field('participants'), auto_admin_site),
        queryset=ScoutQ)
    badges = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(ParkHoliday._meta.get_field('badges'), auto_admin_site),
        queryset=Badge.objects.all())
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ParkHoliday
        fields = ['badges', 'examiner', 'support_staff', 'participants',
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
            Fieldset('Add a Park Holiday event',
                     HTML("""
                        <br>
                        """
                          ),
                     Row(
                         Column('examiner', css_class='form-group col-md-6 mb-0'),
                         Column('report', css_class='form-group col-md-6 mb-0'),
                         Column('start_date', css_class='form-group col-md-6 mb-0'),
                         Column('end_date', css_class='form-group col-md-6 mb-0'),
                         Column('sub_county', css_class='form-group col-md-6 mb-0'),
                         Column('venue_name', css_class='form-group col-md-6 mb-0'),
                         Column('support_staff', css_class='form-group col-md-6 mb-0'),
                         Column('participants', css_class='form-group col-md-6 mb-0'),
                         Column('badges', css_class='form-group col-md-6 mb-0'),
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


class PLCForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='PLC'))
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(PLC._meta.get_field('sub_county'), auto_admin_site),
                                        queryset=SubCountyQ)
    course_director = forms.ModelChoiceField(widget=AutocompleteSelect(PLC._meta.get_field('course_director'),
                                                                       auto_admin_site),
                                             queryset=ScoutLeaderQ,
                                             help_text="""Only active Scout Leaders with training level of
                                             Two Beads and above are valid options""")
    support_staff = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PLC._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ, required=False)
    participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(PLC._meta.get_field('participants'), auto_admin_site),
        queryset=ScoutQ)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = PLC
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
            Fieldset('Add a PLC event',
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


class RMForm(forms.ModelForm):
    report = forms.FileField(widget=forms.FileInput(), help_text=report_template(model='Rover Mate'))
    sub_county = forms.ModelChoiceField(widget=AutocompleteSelect(RM._meta.get_field('sub_county'), auto_admin_site),
                                        queryset=SubCountyQ)
    course_director = forms.ModelChoiceField(widget=AutocompleteSelect(RM._meta.get_field('course_director'),
                                                                       auto_admin_site),
                                             queryset=ScoutLeaderQ,
                                             help_text="""Only active Scout Leaders with training level of
                                      Two Beads and above are valid options""")
    support_staff = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(RM._meta.get_field('support_staff'), auto_admin_site),
        queryset=ScoutLeaderQ, required=False)
    participants = forms.ModelMultipleChoiceField(
        widget=AutocompleteSelectMultiple(RM._meta.get_field('participants'), auto_admin_site),
        queryset=ScoutQ)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = RM
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
            Fieldset('Add a Rover Mate event',
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
