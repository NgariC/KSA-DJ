from django.urls import re_path, path

from apps.training import views

app_name = 'training'

urlpatterns = [
    path('itc-events', views.ITCList.as_view(), name='itc'),
    path('ptc-event', views.PTCList.as_view(), name='ptc'),
    path('woodbadge-theory', views.WBIList.as_view(), name='wbi'),
    path('woodbadge-course', views.WBIIList.as_view(), name='wbii'),
    path('woodbadge-assessment', views.WBIIIList.as_view(), name='wbiii'),
    path('alt-course', views.ALTList.as_view(), name='alt'),
    path('lt-course', views.LTList.as_view(), name='lt'),
    path('sl-special-events', views.SLSpecialEventList.as_view(), name='slse'),

    re_path('itc-detail/(?P<pk>\d+)', views.ITCDetail.as_view(), name='itc_detail'),
    re_path('ptc-detail/(?P<pk>\d+)', views.PTCDetail.as_view(), name='ptc_detail'),
    re_path('woodbadge-I-detail/(?P<pk>\d+)', views.WBIDetail.as_view(), name='wbi_detail'),
    re_path('woodbadge-II-detail/(?P<pk>\d+)', views.WBIIDetail.as_view(), name='wbii_detail'),
    re_path('woodbadge-III-detail/(?P<pk>\d+)', views.WBIIIDetail.as_view(), name='wbiii_detail'),
    re_path('alt-detail/(?P<pk>\d+)', views.ALTDetail.as_view(), name='alt_detail'),
    re_path('lt-detail/(?P<pk>\d+)', views.LTDetail.as_view(), name='lt_detail'),
    re_path('sl-special-event-detail/(?P<pk>\d+)', views.SLSpecialEventDetail.as_view(), name='slse_detail'),

    path('itc/add', views.AddITC.as_view(), name='add_itc'),
    path('ptc/add', views.AddPTC.as_view(), name='add_ptc'),
    path('wood-badge-I/add', views.AddWBI.as_view(), name='add_wbi'),
    path('wood-badge-II/add', views.AddWBII.as_view(), name='add_wbii'),
    path('wood-badge-III/add', views.AddWBIII.as_view(), name='add_wbiii'),
    path('alt-camp-phase/add', views.AddALT.as_view(), name='add_alt'),
    path('lt-camp-phase/add', views.AddLT.as_view(), name='add_lt'),
    path('sl-special-event/add', views.AddSLSpecialEvent.as_view(), name='add_slse'),
]
