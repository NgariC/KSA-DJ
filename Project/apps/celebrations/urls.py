from django.urls import path, re_path

from apps.celebrations import views

app_name = 'celebrations'

urlpatterns = [
    path('fouderees', views.FoundereeList.as_view(), name='founderee'),
    path('patrons-day-participants', views.CountyParticipantsList.as_view(), name='patrons_day_participants'),

    re_path('founderee-detail/(?P<pk>\d+)', views.FoundereeDetail.as_view(), name='founderee_detail'),
    re_path('patrons-day-participants-detail/(?P<pk>\d+)', views.CountyParticipantsDetail.as_view(),
            name='patrons_day_participants_detail'),

    path('founderee/add', views.AddFounderee.as_view(), name='add_founderee'),
    path('patrons-day-participants/add', views.AddCountyParticipants.as_view(), name='add_patrons_day_participants'),
]
