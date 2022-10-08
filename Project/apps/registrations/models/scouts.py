import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from apps.core.project_requirements.utilities import mobile_num_regex
from apps.registrations.managers import ScoutManager
from apps.registrations.models.abstract import Person
from apps.registrations.models.units import Unit
from apps.registrations.utilities import SECTION

old_27_years = datetime.date.today() - datetime.timedelta(days=9855)
years_back_27 = int(datetime.date.today().year) - 27


class Scout(Person):
    birth_certificate_number = models.CharField('Birth Certificate Number', max_length=8, null=True, blank=True)
    section = models.CharField(max_length=10, choices=SECTION, db_index=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, db_index=True)
    investiture = models.BooleanField(default=False, db_index=True)
    jasiri_investiture = models.BooleanField(default=False, db_index=True)
    nyota_i = models.BooleanField('Nyota I', default=False, db_index=True)
    nyota_ii = models.BooleanField('Nyota II', default=False, db_index=True)
    nyota_iii = models.BooleanField('Nyota III', default=False, db_index=True)
    link_badge_award = models.BooleanField('Link Badge Award', default=False, db_index=True)
    zizi = models.BooleanField('Zizi', default=False, db_index=True)
    shina = models.BooleanField('Shina', default=False, db_index=True)
    tawi = models.BooleanField('Tawi', default=False, db_index=True)
    chui_badge_award = models.BooleanField('Chui Badge Award', default=False, db_index=True)
    mwanzo = models.BooleanField('Mwanzo', default=False, db_index=True)
    mwangaza = models.BooleanField('Mwangaza', default=False, db_index=True)
    kilele = models.BooleanField('Kilele', default=False, db_index=True)
    simba_badge_award = models.BooleanField('Simba Badge Award', default=False, db_index=True)
    csa_award = models.BooleanField('CSA Award', default=False, db_index=True)
    date_of_birth = models.DateField()
    national_id = models.CharField('National ID/Passport', max_length=8, unique=True, null=True, blank=True,
                                   help_text='Leave blank if the Scout is not a Jasiri')
    email = models.EmailField(unique=True, help_text='example@gmail.com (Leave blank if the Scout is not a Jasiri)',
                              null=True, blank=True)
    phone_number = models.CharField(validators=[mobile_num_regex], max_length=13, null=True, blank=True,
                                    help_text='Leave blank if the Scout is not a Jasiri')

    objects = ScoutManager()

    class Meta:
        permissions = [('can_verify_scouts', 'Can verify scouts')]
        unique_together = ['first_name', 'middle_name', 'unit']

    def __str__(self):
        return f"{self.get_short_name} - {self.code}"

    def get_absolute_url(self):
        return reverse('registrations:scout_detail', kwargs={'pk': self.pk})

    @property
    def code(self):
        return f"{self.gender}{self.unique_code}{self.section[:1]}"

    @property
    def sub_county(self):
        return self.unit.sub_county

    @property
    def age(self):
        return int((datetime.date.today() - self.date_of_birth).days / 365)

    @property
    def reg_amount(self):
        return 100

    def clean(self):
        if self.section == 'Jasiri' and not self.national_id:
            raise ValidationError('For a Jasiri Scout the National Id/Passport must be provided.')
        if self.section == 'Jasiri' and not self.email:
            raise ValidationError('For a Jasiri Scout the Email must be provided.')
        if self.section == 'Jasiri' and not self.phone_number:
            raise ValidationError('For a Jasiri Scout the Phone Number must be provided.')
        if self.section == 'Sungura' and self.chui_badge_award:
            raise ValidationError('A Sungura Scout cannot attain the highest badge of a Chipukizi Scout.')
        if self.section == 'Sungura' and self.simba_badge_award:
            raise ValidationError('A Sungura Scout cannot attain the highest badge of a Mwamba Scout.')
        if self.section == 'Sungura' and self.csa_award:
            raise ValidationError('A Sungura Scout cannot attain the highest badge of a Jasiri Scout.')
        if self.section == 'Chipukizi' and self.simba_badge_award:
            raise ValidationError('A Chipukizi Scout cannot attain the highest badge of a Mwamba Scout.')
        if self.section == 'Chipukizi' and self.csa_award:
            raise ValidationError('A Chipukizi Scout cannot attain the highest badge of a Jasiri Scout.')
        if self.section == 'Mwamba' and self.csa_award:
            raise ValidationError('A Mwamba Scout cannot attain the highest badge of a Jasiri Scout.')
        if self.section != 'Jasiri' and self.jasiri_investiture:
            raise ValidationError('Only Jasiri Scouts can undergo Jasiri Investiture')
        if self.section == 'Jasiri':
            self.date_of_birth.__gt__(old_27_years)
