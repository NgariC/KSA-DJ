from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User, EmailActivation


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_action = reverse_lazy('index')
        # self.helper.form_method = 'POST'
        self.helper.form_id = 'user-form'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.TextInput(attrs={
                'hx-get': reverse_lazy('check-email'),
                'hx-target': '#div_id_email',
                'hx-trigger': 'keyup'
            })
        }


class CustomLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(label="Password",
                               strip=False,
                               widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}), )
    error_messages = {
        "invalid_login": _("Please enter a correct %(email)s and password. "
                           "Note that both fields may be case-sensitive."),
        "inactive": _("This account is inactive. Contact the administrator for more information about your account"),
    }

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["email"].max_length = username_max_length
        self.fields["email"].widget.attrs["maxlength"] = username_max_length
        if self.fields["email"].label is None:
            self.fields["email"].label = capfirst(self.username_field.verbose_name)

        self.helper = FormHelper(self)
        self.helper.form_id = 'user-form'
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Fieldset('Login Form',
                     'email',
                     'password',
                     ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='primaryAction'),
            )
        )

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check active/
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                self._extracted_from_clean_12(email)
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError(_("Invalid credentials"))
        login(request, user)
        self.user = user
        return data

    # TODO Rename this here and in `clean`
    def _extracted_from_clean_12(self, email):
        ## not active, check email activation
        link = reverse("account:resend-activation")
        reconfirm_msg = _("""Go to <a href='{resend_link}'>
                resend confirmation email</a>.
                """).format(resend_link=link)
        confirm_email = EmailActivation.objects.filter(email=email)
        is_confirmable = confirm_email.confirmable().exists()
        if is_confirmable:
            msg1 = _(f"Please check your email to confirm your account or {reconfirm_msg.lower()}")

            raise forms.ValidationError(mark_safe(msg1))
        if email_confirm_exists := EmailActivation.objects.email_exists(email).exists():
            msg2 = _(f"Email not confirmed. {reconfirm_msg}")
            raise forms.ValidationError(mark_safe(msg2))
        if not is_confirmable:
            raise forms.ValidationError(_("This user is inactive."))

    # def clean(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #
    #     if email is not None and password:
    #         self.user_cache = authenticate(
    #             self.request, username=email, password=password
    #         )
    #         if self.user_cache is None:
    #             raise self.get_invalid_login_error()
    #         else:
    #             self.confirm_login_allowed(self.user_cache)
    #
    #     return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )
        if not user.email_confirmed:
            link = reverse("resend-activation")
            reconfirm_msg = _("""Go to <a href='{resend_link}'> resend confirmation email</a>.""").format(
                resend_link=link)
            msg1 = _(f"Please check your email to confirm your account or {reconfirm_msg.lower()}")

            raise ValidationError(
                forms.ValidationError(mark_safe(msg1)),
                code=_("email not confirmed"),
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code=_("invalid_login"),
            params={"email": self.username_field.verbose_name},
        )


class ReactivateEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.email_exists(email).exists():
            msg = _("""This email does not exists, would you like to <a href="{link}">Sign Up</a>?
            """).format(link=reverse("sign_up"))
            raise forms.ValidationError(mark_safe(msg))
        return email
