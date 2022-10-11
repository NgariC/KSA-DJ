from django.urls import path, re_path

from apps.registrations import views

app_name = 'registrations'

urlpatterns = [

    path('units', views.UnitList.as_view(), name="units"),
    path('scouts', views.ScoutList.as_view(), name='scouts'),
    path('scout-leaders', views.ScoutLeaderList.as_view(), name='scout_leaders'),

    re_path('unit-detail/(?P<pk>\d+)', views.UnitDetail.as_view(), name='unit_detail'),
    re_path('scout-detail/(?P<pk>\d+)', views.ScoutDetail.as_view(), name='scout_detail'),
    re_path('scout-leader-detail/(?P<pk>\d+)', views.ScoutLeaderDetail.as_view(), name='scout_leader_detail'),

    path('unit/add', views.AddUnit.as_view(), name='add_unit'),
    path('scout/add', views.AddScout.as_view(), name='add_scout'),
    path('scoutleader/add', views.AddScoutLeader.as_view(), name='add_scout_leader'),
    path('scoutleader-cert/add', views.AddScoutLeaderCert.as_view(), name='add_scout_leader_cert'),

    path('section/select', views.SectionSelect.as_view(), name='section_select'),

    re_path('scout-unit-update/(?P<pk>\d+)', views.ScoutUnitUpdate.as_view(), name='scout_unit_update'),
    re_path('scout-section-update/(?P<pk>\d+)', views.ScoutSectionUpdate.as_view(), name='scout_section_update'),
    re_path('scout-leader-unit-update/(?P<pk>\d+)', views.ScoutLeaderUnitUpdate.as_view(),
            name='scout_leader_unit_update'),
]
