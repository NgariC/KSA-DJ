from django.urls import path, re_path

from apps.payments import views

app_name = 'payments'

urlpatterns = [
    path('mpesa-payments', views.AddPayments.as_view(), name='mpesa_payments'),
    # path('payments-complete', views.PaymentsComplete.as_view(), name='payments_complete'),

    re_path('payments/(?P<pk>\d+)', views.PaymentsDetail.as_view(), name='payments'),

    re_path('mpesa/(?P<pk>\d+)', views.UpdatePayments.as_view(), name='mpesa'),
]