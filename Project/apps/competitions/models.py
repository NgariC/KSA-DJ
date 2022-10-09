import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.competitions.managers import TeamManager, CompetitionManager
from apps.core.project_requirements.utilities import active_limit, validate_file_extension, GENDER
from apps.geoposition.fields import GeopositionField
from apps.jurisdictions.models import SubCounty, Country
from apps.registrations.models import ScoutLeader, Unit, Scout


class SpecialTeamsCategories(models.Model):
    name = models.CharField(_('name'), max_length=150, db_index=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CompetitionTeam(models.Model):
    LEVEL = (
        ('SubCounty', _('SubCounty')),
        ('County', _('County')),
        ('Region', _('Region')),
        ('National', _('National')),
        ('Zonal', _('Zonal')),
    )
    SECTION = (
        ('Chipukizi', _('Chipukizi')),
        ('Mwamba', _('Mwamba')),
        ('Jasiri', _('Jasiri')),
    )
    year = models.PositiveSmallIntegerField(_("Competition Year"), default=datetime.date.today().year, editable=False)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER, db_index=True)
    name = models.CharField(_('name'), max_length=150, db_index=True)
    team_leaders = models.ManyToManyField(ScoutLeader, related_name='%(class)s_team_leaders',
                                          limit_choices_to=active_limit,
                                          help_text="Only active Scout Leaders are valid options")
    leaders = models.ManyToManyField(ScoutLeader, related_name='%(class)s_leaders', blank=True)
    level_of_competition = models.CharField(_('Level of Competition'), default='SubCounty', max_length=15, choices=LEVEL,
                                            db_index=True)
    section = models.CharField(_('Team Section'), max_length=15, choices=SECTION, db_index=True)
    special = models.BooleanField(_('If the Team is a Special team'), default=False, db_index=True)
    special_category = models.ForeignKey(SpecialTeamsCategories, on_delete=models.PROTECT, null=True, blank=True,
                                         help_text="Only select if the Team is a Special Team, otherwise leave blank")
    competitors = models.ManyToManyField(Scout, related_name='%(class)s_competitors', blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, limit_choices_to=Q(active=True),
                             help_text="Validity limited to verified units")
    chipukizi_competitors = models.ManyToManyField(
        Scout, related_name='%(class)s_chipukizi_competitors', blank=True,
        limit_choices_to=Q(active=True) & Q(section='Chipukizi') & Q(investiture=True),
        help_text="Only active & invested Chipukizi Scouts are valid options")
    mwamba_competitors = models.ManyToManyField(
        Scout, related_name='%(class)s_mwamba_competitors', blank=True,
        limit_choices_to=Q(active=True) & Q(section='Mwamba') & Q(investiture=True),
        help_text="Only active & invested Mwamba Scouts are valid options")
    jasiri_competitors = models.ManyToManyField(
        Scout, related_name='%(class)s_jasiri_competitors', blank=True,
        limit_choices_to=Q(active=True) & Q(section='Jasiri') & Q(jasiri_investiture=True),
        help_text="Only active & invested Jasiri Scouts are valid options")

    objects = TeamManager()

    class Meta:
        unique_together = ['name', 'unit', 'year']
        ordering = ['name']
        permissions = [('can_update_competition_team_level_of_competition',
                        'Can update Competition Team level of competition'),
                       ('can_edit_competition_team_competitors', 'Can edit Competition Team competitors')]

    def clean(self):
        if self.special and not self.special_category:
            raise ValidationError('Please select a Special Category for you have marked the team as a Special.')
        if self.special_category and not self.special:
            raise ValidationError('Please mark the team to be Special for you have selected a Special Category.')

    def __str__(self):
        return f'{self.name}/{self.year} - {self.unit}'

    def get_absolute_url(self):
        return reverse('competitions:ct_detail', kwargs={'pk': self.pk})


class Competition(models.Model):
    LEVELS = (
        ('SubCounty', _('SubCounty')),
        ('County', _('County')),
        ('Regional', _('Regional')),
        ('National', _('National')),
        ('Zonal', _('Zonal')),
    )
    year = models.PositiveSmallIntegerField(_("Competition Year"), default=datetime.date.today().year, editable=False)
    start_date = models.DateField(_('start date'), db_index=True)
    end_date = models.DateField(_('end date'), db_index=True)
    report = models.FileField(_('report'), upload_to='Competition Report/%Y/%m', validators=[validate_file_extension])
    level = models.CharField(_('Level of Competition'), max_length=15, choices=LEVELS, db_index=True)
    venue_name = models.CharField(_('venue name'), max_length=50)
    venue = GeopositionField(_('venue'))
    payments = models.BooleanField(default=False)
    chief = models.ForeignKey(ScoutLeader, on_delete=models.PROTECT, related_name='%(class)s_chief',
                              null=True, blank=True)
    assessors = models.ManyToManyField(ScoutLeader, related_name='%(class)s_assessors', blank=True)
    teams = models.ManyToManyField(CompetitionTeam, related_name='%(class)s_teams', blank=True)
    chief_assessor = models.ForeignKey(ScoutLeader,
                                       on_delete=models.PROTECT,
                                       related_name='%(class)s_chief_assessor',
                                       limit_choices_to=active_limit,
                                       help_text="Only active Scout Leaders are valid options")
    assistant_assessors = models.ManyToManyField(ScoutLeader,
                                                 blank=True,
                                                 related_name='%(class)s_assistant_assessor',
                                                 limit_choices_to=active_limit,
                                                 help_text="Only active Scout Leaders are valid options")
    competing_teams = models.ManyToManyField(
        CompetitionTeam, blank=True, limit_choices_to=Q(year=datetime.date.today().year),
        help_text="Only Chipukizi teams registered in the year of competition are valid options")
    sub_county = models.ForeignKey(SubCounty, blank=True, null=True, db_index=True,
                                   on_delete=models.PROTECT,
                                   unique_for_year="start_date",
                                   help_text="The SubCounty from which the competition is taking place")
    country = models.ForeignKey(Country, blank=True, null=True, db_index=True, on_delete=models.PROTECT,
                                unique_for_year="start_date")

    objects = CompetitionManager()

    class Meta:
        ordering = ['start_date']
        unique_together = ['year', 'level', 'sub_county', 'country']
        permissions = [('can_verify_Competition_payments', 'Can verify Competition payments'),
                       ('can_edit_Competition_teams', 'Can edit Competition teams')]

    def __str__(self):
        if self.level == 'SubCounty':
            return f'{self.sub_county.name} SubCounty - {self.year}'
        if self.level == 'County':
            return f'{self.sub_county.county.name} County - {self.year}'
        if self.level == 'Regional':
            return f'{self.sub_county.county.region.name} Region - {self.year}'
        if self.level == 'Zonal':
            return f'Zonal Host: {self.country.name} - {self.year}'

    def get_absolute_url(self):
        return reverse('competitions:competition_detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError('Start date should be before end date.')
        if self.level != 'Zonal' and not self.sub_county:
            raise ValidationError('You need to select the SubCounty in which the Competitions is taking place')
        if self.level == 'Zonal' and not self.country:
            raise ValidationError('You need to select the Country in which the Competitions is taking place')

    def save(self, *args, **kwargs):
        if self.chief_assessor:
            self.chief = self.chief_assessor
        if self.chief and self.chief_assessor is None:
            self.chief_assessor = self.chief
        super().save(*args, **kwargs)
