from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic

from apps.payments.forms import RegistrationForm, PaymentsForm
from apps.payments.models import PaymentsList


class AddPayments(LoginRequiredMixin, generic.CreateView):
    model = PaymentsList
    template_name = 'form.html'

    def get_form_class(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return PaymentsForm
        if not user.sub_county:
            raise PermissionDenied()
        level = user.rank.level
        if level == 'National':
            return PaymentsForm
        elif level == 'Regional':
            return PaymentsForm
        elif level == 'County':
            return PaymentsForm
        elif level == 'SubCounty':
            return PaymentsForm
        else:
            if not user.unit:
                raise PermissionDenied()
            else:
                return RegistrationForm

    def form_valid(self, form):
        payment = form.save(commit=False)
        payment.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payments:mpesa', kwargs={'pk': self.object.pk})
