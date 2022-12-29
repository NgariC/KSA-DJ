import random
import django
import os

# must be in top of django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
django.setup()
from faker import Faker
# must come after django.setup()
from apps.jurisdictions.models import SubCounty, Rank
from apps.registrations.models import Unit, Scout, ScoutLeader

fake = Faker()

sub_counties = SubCounty.objects.all()
units = Unit.objects.all()
s_units = Unit.objects.filter(sections__icontains='Sungura' or 'Chipukizi' or 'Mwamba')
c_units = Unit.objects.filter(sections__icontains='Sungura' or 'Chipukizi' or 'Mwamba')
m_units = Unit.objects.filter(sections__icontains='Sungura' or 'Chipukizi' or 'Mwamba')
j_units = Unit.objects.filter(sections__icontains='Jasiri')
ranks = Rank.objects.filter(level='Unit')


def generate_units(y=10, sub_county=None):
    for _ in range(y):
        name = fake.company()
        sponsoring_authority = fake.company()
        sections = fake.random_elements(elements=('Sungura', 'Chipukizi', 'Mwamba', 'Jasiri'), unique=True)
        sub_county = random.choice(sub_counties)
        active = fake.pybool()

        try:
            if sub_county:
                Unit.objects.bulk_create([
                    Unit(name=name,
                         sponsoring_authority=sponsoring_authority,
                         sections=sections,
                         sub_county=sub_county,
                         active=active)])
        except Exception:
            continue


def generate_scout_leaders(r=10, sub_county=None):
    for _ in range(r):
        first_name = fake.first_name()
        middle_name = fake.last_name()
        surname = fake.last_name()
        gender = fake.random_element(elements=('M', 'F'))
        date_of_birth = fake.date()
        national_id = fake.random_number(digits=8, fix_len=True)
        tsc_number = fake.random_number(digits=6, fix_len=True)
        email = fake.free_email()
        phone_number = fake.numerify('+254 7## ### ###')
        image = None
        unit = random.choice(units)
        rank = random.choice(ranks)
        sub_county = unit.sub_county
        training = fake.random_element(elements=(
            'Not Yet Trained', 'ITC', 'PTC', 'WB Theory', 'WB Course', 'WB Assessment', 'Two Beads', 'ALT Course',
            'ALT Project', 'Three Beads', 'LT Course', 'LT Project', 'Four Beads'))
        active = fake.pybool()

        try:
            if sub_county:
                ScoutLeader.objects.bulk_create([
                    ScoutLeader(first_name=first_name,
                                middle_name=middle_name,
                                surname=surname,
                                gender=gender,
                                date_of_birth=date_of_birth,
                                national_id=national_id,
                                tsc_number=tsc_number,
                                email=email,
                                phone_number=phone_number,
                                image=image,
                                sub_county=sub_county,
                                unit=unit,
                                rank=rank,
                                training=training,
                                active=active)])
        except Exception:
            continue


def generate_sungura(r=10, unit=None):
    for _ in range(r):
        first_name = fake.first_name()
        middle_name = fake.last_name()
        surname = fake.last_name()
        gender = fake.random_element(elements=('M', 'F'))
        date_of_birth = fake.date()
        birth_certificate_number = fake.random_number(digits=8, fix_len=True)
        image = None
        unit = random.choice(s_units)
        investiture = fake.pybool()
        link_badge_award = fake.pybool()
        chui_badge_award = fake.pybool()
        simba_badge_award = fake.pybool()
        active = fake.pybool()
        section = 'Sungura'

        try:
            if unit:
                Scout.objects.bulk_create([
                    Scout(first_name=first_name,
                          middle_name=middle_name,
                          surname=surname,
                          gender=gender,
                          date_of_birth=date_of_birth,
                          birth_certificate_number=birth_certificate_number,
                          image=image,
                          unit=unit,
                          investiture=investiture,
                          link_badge_award=link_badge_award,
                          chui_badge_award=chui_badge_award,
                          simba_badge_award=simba_badge_award,
                          section=section,
                          active=active)])
        except Exception:
            continue


def generate_chipukizi(r=10, unit=None):
    for _ in range(r):
        first_name = fake.first_name()
        middle_name = fake.last_name()
        surname = fake.last_name()
        gender = fake.random_element(elements=('M', 'F'))
        date_of_birth = fake.date()
        birth_certificate_number = fake.random_number(digits=8, fix_len=True)
        image = None
        unit = random.choice(c_units)
        investiture = fake.pybool()
        link_badge_award = fake.pybool()
        chui_badge_award = fake.pybool()
        simba_badge_award = fake.pybool()
        active = fake.pybool()
        section = 'Chipukizi'

        try:
            if unit:
                Scout.objects.bulk_create([
                    Scout(first_name=first_name,
                          middle_name=middle_name,
                          surname=surname,
                          gender=gender,
                          date_of_birth=date_of_birth,
                          birth_certificate_number=birth_certificate_number,
                          image=image,
                          unit=unit,
                          investiture=investiture,
                          link_badge_award=link_badge_award,
                          chui_badge_award=chui_badge_award,
                          simba_badge_award=simba_badge_award,
                          section=section,
                          active=active)])
        except Exception:
            continue


def generate_mwamba(r=10, unit=None):
    for _ in range(r):
        first_name = fake.first_name()
        middle_name = fake.last_name()
        surname = fake.last_name()
        gender = fake.random_element(elements=('M', 'F'))
        date_of_birth = fake.date()
        birth_certificate_number = fake.random_number(digits=8, fix_len=True)
        image = None
        unit = random.choice(m_units)
        investiture = fake.pybool()
        link_badge_award = fake.pybool()
        chui_badge_award = fake.pybool()
        simba_badge_award = fake.pybool()
        active = fake.pybool()
        section = 'Mwamba'

        try:
            if unit:
                Scout.objects.bulk_create([
                    Scout(first_name=first_name,
                          middle_name=middle_name,
                          surname=surname,
                          gender=gender,
                          date_of_birth=date_of_birth,
                          birth_certificate_number=birth_certificate_number,
                          image=image,
                          unit=unit,
                          investiture=investiture,
                          link_badge_award=link_badge_award,
                          chui_badge_award=chui_badge_award,
                          simba_badge_award=simba_badge_award,
                          section=section,
                          active=active)])
        except Exception:
            continue


def generate_jasiri(r=10, unit=None):
    section = 'Jasiri'

    for _ in range(r):
        first_name = fake.first_name()
        middle_name = fake.last_name()
        surname = fake.last_name()
        gender = fake.random_element(elements=('M', 'F'))
        date_of_birth = fake.date()
        national_id = fake.random_number(digits=8, fix_len=True)
        email = fake.free_email()
        phone_number = fake.numerify('+254 7## ### ###')
        image = None
        unit = random.choice(j_units)
        investiture = fake.pybool()
        jasiri_investiture = fake.pybool()
        csa_award = fake.pybool()
        active = fake.pybool()
        try:
            if unit:
                Scout.objects.bulk_create([
                    Scout(first_name=first_name,
                          middle_name=middle_name,
                          surname=surname,
                          gender=gender,
                          date_of_birth=date_of_birth,
                          national_id=national_id,
                          email=email,
                          phone_number=phone_number,
                          image=image,
                          unit=unit,
                          investiture=investiture,
                          jasiri_investiture=jasiri_investiture,
                          csa_award=csa_award,
                          active=active,
                          section=section)])
        except Exception:
            continue


if __name__ == "__main__":
    print('Creating Fake Units....')
    y = int(input('How many units do you wanna create?'))
    generate_units(y)
    print('Units are created.')
    print('Creating Fake Scout Leaders....')
    r = int(input('How many Scout Leaders do you wanna create?'))
    generate_scout_leaders(r)
    print('Scout Leaders are created.')
    print('Creating Fake Sungura Scout....')
    r = int(input('How many Sungura Scout do you wanna create?'))
    generate_sungura(r)
    print('Sungura Scouts are created.')
    print('Creating Fake Chipukizi Scout....')
    r = int(input('How many Chipukizi Scout do you wanna create?'))
    generate_chipukizi(r)
    print('Chipukizi Scouts are created.')
    print('Creating Fake Mwamba Scout....')
    r = int(input('How many Mwamba Scout do you wanna create?'))
    generate_mwamba(r)
    print('Mwamba Scouts are created.')
    print('Creating Fake Jasiri Scout....')
    r = int(input('How many Jasiri Scout do you wanna create?'))
    generate_jasiri(r)
    print('Jasiri Scouts are created.')
