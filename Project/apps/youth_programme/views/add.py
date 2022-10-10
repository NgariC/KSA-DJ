from apps.core.project_requirements.access import SubCountyMemberRequiredForm, SelfSuccessMessageMixinAdded
from apps.youth_programme.forms import InvestitureForm, BadgeCampForm, ParkHolidayForm, RMForm, PLCForm
from apps.youth_programme.models import Investiture, BadgeCamp, ParkHoliday, PLC, RM


class AddInvestiture(SubCountyMemberRequiredForm, SelfSuccessMessageMixinAdded):
    form_class = InvestitureForm
    model = Investiture


class AddBadgeCamp(SubCountyMemberRequiredForm, SelfSuccessMessageMixinAdded):
    form_class = BadgeCampForm
    model = BadgeCamp


class AddParkHoliday(SubCountyMemberRequiredForm, SelfSuccessMessageMixinAdded):
    form_class = ParkHolidayForm
    model = ParkHoliday


class AddPLC(SubCountyMemberRequiredForm, SelfSuccessMessageMixinAdded):
    form_class = PLCForm
    model = PLC


class AddRM(SubCountyMemberRequiredForm, SelfSuccessMessageMixinAdded):
    form_class = RMForm
    model = RM
