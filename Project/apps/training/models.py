from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from tinymce.models import HTMLField

from apps.core.project_requirements.utilities import active_limit, active_four_beads_limit, \
    active_three_beads_and_above_limit, active_two_beads_and_above_limit, active_ptc_and_above_limit, \
    validate_file_extension

from apps.geoposition.fields import GeopositionField
from apps.training.managers import SLEventManager, SLLEventManager, WBIIIManager, WBIManager

from apps.jurisdictions.models import SubCounty, County
from apps.registrations.models import ScoutLeader, Unit


class Event(models.Model):
    report = models.FileField(upload_to='Training Department/%Y/%m', validators=[validate_file_extension])
    start_date = models.DateField()
    end_date = models.DateField()
    venue_name = models.CharField("Venue Name", max_length=50)
    venue = GeopositionField()
    payments = models.BooleanField(default=False, db_index=True)
    director = models.ForeignKey(ScoutLeader, on_delete=models.PROTECT, related_name='%(class)s_director',
                                 null=True, blank=True)
    staff = models.ManyToManyField(ScoutLeader, related_name='%(class)s_staff', blank=True)
    trainees = models.ManyToManyField(ScoutLeader, related_name='%(class)s_trainees', blank=True)

    class Meta:
        abstract = True

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError('Start date should be before end date.')

    def save(self, *args, **kwargs):
        if self.course_director:
            self.director = self.course_director
        if self.director and self.course_director is None:
            self.course_director = self.director
        super().save(*args, **kwargs)

    @property
    def cert_amount(self):
        trainees = self.trainees.count()
        return trainees * 100


class ITC(Event):
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT, db_index=True)
    course_director = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT, limit_choices_to=active_two_beads_and_above_limit,
        help_text="Only active Scout Leaders with training level of Two Beads and above are valid options")
    support_staff = models.ManyToManyField(
        ScoutLeader, related_name='%(class)s_trainers', limit_choices_to=active_ptc_and_above_limit)
    participants = models.ManyToManyField(
        ScoutLeader, related_name='%(class)s_participants',
        limit_choices_to=Q(active=True) & Q(training='Not Yet Trained'))

    objects = SLLEventManager()

    class Meta:
        unique_together = ['course_director', 'start_date']
        indexes = [models.Index(fields=['course_director', 'start_date']), ]
        permissions = [('can_verify_ITC_payments', 'Can verify ITC payments'),
                       ('can_edit_ITC_trainees', 'Can edit ITC Trainees')]
        verbose_name = "Introductory training Course"
        verbose_name_plural = "Introductory training Courses"

    def save(self, *args, **kwargs):
        self.end_date = self.start_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.sub_county} - {self.start_date.month}/{self.start_date.year}'

    def get_absolute_url(self):
        return reverse('training:itc_detail', kwargs={'pk': self.pk})


class PTC(Event):
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT, db_index=True)
    course_director = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT, limit_choices_to=active_three_beads_and_above_limit,
        help_text="Limited to active Scout Leaders with training level of Three Beads and above")
    support_staff = models.ManyToManyField(
        ScoutLeader, related_name='%(class)s_trainers', limit_choices_to=active_two_beads_and_above_limit)
    participants = models.ManyToManyField(
        ScoutLeader, related_name='%(class)s_participants', limit_choices_to=Q(active=True) & Q(training='ITC'))

    objects = SLLEventManager()

    class Meta:
        unique_together = ['course_director', 'start_date']
        indexes = [models.Index(fields=['course_director', 'start_date']), ]
        permissions = [('can_verify_PTC_payments', 'Can verify PTC payments'),
                       ('can_edit_PTC_trainees', 'Can edit PTC Trainees')]
        verbose_name = "PTC"

    def __str__(self):
        return f'{self.sub_county} - {self.start_date.month}/{self.start_date.year}'

    def get_absolute_url(self):
        return reverse('training:ptc_detail', kwargs={'pk': self.pk})


class WBI(models.Model):
    theory_book = models.FileField(upload_to='Woodbadge Theory Books/%Y/%m')
    submission_date = models.DateTimeField(auto_now_add=True, editable=False)
    scout_leader = models.OneToOneField(
        ScoutLeader, on_delete=models.PROTECT,
        limit_choices_to=Q(active=True) & Q(training='PTC'),
        help_text="Only active Scout Leaders with training level of Four Beads are valid options")
    scout_leader_name = models.OneToOneField(ScoutLeader, on_delete=models.PROTECT, null=True, blank=True,
                                             related_name='%(class)s_scout_leader_name')
    marker = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT, null=True, blank=True, related_name='%(class)s_marker',
        limit_choices_to=Q(active=True) & Q(training='PTC'),
        help_text="Only active Scout Leaders with training level of Four Beads are valid options")
    marker_name = models.ForeignKey(ScoutLeader, on_delete=models.PROTECT, null=True, blank=True,
                                    related_name='%(class)s_marker_name')
    comments = HTMLField()
    payments = models.BooleanField(default=False, db_index=True)
    marked = models.BooleanField(default=False, db_index=True)

    objects = WBIManager()

    class Meta:
        permissions = [('can_verify_WoodBadge_I_payments', 'Can verify WoodBadge I payments')]
        verbose_name = "WoodBadge I (Theory)"
        verbose_name_plural = "WoodBadge I (Theories)"

    def save(self, *args, **kwargs):
        if self.scout_leader:
            self.scout_leader_name = self.scout_leader
            self.scout_leader_name.training = 'WB Theory'
            if self.scout_leader_name is None and self.scout_leader_name:
                self.scout_leader_name = self.scout_leader
                self.scout_leader_name.training = 'WB Theory'
        if self.marker:
            self.marker_name = self.marker
            if self.marker_name is None and self.marker_name:
                self.marker_name = self.marker
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.scout_leader_name} - {self.submission_date.month}/{self.submission_date.year}'

    def get_absolute_url(self):
        return reverse('training:wbi_detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.marked and (not self.marker or not self.marker_name):
            raise ValidationError('The theory cannot be marked without a maker.')


class WBII(Event):
    county = models.ForeignKey(County, on_delete=models.PROTECT, db_index=True)
    number = models.PositiveSmallIntegerField('WoodBadge Number')
    course_director = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT,
        limit_choices_to=active_four_beads_limit,
        help_text="Only active Scout Leaders with training level of Four Beads are valid options")
    support_staff = models.ManyToManyField(
        ScoutLeader, related_name='%(class)s_trainers',
        limit_choices_to=active_three_beads_and_above_limit)
    participants = models.ManyToManyField(
        ScoutLeader, related_name='%(class)s_participants', limit_choices_to=Q(active=True) & Q(training='WB Theory'))

    objects = SLEventManager()

    class Meta:
        unique_together = ['course_director', 'start_date']
        indexes = [models.Index(fields=['course_director', 'start_date'])]
        permissions = [('can_verify_WoodBadge_II_payments', 'Can verify WoodBadge II payments'),
                       ('can_edit_WoodBadge_II_trainees', 'Can edit WoodBadge II Trainees')]
        verbose_name = "WoodBadge II (Course)"
        verbose_name_plural = "WoodBadge II (Courses)"

    def __str__(self):
        return f'{self.county} - {self.start_date.month}/{self.start_date.year}'

    def get_absolute_url(self):
        return reverse('training:wbii_detail', kwargs={'pk': self.pk})


class WBIII(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, db_index=True)
    assessment_date = models.DateField(null=True, blank=True)
    assessor = models.ForeignKey(ScoutLeader, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name='%(class)s_assessor',
                                 limit_choices_to=active_three_beads_and_above_limit,
                                 help_text="Only active Scout Leaders with training "
                                           "level of Four Beads are valid options")
    assessor_name = models.ForeignKey(ScoutLeader, on_delete=models.PROTECT, null=True, blank=True,
                                      related_name='%(class)s_assessor_name')
    scout_leader = models.OneToOneField(ScoutLeader, on_delete=models.PROTECT, blank=True,
                                        limit_choices_to=Q(active=True) & Q(training='WB Course'),
                                        help_text="Only active Scout Leaders with training "
                                                  "level of WB Course are valid options")
    scout_leader_name = models.OneToOneField(ScoutLeader, on_delete=models.PROTECT, null=True, blank=True,
                                             related_name='%(class)s_scout_leader_name')
    report = models.FileField(upload_to=' Woodbadge Assessment/%Y/%m')
    venue = GeopositionField()
    payments = models.BooleanField(default=False, db_index=True)
    assessed = models.BooleanField(default=False, db_index=True)

    objects = WBIIIManager()

    class Meta:
        permissions = [('can_verify_WoodBadge_III_payments', 'Can verify WoodBadge III payments')]
        verbose_name = "WoodBadge III (Assessment)"
        verbose_name_plural = "WoodBadge III (Assessments)"

    def save(self, *args, **kwargs):
        if self.assessor:
            self.assessor_name = self.assessor
            if self.assessor_name is None:
                self.assessor_name = self.assessor
        if self.scout_leader:
            self.scout_leader_name = self.scout_leader
            self.scout_leader_name.training = 'WB Assessment'
            if self.scout_leader_name is None:
                self.scout_leader_name = self.scout_leader
                self.scout_leader_name.training = 'WB Assessment'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.scout_leader_name} - {self.unit}'

    def get_absolute_url(self):
        return reverse('training:wbiii_detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.assessed and (not self.assessor or not self.assessor_name):
            raise ValidationError('The Application cannot be marked as assessed without an assessor.')


class ALT(Event):
    county = models.ForeignKey(County, on_delete=models.PROTECT, db_index=True)
    number = models.PositiveSmallIntegerField('ALT Number')
    course_director = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT, limit_choices_to=active_four_beads_limit,
        help_text="Only active Scout Leaders with training level of Four Beads are valid options")
    support_staff = models.ManyToManyField(
        ScoutLeader, related_name='%(class)s_trainers', limit_choices_to=active_four_beads_limit)
    participants = models.ManyToManyField(
        ScoutLeader, related_name='%(class)s_participants', limit_choices_to=Q(active=True) & Q(training='Two Beads'))

    objects = SLEventManager()

    class Meta:
        unique_together = ['course_director', 'start_date']
        indexes = [models.Index(fields=['course_director', 'start_date']), ]
        permissions = [('can_verify_ALT_payments', 'Can verify ALT payments'),
                       ('can_edit_ALT_trainees', 'Can edit ALT Trainees')]
        verbose_name = "ALT"

    def __str__(self):
        return f'{self.county} - {self.start_date.month}/{self.start_date.year}'

    def get_absolute_url(self):
        return reverse('training:alt_detail', kwargs={'pk': self.pk})


class LT(Event):
    county = models.ForeignKey(County, on_delete=models.PROTECT, db_index=True)
    number = models.PositiveSmallIntegerField('LT Number')
    course_director = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT, limit_choices_to=active_four_beads_limit,
        help_text="Only active Scout Leaders with training level of Four Beads are valid options")
    support_staff = models.ManyToManyField(
        ScoutLeader, related_name='%(class)s_trainers', limit_choices_to=active_four_beads_limit)
    participants = models.ManyToManyField(
        ScoutLeader, related_name='%(class)s_participants', limit_choices_to=Q(active=True) & Q(training='Three Beads'))

    objects = SLEventManager()

    class Meta:
        unique_together = ['course_director', 'start_date']
        indexes = [models.Index(fields=['course_director', 'start_date']), ]
        permissions = [('can_verify_LT_payments', 'Can verify LT payments'),
                       ('can_edit_LT_trainees', 'Can edit LT Trainees')]
        verbose_name = "LT"

    def __str__(self):
        return f'{self.county} - {self.start_date.month}/{self.start_date.year}'

    def get_absolute_url(self):
        return reverse('training:lt_detail', kwargs={'pk': self.pk})


class SLSpecialEvent(Event):
    event_name = models.CharField('Event Name', max_length=100, db_index=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT, db_index=True)
    course_director = models.ForeignKey(ScoutLeader, on_delete=models.PROTECT, limit_choices_to=active_limit,
                                        help_text="Only active Scout Leaders are valid options")
    support_staff = models.ManyToManyField(ScoutLeader, related_name='%(class)s_trainers',
                                           limit_choices_to=active_limit,
                                           help_text="Only active Scout Leaders are valid options")
    participants = models.ManyToManyField(ScoutLeader, related_name='%(class)s_participants',
                                          limit_choices_to=active_limit,
                                          help_text="Only active Scout Leaders are valid options")

    objects = SLLEventManager()

    class Meta:
        unique_together = ['course_director', 'start_date']
        indexes = [models.Index(fields=['course_director', 'start_date']), ]
        permissions = [('can_verify_SLSpecialEvent_payments', 'Can verify SLSpecialEvent payments'),
                       ('can_edit_SLSpecialEvent_trainees', 'Can edit SLSpecialEvent Trainees')]
        verbose_name = "Scout Leader Special Event"

    def __str__(self):
        return f'{self.sub_county} - {self.start_date.month}/{self.start_date.year}'

    def get_absolute_url(self):
        return reverse('training:slse_detail', kwargs={'pk': self.pk})
