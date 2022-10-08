from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.core.project_requirements.utilities import GENDER
from apps.registrations.utilities import u_code


class Person(models.Model):
    first_name = models.CharField(_('first name'), max_length=60, db_index=True)
    middle_name = models.CharField(_('middle name'), max_length=60, null=True, blank=True)
    surname = models.CharField(_('surname'), max_length=60)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER, db_index=True)
    image = models.ImageField(_("Profile Picture"), upload_to='Profile Image/%Y/%m/%d')
    registration_date = models.DateTimeField(_('registration date'), auto_now_add=True, editable=False, db_index=True)
    active = models.BooleanField(_('activeness'), default=False, db_index=True)

    class Meta:
        abstract = True

    @property
    def unique_code(self):
        return u_code(self.pk)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.surname}".strip()

    @property
    def get_short_name(self):
        return f"{self.first_name} {self.middle_name}"

    @admin.display(description='Picture')
    def profile_image(self):
        return mark_safe('<img base="{url}" width="{width}" height={height} />'.format(
            url=self.image.path,
            width=self.image.width,
            height=self.image.height,
        )
        )
