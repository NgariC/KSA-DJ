from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Column, HTML, Row, Submit, ButtonHolder
from django import forms

from apps.payments.models import PaymentsList


class PaymentsF(forms.ModelForm):

    class Meta:
        model = PaymentsList
        fields = ['phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['phone_number'].initial = '+2547'
        self.helper.form_id = 'id-scoutForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal form-bordered form-inline'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-7'
        self.helper.layout = Layout(
            Fieldset('',
                     HTML("""
                     </br></br></br>
                        <h4>Phone number used for MPESA payments</h4>
                        """
                          ),
                     Row(
                         Column('phone_number', css_class='form-group col-md-12 mb-0'),
                         css_class='form-row'
                     ),
                     ),
            ButtonHolder(
                Submit('express', 'Submit and Add Another', css_class='another primaryAction'),
                Submit('offline', 'Submit', css_class='itself primaryAction'),
            )
        )
