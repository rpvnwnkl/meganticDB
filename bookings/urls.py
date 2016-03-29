from django.conf.urls import url, include

from . import views
from . import forms

from . import reservation_views as Res
from . import member_views as Mem

from bookings.info_views import CampsInfoView

from bookings.info_views import CampArchive
from bookings.info_views import CampYearArchive
from bookings.info_views import CampMonthArchive

reservation_patterns = [
        # list of reservations
        url(
            r'^list/$',
            Res.ReservationListView.as_view(),
            name='reservation_list',
            ),
        # new reservation form
        url(
            r'^new/$',
            Res.ReservationCreate.as_view(),
            name='reservation_new',
            ),
        url(
            r'^new/(?P<pk>[0-9]*)$', 
            Res.ReservationCreate.as_view(),
            name='reservation_new',
            ),
        # view reservation info
        url(
            r'^(?P<pk>[0-9]+)/$',
            Res.ReservationDetailView.as_view(),
            name='reservation_detail',
            ),
        # edit reservation form
        url(
            r'^(?P<pk>[0-9]+)/edit/$',
            Res.reservation_edit, 
            name='reservation_edit',
            ),
        # delete reservation
        url(
            r'^(?P<pk>[0-9]+)/remove/$',
            Res.reservation_delete,
            name='reservation_delete',
            ),
       ]
member_patterns = [
        # member list
        url(
            r'^list/$',
            Mem.MemberListView.as_view(),
            name='member_list',
            ),
        # new member
        url(
            r'^new/$',
            Mem.MemberCreate.as_view(),
            name='member_new',
            ),
        # update member
        url(
            r'^edit/(?P<pk>[0-9]+)/$',
            Mem.MemberUpdate.as_view(),
            name='member_update',
            ),
        # delete member
        url(r'^(?P<pk>[0-9]+)/delete/$',
            Mem.MemberDelete.as_view(),
            name='member_delete',
            ),
        # member details
        url(
            r'^(?P<pk>[0-9]+)/$',
            Mem.MemberDetailView.as_view(),
            name='member_detail',
            ),
        ]
archive_patterns = [
        url(
            r'^$',
            Res.ReservationArchiveView.as_view(),
                name="reservation_archive",
                ),
        url(
            r'^(?P<year>[0-9]{4})/$',
            Res.ReservationYearArchiveView.as_view(),
            name="reservation_year_archive",
            ),
        url(
            r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
            Res.ReservationMonthArchiveView.as_view(),
            name="reservation_month_archive",
            ),
        url(
            r'^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$',
            Res.ReservationWeekArchiveView.as_view(),
            name="archive_week",
            ),
        url(
            r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]{2})/$',
            Res.ReservationDayArchiveView.as_view(),
            name="reservation_day_archive",
            ),
       ]
base_info_patterns = [
        url(r'^camps/$',
            CampsInfoView.as_view(),
            name="camp_info",
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
        url(r'^member/', include(member_patterns)),
        url(r'^camp/', include(camp_patterns)),
        ] 
