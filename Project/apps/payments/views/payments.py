from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from apps.payments.forms import PaymentsF
from apps.payments.models import PaymentsList
from apps.payments.views.mpesa import lipa_na_mpesa, simulate_c2b_transaction


def get_obect_or_404(Post, publish__year, publish__month, publish__day, slug, author):
    pass


class UpdatePayments(LoginRequiredMixin, FormMessagesMixin, generic.UpdateView):
    form_class = PaymentsF
    model = PaymentsList
    template_name = 'payments/payments_form.html'

    def post(self, request, *args, **kwargs):
        save_action = super().post(request, *args, **kwargs)
        if "express" in request.POST:
            lipa_na_mpesa()
        elif 'offline' in request.POST:
            simulate_c2b_transaction()
        return save_action

    def get_success_url(self):
        return reverse_lazy('payments:payments', kwargs={'pk': self.object.pk})

    def get_form_valid_message(self):
        return u"{0} {1} successfully updated!".format(self.object, self.model.__name__)

    def get_form_invalid_message(self):
        return u"{0} not updated! Please correct the error below.".format(self.object)