from django.urls import path, re_path

from apps.competitions import views

app_name = 'competitions'

urlpatterns = [
    path('competitions-teams', views.TeamsList.as_view(), name='teams'),
    path('competitions', views.CompetitionList.as_view(), name='competitions'),

    re_path('chipukizi-patrol-detail/(?P<pk>\d+)', views.CompetitionTeamDetail.as_view(), name='ct_detail'),
    re_path('competition-detail/(?P<pk>\d+)', views.CompetitionDetail.as_view(), name='competition_detail'),

    path('team/add', views.AddTeam.as_view(), name='add_team'),
    path('competition/add', views.AddCompetition.as_view(), name='add_competition'),

    path('level/select', views.LevelSelect.as_view(), name='level_select'),
    path('section/select', views.SectionSelect.as_view(), name='team_section_select'),

    re_path('competition-update/(?P<pk>\d+)', views.CompetitionUpdate.as_view(), name='competition_update'),
]
