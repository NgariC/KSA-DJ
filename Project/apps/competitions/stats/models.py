from apps.competitions.models import CompetitionTeam, Competition
from apps.competitions.stats.managers import TeamManager, CompetitionManager


class CompetitionTeamStats(CompetitionTeam):
    objects = TeamManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'Competition Team Stats'
        verbose_name_plural = 'Competition Teams Stats'


class CompetitionStats(Competition):
    objects = CompetitionManager()

    class Meta:
        proxy = True
        default_permissions = ('view',)
        verbose_name = 'Competition Stats'
        verbose_name_plural = 'Competitions Stats'
