import datetime

from django.db import models
from django.urls import reverse

from apps.celebrations.managers import FoundereeManager
from apps.core.project_requirements.utilities import active_limit

from apps.geoposition.fields import GeopositionField
from apps.jurisdictions.models import County
from apps.registrations.models import ScoutLeader


class Founderee(models.Model):
    year = models.PositiveSmallIntegerField(
        "Founderee Year", default=datetime.date.today().year, editable=False)
    camp_chief = models.ForeignKey(ScoutLeader,
                                   on_delete=models.PROTECT,
                                   limit_choices_to=active_limit,
                                   help_text="Only active Scout Leaders are valid options")
    support_staff = models.ManyToManyField(ScoutLeader,
                                           related_name='%(class)s_support_staff',
                                           limit_choices_to=active_limit,
                                           help_text="Only active Scout Leaders are valid options")
    staff = models.ManyToManyField(ScoutLeader, related_name='%(class)s_staff',)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    report = models.FileField(upload_to='Founderee/%Y')
    county = models.ForeignKey(County, on_delete=models.PROTECT)
    venue_name = models.CharField("Venue Name", max_length=50)
    venue = GeopositionField()

    objects = FoundereeManager()

    def __str__(self):
        return f'{self.county} - {self.year}'

    def get_absolute_url(self):
        return reverse('celebrations:founderee_detail', kwargs={'pk': self.pk})
