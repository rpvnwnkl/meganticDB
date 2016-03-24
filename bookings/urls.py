from django.conf.urls import url, include

from . import views


reservation_patterns = [
        url(r'^([0-9]+)/$', views.reservation_detail, name='reservation-detail'),
        url(r'^all/([0-9]{4})/$', views.year_archive, name='year-archive'),
        url(r'^all/([0-9]{4})/([0-9]{2})/$', views.month_archive, name='month-archive'),
        url(r'^all/([0-9]{4})/([0-9]{2})/([0-9]{2})/$', views.day_archive, name='day-archive'),
       ]

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^reservation/', include(reservation_patterns)),
        url(r'^reservations/xml_detail/([0-9]+)/$', views.xml_detail),
        ] 
