import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.project_requirements.utilities import mobile_num_regex
from apps.jurisdictions.models import SubCounty, Rank
from apps.registrations.managers import ScoutLeaderManager
from apps.registrations.models.abstract import Person
from apps.registrations.models.units import Unit
from apps.registrations.utilities import TRAINING

old_enough_26 = datetime.date.today() - datetime.timedelta(days=9490)


def over_26_years(value):
    if value > old_enough_26:
        raise ValidationError(_("The age have to be 26 years and above!"))
    return value


class ScoutLeader(Person):
    date_of_birth = models.DateField(_('date of birth'), validators=[over_26_years])
    national_id = models.CharField(_('National ID/Passport'), max_length=8, unique=True)
    email = models.EmailField(_('email'), unique=True, help_text='example@gmail.com')
    phone_number = models.CharField(_('phone number'), validators=[mobile_num_regex], max_length=13)
    tsc_number = models.CharField(_('tsc number'), max_length=6, null=True, blank=True)
    rank = models.ForeignKey(Rank, default='Unit-Leader', on_delete=models.PROTECT, db_index=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, db_index=True, null=True, blank=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT, db_index=True)
    training = models.CharField(_('Level of Training'), default='Not Yet Trained', max_length=15, choices=TRAINING,
                                db_index=True)
    life_member = models.BooleanField(_('life member'), default=False, db_index=True)

    objects = ScoutLeaderManager()

    class Meta:
        unique_together = ['first_name', 'national_id', 'email']
        permissions = [('can_verify_scout_leaders', 'Can verify scout leaders')]

    def __str__(self):
        return f"{self.get_short_name} - {self.code}"

    def get_absolute_url(self):
        return reverse('registrations:scout_leader_detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.life_member and not self.active:
            raise ValidationError(_('A life member should always be active. Mark the Scout Leader as active'))

    @property
    def code(self):
        return f"{self.gender}{self.unique_code}/{self.rank.code}"

    @property
    def office(self):
        return f"{self.rank.level}"

    @property
    def reg_amount(self):
        if self.rank.level == 'National':
            return 2000
        elif self.rank.level in ['Regional', 'County']:
            return 1000
        elif self.rank.level == 'SubCounty':
            return 500
        else:
            return 300


class ScoutLeaderCert(models.Model):
    code = models.CharField(_('code'), primary_key=True, max_length=20, db_index=True)
    name = models.CharField(_('name'), max_length=100)
    scout_leader = models.ForeignKey(ScoutLeader, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return f"{self.code} {self.name}"
