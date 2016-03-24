from django.conf.urls import url, include

from . import views
from bookings.archive_views import ReservationYearArchiveView
from bookings.archive_views import ReservationMonthArchiveView
from bookings.archive_views import ReservationWeekArchiveView
from bookings.archive_views import ReservationDayArchiveView
from bookings.archive_views import ReservationArchiveView

from bookings.info_views import MembersInfoView
from bookings.info_views import CampsInfoView
from bookings.info_views import ReservationInfoView

from bookings.info_views import CampArchive
from bookings.info_views import CampYearArchive
from bookings.info_views import CampMonthArchive


reservation_patterns = [
        url(r'^([0-9]+)/$', views.reservation_detail, name='reservation-detail'),
        url(r'^all/([0-9]{4})/$', views.year_archive, name='year-archive'),
        url(r'^all/([0-9]{4})/([0-9]{2})/$', views.month_archive, name='month-archive'),
        url(r'^all/([0-9]{4})/([0-9]{2})/([0-9]{2})/$', views.day_archive, name='day-archive'),
       ]
archive_patterns = [
        url(
            r'^$',
            ReservationArchiveView.as_view(),
                name="reservation_archive",
                ),
        url(
            r'^(?P<year>[0-9]{4})/$',
            ReservationYearArchiveView.as_view(),
            name="reservation_year_archive",
            ),
        url(
            r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
            ReservationMonthArchiveView.as_view(),
            name="reservation_month_archive",
            ),
        url(
            r'^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$',
            ReservationWeekArchiveView.as_view(),
            name="archive_week",
            ),
        url(
            r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]{2})/$',
            ReservationDayArchiveView.as_view(),
            name="reservation_day_archive",
            ),
       ]
base_info_patterns = [
        url(r'^members/$',
            MembersInfoView.as_view(),
            name="member_info",
            ),
        url(r'^camps/$',
            CampsInfoView.as_view(),
            name="camp_info",
            ),
        url(r'^reservation/(?P<pk>[0-9]+)/$',
            ReservationInfoView.as_view(),
            name="reservation_info",
            ),
       ]

camp_patterns = [
        url(r'^(?P<camp>[-\w ]+)/$',
            CampArchive.as_view(),
            name="camp_archive",
            ),
        url(r'^(?P<camp>[-\w ]+)/(?P<year>[0-9]{4})/$',
            CampYearArchive.as_view(),
            name="camp_year_archive",
            ),
        url(r'^(?P<camp>[-\w ]+)/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
            CampMonthArchive.as_view(),
            name="camp_month_archive",
            ),
        ]
urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^info/', include(base_info_patterns)),
        url(r'^archive/', include(archive_patterns)),
        url(r'^reservation/', include(reservation_patterns)),
        url(r'^camp/', include(camp_patterns)),
        url(r'^reservations/xml_detail/([0-9]+)/$', views.xml_detail),
        ] 
