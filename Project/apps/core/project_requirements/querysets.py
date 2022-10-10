from apps.competitions.models import CompetitionTeam, SpecialTeamsCategories
from apps.core.models import ComingEvent
from apps.jurisdictions.models import Zone, SubCounty, County, Region, Country, Rank
from apps.registrations.models import Unit, Scout, ScoutLeader, ScoutLeaderCert

SpecialTeamsCategoriesQ = SpecialTeamsCategories.objects.all()
CompetitionTeamQ = CompetitionTeam.objects.all()

CountryQ = Country.objects.all()
RegionQ = Region.objects.all()
CountyQ = County.objects.all()
SubCountyQ = SubCounty.objects.all()
ZoneQ = Zone.objects.all()
RankQ = Rank.objects.all()

UnitQ = Unit.objects.all()
ScoutQ = Scout.objects.all()
ScoutLeaderQ = ScoutLeader.objects.all()
ScoutLeaderCertQ = ScoutLeaderCert.objects.all()

ComingEventQ = ComingEvent.objects.all()
