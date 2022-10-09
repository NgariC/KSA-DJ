from django.db import models
from django.db.models import Q
from django.db.models import UniqueConstraint
from django.urls import reverse
from tinymce.models import HTMLField

from apps.core.project_requirements.utilities import validate_file_extension
from apps.projects.managers import CSAProjectManager, ALTProjectManager, UnitProjectManager

from apps.registrations.models import Unit, Scout, ScoutLeader


class Reports(models.Model):
    proposal = models.FileField("Proposal", upload_to='Projects/Proposals/%Y/%m', validators=[validate_file_extension])
    report1 = models.FileField("1st Report", upload_to='Projects/Reports/%Y/%m', validators=[validate_file_extension],
                               null=True, blank=True)
    report2 = models.FileField("2nd Report", upload_to='Projects/Reports/%Y/%m', validators=[validate_file_extension],
                               null=True, blank=True)
    report3 = models.FileField("3rd Report", upload_to='Projects/Reports/%Y/%m', validators=[validate_file_extension],
                               null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True, help_text='Only feel when the project is complete')

    class Meta:
        abstract = True


class Project(models.Model):
    title = models.CharField('Project Title', max_length=100)
    project_description = HTMLField()

    class Meta:
        abstract = True

    @property
    def project_code(self):
        """ a unique identifier of the project within the database. """
        if not self.pk:
            return "00000"
        if len(str(self.pk)) == 1:
            return f"000{self.pk}"
        elif len(str(self.pk)) == 2:
            return f"00{self.pk}"
        elif len(str(self.pk)) == 3:
            return f"0{self.pk}"
        else:
            return f"{self.pk}"


class CSAProject(Project, Reports):
    jasiri_scouts = models.ManyToManyField(
        Scout, db_index=True, limit_choices_to=Q(section="Jasiri") & Q(active=True) & Q(jasiri_investiture=True),
        help_text="Only active Jasiri Scouts who are invested are valid options")
    supervisor = models.ForeignKey(ScoutLeader, on_delete=models.PROTECT, blank=True, null=True,
                                   limit_choices_to=Q(active=True) & (
                                           Q(training='Two Beads') | Q(training='ALT Practical') |
                                           Q(training='ALT Project') | Q(training='Three Beads') |
                                           Q(training='LT Practical') |
                                           Q(training='LT Project') | Q(training='Four Beads')),
                                   help_text="Only active Scout Leaders with training level "
                                             "of Two Beads and above are valid options")

    objects = CSAProjectManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:csa_p_detail', kwargs={'pk': self.pk})


class ALTProject(Project, Reports):
    scout_leader_name = models.OneToOneField(
        ScoutLeader, on_delete=models.PROTECT,
        limit_choices_to=Q(active=True) & Q(training='ALT Course'),
        help_text="Only active Scout Leaders with training level of ALT Course are valid options")
    supervisor = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT, blank=True, null=True,
        related_name='alt_supervisor',
        limit_choices_to=Q(active=True) & Q(training='Four Beads'),
        help_text="Only active Scout Leaders with training level of Four Beads are valid options")

    objects = ALTProjectManager()

    class Meta:
        ordering = ['scout_leader_name']
        constraints = [
            UniqueConstraint(fields=['scout_leader_name', 'title'], name='unique_alt_project')
        ]

    def __str__(self):
        return f'{self.title} - {self.scout_leader_name}'

    def get_absolute_url(self):
        return reverse('projects:alt_p_detail', kwargs={'pk': self.pk})


class LTProject(Project, Reports):
    scout_leader_name = models.OneToOneField(
        ScoutLeader, on_delete=models.PROTECT, db_index=True,
        limit_choices_to=Q(active=True) & Q(training='LT Course'),
        help_text="Only active Scout Leaders with training level of Three Beads are valid options")
    supervisor = models.ForeignKey(
        ScoutLeader, on_delete=models.PROTECT, blank=True, null=True,
        related_name='lt_supervisor',
        limit_choices_to=Q(active=True) & Q(training='Four Beads'),
        help_text="Only active Scout Leaders with training level of Four Beads are valid options")

    objects = ALTProjectManager()

    class Meta:
        ordering = ['scout_leader_name']
        constraints = [
            UniqueConstraint(fields=['scout_leader_name', 'title'], name='unique_lt_project')
        ]

    def __str__(self):
        return f'{self.title} - {self.scout_leader_name}'

    def get_absolute_url(self):
        return reverse('projects:lt_p_detail', kwargs={'pk': self.pk})


class UnitProject(Project):
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, db_index=True,
                             limit_choices_to=Q(active=True),
                             help_text="Only verified Units are valid options")
    coordinator = models.ForeignKey(ScoutLeader, on_delete=models.PROTECT, blank=True, null=True,
                                    limit_choices_to=Q(active=True),
                                    help_text="Only active Scout Leaders are valid options")
    detailed_report = models.FileField(upload_to='Unit Projects/%Y/%m')

    objects = UnitProjectManager()

    class Meta:
        ordering = ['unit']

    def __str__(self):
        return f'{self.title} - {self.unit}'

    def get_absolute_url(self):
        return reverse('projects:unit_p_detail', kwargs={'pk': self.pk})
