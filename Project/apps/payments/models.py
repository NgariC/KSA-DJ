from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.urls import reverse

from apps.core.project_requirements.utilities import mobile_num_regex
from apps.registrations.models import Unit, Scout, ScoutLeader
from apps.training.models import ITC, PTC
from apps.youth_programme.models import Investiture, BadgeCamp, ParkHoliday, PLC, RM


def payments_limit():
    return Q(model='unit') | Q(model='scout') | Q(model='scoutleader') | Q(model='itc') | Q(model='ptc') | \
           Q(model='investitures') | Q(model='badgecamp') | Q(model='parkholiday') | Q(model='plc') | \
           Q(model='rovermate')


class PaymentsList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    ref_number = models.CharField(max_length=16, editable=False)
    paid = models.BooleanField('Payments Done', default=False, db_index=True)
    phone_number = models.CharField(validators=[mobile_num_regex], max_length=13,
                                    help_text='The phone number will be used to make payments')
    units = models.ManyToManyField(Unit, related_name='%(class)s_units', blank=True, limit_choices_to=Q(active=False))
    scouts = models.ManyToManyField(Scout, related_name='%(class)s_scout', blank=True, limit_choices_to=Q(active=False))
    scout_leaders = models.ManyToManyField(ScoutLeader, related_name='%(class)s_scout_leaders', blank=True,
                                           limit_choices_to=Q(active=False))
    itcs = models.ManyToManyField(ITC, related_name='%(class)s_itcs', blank=True, limit_choices_to=Q(payments=False))
    ptcs = models.ManyToManyField(PTC, related_name='%(class)s_ptcs', blank=True, limit_choices_to=Q(payments=False))
    investitures = models.ManyToManyField(Investiture, related_name='%(class)s_investitures', blank=True,
                                          limit_choices_to=Q(payments=False))
    badge_camps = models.ManyToManyField(BadgeCamp, related_name='%(class)s_badge_camps', blank=True,
                                         limit_choices_to=Q(payments=False))
    park_holidays = models.ManyToManyField(ParkHoliday, related_name='%(class)s_park_holidays', blank=True,
                                           limit_choices_to=Q(payments=False))
    plcs = models.ManyToManyField(PLC, related_name='%(class)s_plcs', blank=True, limit_choices_to=Q(payments=False))
    rover_mates = models.ManyToManyField(RM, related_name='%(class)s_rover_mates', blank=True,
                                         limit_choices_to=Q(payments=False))
    units_paid_for = models.ManyToManyField(Unit, blank=True)
    scouts_paid_for = models.ManyToManyField(Scout, blank=True)
    scout_leaders_paid_for = models.ManyToManyField(ScoutLeader, blank=True)
    itcs_paid_for = models.ManyToManyField(ITC, blank=True)
    ptcs_paid_for = models.ManyToManyField(PTC, blank=True)
    investitures_paid_for = models.ManyToManyField(Investiture, blank=True)
    badge_camps_paid_for = models.ManyToManyField(BadgeCamp, blank=True)
    park_holidays_paid_for = models.ManyToManyField(ParkHoliday, blank=True)
    plcs_paid_for = models.ManyToManyField(PLC, blank=True)
    rover_mates_paid_for = models.ManyToManyField(RM, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.ref_number = 0
        elif len(str(self.pk)) == 1:
            self.ref_number = hex(int(f"1111{self.pk}"))
        elif len(str(self.pk)) == 2:
            return f"000{self.pk}"
        elif len(str(self.pk)) == 3:
            return f"00{self.pk}"
        elif len(str(self.pk)) == 4:
            return f"0{self.pk}"
        else:
            return f"{self.pk}"
        super().save(*args, **kwargs)

    @property
    def investiture_total(self):
        return sum(
            i.cert_amount for i in self.investitures_paid_for.all()) if self.investitures_paid_for.exists() else 0

    @property
    def badge_camp_total(self):
        return sum(i.cert_amount for i in self.badge_camps_paid_for.all()) if self.badge_camps_paid_for.exists() else 0

    @property
    def park_holidays_total(self):
        return sum(
            i.cert_amount for i in self.park_holidays_paid_for.all()) if self.park_holidays_paid_for.exists() else 0

    @property
    def plc_total(self):
        return sum(i.cert_amount for i in self.plcs_paid_for.all()) if self.plcs_paid_for.exists() else 0

    @property
    def rover_mate_total(self):
        return sum(i.cert_amount for i in self.rover_mates_paid_for.all()) if self.rover_mates_paid_for.exists() else 0

    @property
    def itc_total(self):
        return sum(i.cert_amount for i in self.itcs_paid_for.all()) if self.itcs_paid_for.exists() else 0

    @property
    def ptc_total(self):
        return sum(i.cert_amount for i in self.ptcs_paid_for.all()) if self.ptcs_paid_for.exists() else 0

    @property
    def total(self):
        units_t = self.units_paid_for.count() * 500 if self.units_paid_for.exists() else 0

        if self.scouts_paid_for.exists():
            scouts_t = self.scouts_paid_for.count() * 100
        else:
            scouts_t = 0
        if self.scout_leaders_paid_for.exists():
            scout_leaders_t = sum(i.reg_amount for i in self.scout_leaders_paid_for.all())
        else:
            scout_leaders_t = 0
        if self.investitures_paid_for.exists():
            investitures_t = sum(i.cert_amount for i in self.investitures_paid_for.all())
        else:
            investitures_t = 0
        if self.badge_camps_paid_for.exists():
            badge_camps_t = sum(i.cert_amount for i in self.badge_camps_paid_for.all())
        else:
            badge_camps_t = 0
        if self.park_holidays_paid_for.exists():
            park_holidays_t = sum(i.cert_amount for i in self.park_holidays_paid_for.all())
        else:
            park_holidays_t = 0
        if self.plcs_paid_for.exists():
            plcs_t = sum(i.cert_amount for i in self.plcs_paid_for.all())
        else:
            plcs_t = 0
        if self.rover_mates_paid_for.exists():
            rover_mates_t = sum(i.cert_amount for i in self.rover_mates_paid_for.all())
        else:
            rover_mates_t = 0
        if self.itcs_paid_for.exists():
            itcs_t = sum(i.cert_amount for i in self.itcs_paid_for.all())
        else:
            itcs_t = 0
        if self.ptcs_paid_for.exists():
            ptcs_t = sum(i.cert_amount for i in self.ptcs_paid_for.all())
        else:
            ptcs_t = 0
        return sum([units_t, scouts_t, scout_leaders_t, itcs_t, ptcs_t, investitures_t, badge_camps_t,
                    park_holidays_t, plcs_t, rover_mates_t])

    def __str__(self):
        return f"{self.user} Total Amount: {self.total} Ref Number : {self.ref_number}"

    def get_absolute_url(self):
        return reverse('payments:payments', kwargs={'pk': self.pk})


class LNMOnline(models.Model):
    CheckoutRequestID = models.CharField(max_length=50, blank=True, null=True)
    MerchantRequestID = models.CharField(max_length=20, blank=True, null=True)
    ResultCode = models.IntegerField(blank=True, null=True)
    ResultDesc = models.CharField(max_length=120, blank=True, null=True)
    Amount = models.FloatField(blank=True, null=True)
    MpesaReceiptNumber = models.CharField(max_length=15, blank=True, null=True)
    Balance = models.CharField(max_length=12, blank=True, null=True)
    TransactionDate = models.DateTimeField(blank=True, null=True)
    PhoneNumber = models.CharField(max_length=13, blank=True, null=True)

    def post_save(self, instance, created, using=None, **kwargs):
        payment = PaymentsList.objects.get(ref_number=instance.TransactionDesc)
        if created:
            payment.paid = True
            payment.save()


class C2BPayments(models.Model):
    TransactionType = models.CharField(max_length=12, blank=True, null=True)
    TransID = models.CharField(max_length=12, blank=True, null=True)
    TransTime = models.CharField(max_length=14, blank=True, null=True)
    TransAmount = models.CharField(max_length=12, blank=True, null=True)
    BusinessShortCode = models.CharField(max_length=6, blank=True, null=True)
    BillRefNumber = models.CharField(max_length=20, blank=True, null=True)
    InvoiceNumber = models.CharField(max_length=20, blank=True, null=True)
    OrgAccountBalance = models.CharField(max_length=12, blank=True, null=True)
    ThirdPartyTransID = models.CharField(max_length=20, blank=True, null=True)
    MSISDN = models.CharField(max_length=12, blank=True, null=True)
    FirstName = models.CharField(max_length=20, blank=True, null=True)
    MiddleName = models.CharField(max_length=20, blank=True, null=True)
    LastName = models.CharField(max_length=20, blank=True, null=True)


class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, limit_choices_to=payments_limit, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    ref_number = models.CharField(max_length=16, editable=False)
    paid = models.BooleanField('Payments Done', default=False, db_index=True)
    phone_number = models.CharField(validators=[mobile_num_regex], max_length=13,
                                    help_text='The phone number will be used to make payments')
    amount_paid = models.PositiveIntegerField()
