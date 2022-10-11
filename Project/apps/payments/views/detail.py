from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from apps.payments.models import PaymentsList


class PaymentsDetail(LoginRequiredMixin, generic.DetailView):
    model = PaymentsList
