from django.urls import path, re_path

from apps.projects import views

app_name = 'projects'

urlpatterns = [
    path('csa-projects', views.CSAProjectList.as_view(), name='csa_p'),
    path('alt-projects', views.ALTProjectList.as_view(), name='alt_p'),
    path('leaders/lt-projects', views.LTProjectList.as_view(), name='lt_p'),
    path('unit-projects', views.UnitProjectList.as_view(), name='unit_p'),

    re_path('csa-project-detail/(?P<pk>\d+)', views.CSAProjectDetail.as_view(), name='csa_p_detail'),
    re_path('alt-project-detail/(?P<pk>\d+)', views.ALTProjectDetail.as_view(), name='alt_p_detail'),
    re_path('lt-project-detail/(?P<pk>\d+)', views.LTProjectDetail.as_view(), name='lt_p_detail'),
    re_path('unit-project-detail/(?P<pk>\d+)', views.UnitProjectDetail.as_view(), name='unit_p_detail'),

    path('csa-project/add', views.AddCSAProject.as_view(), name='add_csa_project'),
    path('alt-project/add', views.AddALTProject.as_view(), name='add_alt_project'),
    path('lt-project/add', views.AddLTProject.as_view(), name='add_lt_project'),
    path('unit-project/add', views.AddUnitProject.as_view(), name='add_unit_project'),
]
