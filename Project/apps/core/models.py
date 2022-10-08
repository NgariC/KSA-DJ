from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from apps.core.managers import ComingEventManager, ScoutCenterManager
from apps.core.project_requirements.utilities import mobile_num_regex
from apps.geoposition.fields import GeopositionField
from apps.jurisdictions.models import SubCounty, County
from apps.registrations.models import ScoutLeader


class SiteConfig(models.Model):
    key = models.SlugField(_('key'))
    value = models.CharField(_('value'), max_length=200)

    def __str__(self):
        return self.key


class Slide(models.Model):
    title = models.CharField(_('title'), max_length=50, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    image = models.ImageField(_('Slide Image'), upload_to='Slides Images/%Y/%m')
    featured = models.BooleanField(_('featured'), default=False, db_index=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True, db_index=True)

    objects = models.Manager()

    def __str__(self):
        return self.title or str(self.timestamp)


class About(models.Model):
    content = HTMLField()

    objects = models.Manager()

    def __str__(self):
        return str(self.id)


class WeProduce(models.Model):
    title = models.CharField(_('title'), max_length=200)
    content = HTMLField(_('content'), )
    image = models.ImageField(_('Background Image'), upload_to='BackGround Images/%Y/%m')

    objects = models.Manager()

    def __str__(self):
        return self.title


class ScoutingInBrief(models.Model):
    title = models.CharField(_('title'), max_length=200)
    content = HTMLField(_('content'), )

    objects = models.Manager()

    def __str__(self):
        return self.title


class Department(models.Model):
    name = models.CharField(_('department name'), max_length=200)
    description = models.TextField(_('description'))
    icon = models.CharField(_('icon'), max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.name


class ScoutsCenter(models.Model):
    cover_photo = models.ImageField(_('cover photo'), upload_to='Scouts Centers/%Y', null=True, blank=True)
    name = models.CharField(_('camp center name'), max_length=200, db_index=True)
    camp_warden = models.CharField(_('camp warden'), max_length=50, db_index=True)
    email = models.EmailField(_('email'), unique=True)
    phone_number = models.CharField(_('phone number'), validators=[mobile_num_regex], max_length=13)
    description = HTMLField(_('description'), null=True, blank=True)
    services = HTMLField(_('services'), null=True, blank=True)
    payments = HTMLField(_('payments'), null=True, blank=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT, db_index=True)
    exact_place = GeopositionField(_('exact place'), )

    objects = ScoutCenterManager()

    class Meta:
        unique_together = ['name', 'camp_warden', 'sub_county']

    def __str__(self):
        return f'{self.name} -{self.camp_warden} - {self.sub_county}'

    def get_absolute_url(self):
        return reverse('core:sc_detail', kwargs={'pk': self.pk})


class ComingEvent(models.Model):
    event_type = models.CharField(_('Type of Event'), max_length=100, db_index=True)
    start_date = models.DateField(_('start date'), db_index=True)
    end_date = models.DateField(_('end date'), db_index=True)
    requirement = HTMLField(_('Requirement to attend'))
    county = models.ForeignKey(County, on_delete=models.PROTECT)
    venue_name = models.CharField(_('Venue Name'), max_length=50)
    venue = GeopositionField(_('venue'), )
    is_featured = models.BooleanField(_('is featured'), default=False,
                                      help_text='whether the event should be displayed in home page',
                                      db_index=True)
    is_published = models.BooleanField(_('is published'), default=False,
                                       help_text='whether the event should be displayed', db_index=True)
    event_coordinators = models.ManyToManyField(ScoutLeader,
                                                blank=True,
                                                limit_choices_to=Q(active=True),
                                                help_text="Only active Scout Leaders are valid options")
    enable_registration = models.BooleanField(_('enable event registration'), default=False)
    registration_deadline_at = models.DateTimeField(_('allow registration until'), null=True, blank=True, default=None)

    objects = ComingEventManager()

    class Meta:
        permissions = [('can_publish_coming_events', 'Can publish coming events')]
        unique_together = ['event_type', 'start_date', 'venue_name']
        verbose_name = 'Up coming event'
        verbose_name_plural = 'Up coming events'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.event_type} - {self.county}'

    def get_absolute_url(self):
        return reverse('core:ce_detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_('Start date should be before end date.'))

        if self.enable_registration and not self.registration_deadline_at:
            raise ValidationError(_('Please select a registration deadline.'))

    def is_registration_deadline_passed(self):
        return not (self.registration_deadline_at and self.registration_deadline_at > timezone.now())


class Registration(models.Model):
    event = models.ForeignKey(ComingEvent, on_delete=models.CASCADE,
                              limit_choices_to=Q(enable_registration=True) & Q(is_published=True))
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT)
    email = models.EmailField(_('email'), unique=True, help_text='example@gmail.com')
    phone_number = models.CharField(_('phone number'), validators=[mobile_num_regex], max_length=13)
    message = models.TextField(_('Message'), blank=True, default='')

    class Meta:
        verbose_name = 'Event Registration'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('core:ce_registration', kwargs={'pk': self.pk})
