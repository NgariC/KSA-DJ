import datetime

from django.db import models
from django.db.models import Q
from django.urls import reverse

from apps.celebrations.managers import LinkBadgeAwardManager, ChuiBadgeAwardManager, SimbaBadgeAwardManager, \
    ChiefScoutAwardManager, ScoutLeaderAwardManager, CountyParticipantsManager, PatronsDayManager, BeadsAwardManager
from apps.core.project_requirements.utilities import active_limit, this_year_limit
from apps.jurisdictions.models import County
from apps.registrations.models import ScoutLeader, Scout


class Award(models.Model):
    award_date = models.DateField()
    year = models.PositiveSmallIntegerField("Awards Year", default=datetime.date.today().year, editable=False)

    class Meta:
        abstract = True


class SLAward(models.Model):
    awardees = models.ManyToManyField(ScoutLeader, related_name='%(class)s_awardees', blank=True)

    class Meta:
        abstract = True


class ScoutAward(models.Model):
    awardees = models.ManyToManyField(Scout, related_name='%(class)s_awardees', blank=True)

    class Meta:
        abstract = True


class TwoBeadsAward(Award, SLAward):
    scout_leaders = models.ManyToManyField(ScoutLeader, related_name='two_beads_awardees', blank=True,
                                           limit_choices_to=Q(active=True) & Q(training='WB Assessment'),
                                           help_text="Only active Scout Leaders who have completed their "
                                                     "WoodBadge Assessment are valid options")

    objects = BeadsAwardManager()

    def __str__(self):
        return str(self.year)


class ThreeBeadsAward(Award, SLAward):
    scout_leaders = models.ManyToManyField(ScoutLeader, related_name='three_beads_awardees', blank=True,
                                           limit_choices_to=Q(active=True) & Q(training='ALT Project'),
                                           help_text="Only active Scout Leaders who have completed their "
                                                     "ALT Project are valid options")

    objects = BeadsAwardManager()

    def __str__(self):
        return str(self.year)


class FourBeadsAward(Award, SLAward):
    scout_leaders = models.ManyToManyField(ScoutLeader, related_name='four_beads_awardees', blank=True,
                                           limit_choices_to=Q(active=True) & Q(training='LT Project'),
                                           help_text="Only active Scout Leaders who have completed their "
                                                     "ALT Project are valid options")

    objects = BeadsAwardManager()

    def __str__(self):
        return str(self.year)


class LinkBadgeAward(Award, ScoutAward):
    sungura_scouts = models.ManyToManyField(Scout, blank=True,
                                            limit_choices_to=Q(active=True) & Q(section='Sungura') &
                                            Q(investiture=True) & Q(link_badge_award=False),
                                            help_text="Only active & invested Sungura Scouts who have not yet "
                                                      "been awarded Link Badge Award are valid options")

    objects = LinkBadgeAwardManager()

    def __str__(self):
        return str(self.year)


class ChuiBadgeAward(Award, ScoutAward):
    chipukizi_scouts = models.ManyToManyField(Scout, blank=True,
                                              limit_choices_to=Q(active=True) & Q(section='Chipukizi')
                                              & Q(investiture=True) & Q(chui_badge_award=False),
                                              help_text="Only active & invested Chipukizi Scouts who have not yet "
                                                        "been awarded Chui Badge Award are valid options")

    objects = ChuiBadgeAwardManager()

    def __str__(self):
        return str(self.year)


class SimbaBadgeAward(Award, ScoutAward):
    mwamba_scouts = models.ManyToManyField(Scout, blank=True,
                                           limit_choices_to=Q(active=True) & Q(section='Mwamba') &
                                           Q(investiture=True) & Q(simba_badge_award=False),
                                           help_text="Only active & invested Mwamba Scouts who have not yet "
                                                     "been awarded Simba Badge Award are valid options")

    objects = SimbaBadgeAwardManager()

    def __str__(self):
        return str(self.year)


class ChiefScoutAward(Award):
    jasiri_scouts = models.ManyToManyField(Scout, blank=True, limit_choices_to=Q(active=True) & Q(section='Jasiri') &
                                           Q(jasiri_investiture=True) & Q(csa_award=False),
                                           help_text="Only active & invested Jasiri Scouts who have not yet "
                                                     "been awarded Chief Scout Award (CSA) are valid options")
    awardees = models.ManyToManyField(Scout, related_name='%(class)s_awardees', blank=True)

    objects = ChiefScoutAwardManager()

    def __str__(self):
        return str(self.year)


class ScoutLeaderAward(Award, SLAward):
    name = models.CharField(max_length=250, db_index=True)
    scout_leaders = models.ManyToManyField(ScoutLeader, blank=True, limit_choices_to=active_limit,
                                           help_text="Only active Scout Leaders are valid options")

    objects = ScoutLeaderAwardManager()

    def __str__(self):
        return f'{self.name} - {self.year}'


class CountyParticipants(models.Model):
    year = models.PositiveSmallIntegerField("Year", default=datetime.date.today().year, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    county = models.ForeignKey(County, on_delete=models.PROTECT, db_index=True, unique_for_year="year")
    sungura_scouts = models.ManyToManyField(Scout, related_name='sungura_scouts',
                                            limit_choices_to=Q(active=True) & Q(section='Sungura'),
                                            help_text="Only active Sungura Scouts are valid options")
    chipukizi_scouts = models.ManyToManyField(Scout, related_name='chipukizi_scouts',
                                              limit_choices_to=Q(active=True) & Q(section='Chipukizi'),
                                              help_text="Only active Chipukizi Scouts are valid options")
    mwamba_scouts = models.ManyToManyField(Scout, related_name='mwamba_scouts',
                                           limit_choices_to=Q(active=True) & Q(section='Mwamba'),
                                           help_text="Only active Mwamba Scouts are valid options")
    jasiri_scouts = models.ManyToManyField(Scout, limit_choices_to=Q(active=True) & Q(section='Jasiri'),
                                           help_text="Only active Jasiri Scouts are valid options")
    scout_leaders = models.ManyToManyField(ScoutLeader, limit_choices_to=active_limit,
                                           help_text="Only active Scout Leaders are valid options")
    scouts_attendees = models.ManyToManyField(Scout, blank=True, related_name='%(class)s_scout_attendees')
    scout_leaders_attendees = models.ManyToManyField(ScoutLeader, blank=True,
                                                     related_name='%(class)s_scout_leaders_attendees')

    objects = CountyParticipantsManager()

    def __str__(self):
        return f'{self.county} - {self.year}'

    def get_absolute_url(self):
        return reverse('celebrations:patrons_day_participants_detail', kwargs={'pk': self.pk})


class PatronsDay(models.Model):
    year = models.PositiveSmallIntegerField("Year", default=datetime.date.today().year, editable=False)
    date = models.DateField(db_index=True)
    sungura_awards = models.ManyToManyField(LinkBadgeAward, blank=True, limit_choices_to=this_year_limit)
    chipukizi_awards = models.ManyToManyField(ChuiBadgeAward, blank=True, limit_choices_to=this_year_limit)
    mwamba_awards = models.ManyToManyField(SimbaBadgeAward, blank=True, limit_choices_to=this_year_limit)
    jasiri_awards = models.ManyToManyField(ChiefScoutAward, blank=True, limit_choices_to=this_year_limit)
    scout_leaders_awards = models.ManyToManyField(ScoutLeaderAward, blank=True, limit_choices_to=this_year_limit)
    county_participants = models.ManyToManyField(CountyParticipants, blank=True, limit_choices_to=this_year_limit)

    objects = PatronsDayManager()

    def __str__(self):
        return f'{self.date} - {self.year}'
