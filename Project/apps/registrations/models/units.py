from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from apps.jurisdictions.models import SubCounty
from apps.registrations.managers import UnitManager

from apps.registrations.utilities import SECTION, u_code


class Unit(models.Model):
    name = models.CharField(_("Unit Name"), max_length=100, db_index=True)
    sponsoring_authority = models.CharField(_('sponsoring authority'), max_length=100, blank=True, null=True)
    sections = MultiSelectField(_('sections'), choices=SECTION, min_choices=1, max_choices=4, max_length=70,
                                db_index=True)
    date_warranted = models.DateTimeField(_('date warranted'), auto_now_add=True, editable=False, db_index=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT)
    active = models.BooleanField(_('activeness'), default=False, db_index=True)

    objects = UnitManager()

    class Meta:
        permissions = [('can_verify_units', 'Can verify units'),
                       ('can_print_units_certs', 'Can print units certificates')]
        unique_together = ['name', 'sub_county']

    def __str__(self):
        return f"{self.name}/{self.unique_code}"

    def get_absolute_url(self):
        return reverse('registrations:unit_detail', kwargs={'pk': self.pk})

    @property
    def unique_code(self):
        return u_code(self.pk)

    @property
    def code(self):
        return f"{self.sub_county.county}/{self.unique_code}/{self.date_warranted.year}"

    @property
    def reg_amount(self):
        return 500
