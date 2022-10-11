from django.urls import re_path, path

from apps.youth_programme import views

app_name = 'youth_programme'

urlpatterns = [
    path('investiture-events', views.InvestitureList.as_view(), name='i'),
    path('badge-camp-events', views.BadgeCampList.as_view(), name='bc'),
    path('park-holiday-events', views.ParkHolidayList.as_view(), name='ph'),
    path('plc-events', views.PLCList.as_view(), name='plc'),
    path('rover-mate-events', views.RMList.as_view(), name='rm'),

    re_path('investiture-detail/(?P<pk>\d+)', views.InvestitureDetail.as_view(), name='i_detail'),
    re_path('badge-camp-detail/(?P<pk>\d+)', views.BadgeCampDetail.as_view(), name='bc_detail'),
    re_path('park-holiday-detail/(?P<pk>\d+)', views.ParkHolidayDetail.as_view(), name='ph_detail'),
    re_path('plc-detail/(?P<pk>\d+)', views.PLCDetail.as_view(), name='plc_detail'),
    re_path('rover-mate-detail/(?P<pk>\d+)', views.RMDetail.as_view(), name='rm_detail'),

    path('investiture/add', views.AddInvestiture.as_view(), name='add_i'),
    path('badge-camp/add', views.AddBadgeCamp.as_view(), name='add_bc'),
    path('park-holiday/add', views.AddParkHoliday.as_view(), name='add_ph'),
    path('plc/add', views.AddPLC.as_view(), name='add_plc'),
    path('rover-mate/add', views.AddRM.as_view(), name='add_rm'),
]
