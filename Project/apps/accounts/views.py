from crispy_forms.utils import render_crispy_form
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import CreateView
from django.views.generic.edit import FormMixin, UpdateView

from apps.accounts.forms import RegisterForm, ReactivateEmailForm, CustomLoginForm
from apps.accounts.mixins import NextUrlMixin, RequestFormAttachMixin
from apps.accounts.models import EmailActivation, User
from apps.accounts.utils import DisAllowLoggedInUser
from apps.core.forms import UserForm


class CustomLoginView(DisAllowLoggedInUser, NextUrlMixin, RequestFormAttachMixin, LoginView):
    form_class = CustomLoginForm
    template_name = 'form.html'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class SignUp(DisAllowLoggedInUser, CreateView):
    template_name = 'registration/sign_up.html'
    model = get_user_model()
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        ctx = {}
        ctx |= csrf(request)
        form_html = render_crispy_form(self.get_form(), context=ctx)
        return HttpResponse(form_html)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class AccountEmailActivateView(FormMixin, View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Please login.")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("login")
        context = {'form': self.get_form(), 'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # create form to receive an email
        return self.form_valid(form) if form.is_valid() else self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key}
        return render(self.request, 'registration/activation-error.html', context)


def view_profile(request, pk=None):
    user = User.objects.get(pk=pk) if pk else request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html', args)


class UserUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'form.html'
    success_url = '/profile'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['link_to_scout_leader'] = self.request.user.link_to_scout_leader
        return initial

    def get_success_message(self, cleaned_data):
        return u"{0} updated!".format(self.object)
