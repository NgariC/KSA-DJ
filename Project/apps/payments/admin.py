from django.contrib import admin

from apps.payments.models import LNMOnline, C2BPayments, PaymentsList, Payments
from apps.payments.utils import PaidForList


@admin.register(LNMOnline)
class LNMOnlineAdmin(admin.ModelAdmin):
    list_display = ("PhoneNumber", "Amount", "MpesaReceiptNumber", "TransactionDate")


@admin.register(C2BPayments)
class C2BPaymentsAdmin(admin.ModelAdmin):
    list_display = ("MSISDN", "TransAmount", "TransID", "TransTime")


@admin.register(PaymentsList)
class PaymentsListAdmin(PaidForList, admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.user = request.user
        super().save_model(request, obj, form, change)

    list_display = 'ref_number', 'user', 'total'
    autocomplete_fields = ('units', 'scouts', 'scout_leaders', 'itcs', 'ptcs', 'investitures', 'badge_camps',
                           'park_holidays', 'plcs', 'rover_mates',
                           'units_paid_for', 'scouts_paid_for', 'scout_leaders_paid_for',
                           'itcs_paid_for', 'ptcs_paid_for',
                           'investitures_paid_for', 'badge_camps_paid_for', 'park_holidays_paid_for',
                           'plcs_paid_for', 'rover_mates_paid_for'
                           )

    def get_readonly_fields(self, request, obj=None):
        return ['units_list', 'scouts_list', 'scout_leaders_list', 'itcs_list', 'ptcs_list', 'investitures_list',
                'badge_camps_list', 'park_holidays_list', 'plcs_list', 'rover_mates_list', 'ref_number']

    def get_fieldsets(self, request, obj=None):
        return (("Phone number to do the MPESA payment", {'fields': ('phone_number',)}),
                ("Registration", {'fields': (('units', 'scouts'), 'scout_leaders',)}),
                ('Training Programme Events', {'fields': (('itcs', 'ptcs'),)}), ('Youth Programme Events', {
            'fields': (('investitures', 'badge_camps'), ('park_holidays', 'plcs'), 'rover_mates')}), (
                "Units, Scouts & Scout Leaders paid for",
                {'fields': ('units_list', 'scouts_list', 'scout_leaders_list')}),
                ('Training Programme Events paid for', {'fields': ('itcs_list', 'ptcs_list')}), (
                'Youth Programme Events paid for', {'fields': (
                'investitures_list', 'badge_camps_list', 'park_holidays_list', 'plcs_list', 'rover_mates_list')}), (
                'Payments',
                {'classes': ('wide',), 'fields': ('paid', 'ref_number')})) if request.user.is_superuser else (
        ("Phone number to do the MPESA payment", {'fields': ('phone_number',)}),
        ("Registration", {'fields': (('units', 'scouts'), 'scout_leaders')}),
        ('Training Programme Events', {'fields': (('itcs', 'ptcs'),)}), ('Youth Programme Events', {
            'fields': (('investitures', 'badge_camps'), ('park_holidays', 'plcs'), 'rover_mates')}), (
        "Units, Scouts & Scout Leaders paid for",
        {'fields': (('units_paid_for', 'scouts_paid_for'), 'scout_leaders_paid_for')}),
        ('Training Department Events paid for', {'fields': (('itcs_paid_for', 'ptcs_paid_for'),)}), (
        'Youth Programme Department Events paid for', {'fields': (
        ('investitures_paid_for', 'badge_camps_paid_for'), ('park_holidays_paid_for', 'plcs_paid_for'),
        'rover_mates_paid_for')}), ('Payments', {'classes': ('wide',), 'fields': ('paid', 'ref_number')}))


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ("user", 'content_type', 'object_id', 'content_object')


admin.site.register(Payments, PaymentsAdmin)
