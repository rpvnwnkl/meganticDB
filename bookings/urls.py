from django.conf.urls import url, include

from . import views

from . import reservation_views as Res
from . import member_views as Mem
from . import camp_views as Cam
from . import guide_views as Gui
from . import reservationdetail_views as ResD

guide_detail_patterns = [
        # list of guides on reservation
        url(
            r'^$',
            Gui.GuideDetailReservation.as_view(),
            name='guide_detail_reservation',
            ),
        # new guide detail
        url(
            r'^new/$',
            Gui.GuideDetailCreate.as_view(),
            name='guide_detail_new',
            ),
        # update guide detail
        url(
            r'^edit/(?P<reservation_detail>[0-9]+)/$',
            Gui.GuideDetailUpdate.as_view(),
            name='guide_detail_update',
            ),
        # delete guide detail
        url(r'^(?P<pk>[0-9]+)/delete/$',
            Gui.GuideDetailDelete.as_view(),
            name='guide_detail_delete',
            ),
        # guide detail details
        #url(
         #   r'^(?P<pk>[0-9]+)/$',
          #  Gui.GuideDetailDetailView.as_view(),
           # name='guide_detail_detail',
            #),
       # url(
        #    r'^reservation/(?P<reservation>[0-9]+)/$',
         #   Gui.GuideDetailReservation.as_view(),
          #  name='guide_detail_reservation',
           # ),
        ]

reservation_patterns = [
        # list of reservations
        url(
            r'^$',
            Res.ReservationListView.as_view(),
            name='reservation_list',
            ),
        # new reservation form
        url(
            r'^new/$',
            Res.ReservationCreate.as_view(),
            name='reservation_new',
            ),
        # new res for particular member
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
            r'^edit/(?P<pk>[0-9]+)/$',
            Res.ReservationUpdate.as_view(), 
            name='reservation_update',
            ),
        # delete reservation
        url(
            r'^remove/(?P<pk>[0-9]+)/$',
            Res.ReservationDelete.as_view(),
            name='reservation_delete',
            ),
        # edit guide details
        url(
            r'^(?P<pk>[0-9]+)/guides/', include(guide_detail_patterns)),

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

camp_patterns = [
        # camp list
        url(
            r'^list/$',
            Cam.CampListView.as_view(),
            name='camp_list',
            ),
        # new camp
        url(
            r'^new/$',
            Cam.CampCreate.as_view(),
            name='camp_new',
            ),
        # update camp
        url(
            r'^edit/(?P<pk>[0-9]+)/$',
            Cam.CampUpdate.as_view(),
            name='camp_update',
            ),
        # delete camp
        url(r'^(?P<pk>[0-9]+)/delete/$',
            Cam.CampDelete.as_view(),
            name='camp_delete',
            ),
        # camp details
        url(
            r'^(?P<pk>[0-9]+)/$',
            Cam.CampDetailView.as_view(),
            name='camp_detail',
            ),
        # camps month schedule
        url(
            r'^schedule/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
            Cam.CampMonthlySchedule.as_view(),
            name='camp_month_schedule',
            ),
        url(
            r'^reservation/(?P<reservation>[0-9]+)/$',
            Cam.CampReservation.as_view(),
            name='camp_reservation',
            ),
        ]

guide_patterns = [
        # guide list
        url(
            r'^list/$',
            Gui.GuideListView.as_view(),
            name='guide_list',
            ),
        # new guide
        url(
            r'^new/$',
            Gui.GuideCreate.as_view(),
            name='guide_new',
            ),
        # update guide
        url(
            r'^edit/(?P<pk>[0-9]+)/$',
            Gui.GuideUpdate.as_view(),
            name='guide_update',
            ),
        # delete guide
        url(r'^(?P<pk>[0-9]+)/delete/$',
            Gui.GuideDelete.as_view(),
            name='guide_delete',
            ),
        # guide details
        url(
            r'^(?P<pk>[0-9]+)/$',
            Gui.GuideDetailView.as_view(),
            name='guide_detail',
            ),
        #url(
         #r'^reservation/(?P<reservation>[0-9]+)/$',
          #Gui.GuideReservation.as_view(),
           # name='guide_reservation',
            #),
        ]

resdetail_patterns = [
        # resdetail list
        url(
            r'^list/$',
            ResD.ReservationDetailListView.as_view(),
            name='resdetail_list',
            ),
        # new resdetail
        url(
            r'^new/$',
            ResD.ReservationDetailCreate.as_view(),
            name='resdetail_new',
            ),
        # update resdetail
        url(
            r'^edit/(?P<pk>[0-9]+)/$',
            ResD.ReservationDetailUpdate.as_view(),
            name='resdetail_update',
            ),
        # delete resdetail
        url(r'^(?P<pk>[0-9]+)/delete/$',
            ResD.ReservationDetailDelete.as_view(),
            name='resdetail_delete',
            ),
        # resdetail details
        url(
            r'^(?P<pk>[0-9]+)/$',
            ResD.ReservationDetailDetailView.as_view(),
            name='resdetail_detail',
            ),
        ]


urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^search/$', views.SearchFormView.as_view(), name='search_form'),
        url(r'^search-results/$', views.SearchResultsView.as_view(), name='search_results'),
        url(r'^reservation/', include(reservation_patterns)),
        url(r'^member/', include(member_patterns)),
        url(r'^camp/', include(camp_patterns)),
        url(r'^guide/', include(guide_patterns)),
        url(r'^resdetail/', include(resdetail_patterns)),
        ] 
