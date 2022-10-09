from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.project_requirements.utilities import active_ptc_and_above_limit, active_limit, active_invested_limit, \
    validate_file_extension

from apps.geoposition.fields import GeopositionField
from apps.jurisdictions.models import SubCounty
from apps.registrations.models import Scout, ScoutLeader

from apps.youth_programme.managers import InvestitureManager, BadgeCampManager, CManager


class Event(models.Model):
    report = models.FileField(_('report'), upload_to='Youth Programme Department/%Y/%m',
                              validators=[validate_file_extension])
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))
    venue_name = models.CharField(_("Venue Name"), max_length=50)
    venue = GeopositionField(_('venue'))
    payments = models.BooleanField(_('payments'), default=False, db_index=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT, db_index=True)
    director = models.ForeignKey(ScoutLeader, on_delete=models.PROTECT, related_name='%(class)s_director',
                                 null=True, blank=True)
    staff = models.ManyToManyField(ScoutLeader, related_name='%(class)s_staff', blank=True)
    trainees = models.ManyToManyField(Scout, related_name='%(class)s_trainees', blank=True)
    support_staff = models.ManyToManyField(ScoutLeader, related_name='%(class)s_trainers',
                                           limit_choices_to=active_limit,
                                           help_text=_("Limited to only active Scout Leaders"))

    class Meta:
        abstract = True

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_('Start date should be before end date.'))

    @property
    def cert_amount(self):
        trainees = self.trainees.count()
        return trainees * 50


class Badge(models.Model):
    SECTION = (
        ('Sungura', _('Sungura')),
        ('Chipukizi', _('Chipukizi')),
        ('Mwamba', _('Mwamba')),
        ('Jasiri', _('Jasiri')),
    )
    name = models.CharField(_('name'), primary_key=True, max_length=100)
    section = models.CharField(_('sections'), max_length=10, choices=SECTION, db_index=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name} {self.section}'


class Investiture(Event):
    investor = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT,
        limit_choices_to=active_ptc_and_above_limit,
        help_text="Limited to active Scout Leaders with training level of PTC and above")
    participants = models.ManyToManyField(
        Scout, related_name='%(class)s_participants', blank=True,
        limit_choices_to=Q(active=True) & Q(investiture=False) & (
                Q(section='Sungura') | Q(section='Chipukizi') | Q(section='Mwamba')))
    jasiri_participants = models.ManyToManyField(
        Scout, related_name='%(class)s_jasiri_participants', blank=True,
        limit_choices_to=Q(active=True) & Q(section='Jasiri') & Q(jasiri_investiture=False))

    objects = InvestitureManager()

    class Meta:
        unique_together = ['venue_name', 'start_date', 'sub_county']
        permissions = [('can_verify_Investiture_payments', 'Can verify Investiture payments'),
                       ('can_edit_Investiture_trainees', 'Can edit Investiture Trainees')]

    def save(self, *args, **kwargs):
        if self.investor:
            self.director = self.investor
        if self.director and self.investor is None:
            self.investor = self.director
        self.end_date = self.start_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.venue_name} - {self.start_date}'

    def get_absolute_url(self):
        return reverse('youth_programme:i_detail', kwargs={'pk': self.pk})


class BadgeCamp(Event):
    examiner = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT,
        limit_choices_to=active_ptc_and_above_limit,
        help_text="Limited to active Scout Leaders with training level of PTC and above")
    nyota_i_participants = models.ManyToManyField(
        Scout, related_name='%(class)s_nyota_i_participants',
        limit_choices_to=Q(active=True) & Q(investiture=True) & Q(section='Sungura') & Q(nyota_i='False'))
    nyota_ii_participants = models.ManyToManyField(
        Scout, related_name='%(class)s_nyota_ii_participants',
        limit_choices_to=Q(active=True) & Q(investiture=True) & Q(section='Sungura') & Q(nyota_i='True') &
                         Q(nyota_ii='False'))
    nyota_iii_participants = models.ManyToManyField(
        Scout, related_name='%(class)s_nyota_iii_participants',
        limit_choices_to=Q(active=True) & Q(investiture=True) & Q(section='Sungura') & Q(nyota_i='True') &
                         Q(nyota_ii='True') & Q(nyota_iii='False'))
    zizi_participants = models.ManyToManyField(
        Scout, related_name='%(class)s_zizi_participants',
        limit_choices_to=Q(active=True) & Q(investiture=True) & Q(section='Chipukizi') & Q(zizi='False'))
    shina_participants = models.ManyToManyField(
        Scout, related_name='%(class)s_shina_participants',
        limit_choices_to=Q(active=True) & Q(investiture=True) & Q(section='Chipukizi') & Q(zizi='True') &
                         Q(shina='False'))
    tawi_participants = models.ManyToManyField(
        Scout, related_name='%(class)s_tawi_participants',
        limit_choices_to=Q(active=True) & Q(investiture=True) & Q(section='Chipukizi') & Q(zizi='True') &
                         Q(shina='True') & Q(tawi='False'))
    mwanzo_participants = models.ManyToManyField(
        Scout, related_name='%(class)s_mwanzo_participants',
        limit_choices_to=Q(active=True) & Q(investiture=True) & Q(section='Mwamba') & Q(mwanzo='False'))
    mwangaza_participants = models.ManyToManyField(
        Scout, related_name='%(class)s_mwangaza_participants',
        limit_choices_to=Q(active=True) & Q(investiture=True) & Q(section='Mwamba') & Q(mwanzo='True') &
                         Q(mwangaza='False'))
    kilele_participants = models.ManyToManyField(
        Scout, related_name='%(class)s_kilele_participants',
        limit_choices_to=Q(active=True) & Q(investiture=True) & Q(section='Mwamba') & Q(mwanzo='True') &
                         Q(mwangaza='True') & Q(kilele='False'))
    # participants = models.ManyToManyField(
    #     Scout, related_name='%(class)s_participants',
    #     limit_choices_to=Q(active=True) & Q(investiture=True) & (Q(section='Chipukizi') | Q(section='Mwamba')))
    # badges = models.ManyToManyField(Badge, limit_choices_to=Q(section='Chipukizi') | Q(section='Mwamba'))

    objects = BadgeCampManager()

    class Meta:
        unique_together = ['venue_name', 'start_date', 'sub_county']
        permissions = [('can_verify_BadgeCamp_payments', 'Can verify BadgeCamp payments'),
                       ('can_edit_BadgeCamp_trainees', 'Can edit BadgeCamp Trainees')]

    def save(self, *args, **kwargs):
        if self.examiner:
            self.director = self.examiner
        if self.director and self.examiner is None:
            self.examiner = self.director
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.venue_name} - {self.start_date}'

    def get_absolute_url(self):
        return reverse('youth_programme:bc_detail', kwargs={'pk': self.pk})


class ParkHoliday(Event):
    examiner = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT,
        limit_choices_to=active_ptc_and_above_limit,
        help_text="Limited to active Scout Leaders with training level of PTC and above")
    participants = models.ManyToManyField(
        Scout, related_name='%(class)s_participants',
        limit_choices_to=Q(active=True) & Q(investiture=True) & Q(section='Sungura'))
    badges = models.ManyToManyField(Badge, limit_choices_to=Q(section='Sungura'))

    objects = BadgeCampManager()

    class Meta:
        unique_together = ['venue_name', 'start_date', 'sub_county']
        permissions = [('can_verify_ParkHoliday_payments', 'Can verify ParkHoliday payments'),
                       ('can_edit_ParkHoliday_trainees', 'Can edit ParkHoliday Trainees')]
        verbose_name = "Park Holiday"

    def save(self, *args, **kwargs):
        if self.examiner:
            self.director = self.examiner
        if self.director and self.examiner is None:
            self.examiner = self.director
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.venue_name} - {self.start_date}'

    def get_absolute_url(self):
        return reverse('youth_programme:ph_detail', kwargs={'pk': self.pk})


class PLC(Event):
    course_director = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT,
        limit_choices_to=active_ptc_and_above_limit,
        help_text="Limited to active Scout Leaders with training level of PTC and above")
    participants = models.ManyToManyField(
        Scout, related_name='%(class)s_participants',
        limit_choices_to=active_invested_limit)

    objects = CManager()

    class Meta:
        unique_together = ['venue_name', 'start_date', 'sub_county']
        permissions = [('can_verify_PLC_payments', 'Can verify PLC payments'),
                       ('can_edit_PLC_trainees', 'Can edit PLC Trainees')]
        verbose_name = _("Patrol Leaders Course")

    def save(self, *args, **kwargs):
        if self.course_director:
            self.director = self.course_director
        if self.director and self.course_director is None:
            self.course_director = self.director
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.venue_name} - {self.start_date}'

    def get_absolute_url(self):
        return reverse('youth_programme:plc_detail', kwargs={'pk': self.pk})


class RM(Event):
    course_director = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT,
        limit_choices_to=active_ptc_and_above_limit,
        help_text=_("Limited to active Scout Leaders with training level of PTC and above"))
    participants = models.ManyToManyField(
        Scout, related_name='%(class)s_participants',
        limit_choices_to=Q(active=True) & Q(section='Jasiri') & Q(jasiri_investiture=True))

    objects = CManager()

    class Meta:
        unique_together = ['venue_name', 'start_date', 'sub_county']
        permissions = [('can_verify_Rover_Mate_payments', 'Can verify Rover Mate payments'),
                       ('can_edit_Rover_Mate_trainees', 'Can edit Rover Mate Trainees')]
        verbose_name = "Rover Mate Course"

    def save(self, *args, **kwargs):
        if self.course_director:
            self.director = self.course_director
        if self.director and self.course_director is None:
            self.course_director = self.director
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.venue_name} - {self.start_date}'

    def get_absolute_url(self):
        return reverse('youth_programme:rm_detail', kwargs={'pk': self.pk})
