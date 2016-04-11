from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.forms import modelformset_factory
from django.shortcuts import redirect, render

from django.http import HttpResponse
from django.template import loader
from django import forms

from django.utils import timezone

from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from .models import Reservation, ReservationDetail

from .forms import SearchDatesForm, ReservationStepOne 
from .forms import DailyDetailsForm, BaseDetailsFormSet, ReservationUpdateForm


from . import forms


import datetime
# Create your views here.

def index(request):
    latest_reservation_list = Reservation.objects.order_by('arrival')[:5]
    template = loader.get_template('bookings/index.html')
    context = {
            'latest_reservation_list': latest_reservation_list,
            }
    return HttpResponse(template.render(context, request))

class SearchFormView(FormView):
    template_name = 'bookings/search_page.html'
    form_class = SearchDatesForm
    success_url = '/search/'

    def get(self, request, *args, **kwargs):
        if request.GET:
            form = SearchDatesForm(self.request.GET)
            if form.is_valid():
                search_results = True
                context = self.get_context_data(*args, **kwargs)
                context['form'] = form
                context['search_results'] = search_results
                print ('\nform data', form.cleaned_data)
                context['the_results'] = self.search_tool(form.cleaned_data)
                return render(request, 'bookings/search_page.html', context)
            else:
                return render(request, 'bookings/search_page.html', {'form':form})
        else:
            return super(SearchFormView, self).get(request, *args, **kwargs)
    
    def clean(self):
        print('\nclean method now starting\n')
        cleaned_data = super(SearchDatesForm, self).clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        
        if check_in and check_out:
            print('hello')
            if check_in < check_out:
                raise forms.ValidationError(
                        "Check-in and Check-out dates are not possible."
                        )

    def form_valid(self, form):
        return super(SearchFormView, self).form_valid(form)
    
    def get_context_data(self, *args, **kwargs):
        context = super(SearchFormView, self).get_context_data(*args, **kwargs)
        print('\ncontext: ', context)
        print('\nself.request: ', self.request)
        print('\nself.request.GET: ', self.request.GET)
        return context

    def search_tool(self, data):
        check_in = data['check_in']
        check_out = data['check_out']
        num_guests = data['guests']
        return Reservation.objects.filter(arrival__gte=check_in, arrival__lte=check_out, departure__lte=check_out, departure__gte=check_in)

##################################
### Reservation Step-Thru Form ###
##################################


class ReservationFormViewOne(FormView):
    form_class = ReservationStepOne
    template_name = 'bookings/reservation/step_one.html'
    success_url = 'step_two/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.created_on = timezone.now()
            reservation.save()

            return forms.create_res_details(request, reservation.pk)
        else:
            return self.form_invalid(form, **kwargs)
'''
class ReservationFormViewTwo(UpdateView):
    template_name = 'bookings/reservation/step_two.html'
    form_class = ReservationStepTwo

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            reservationdetail = form.save(commit=False)
            #if not reservationdetail.is_last_day:
'''

class SearchResultsView(TemplateView):
    template_name = 'bookings/search_results.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchResultsView, self).get_context_data(*args, **kwargs)
        print('context: ', context)
        print('self.request: ', self.request)
        print('self.request.GET: ', self.request.GET)
        return context

def search_form(request):
    if request.method == 'POST':
        form = SearchDatesForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = SearchDatesForm()
        return render(request, 'bookings/search_page.html', {'form': form})
def year_archive(request, year):
    year_entries = Reservation.objects.filter(arrival__year=year)
    entry_dicts = [entry.archive_dict() for entry in year_entries]
    context = {
            'year': year,
            'year_entries': entry_dicts,
            }
    return render(request, 'bookings/year_archive.html', context)

def month_archive(request, year, month):
    month_entries = Reservation.objects.month_archive(year, month)
    entry_dicts = [entry.archive_dict() for entry in month_entries]
    context = {
            'year': year,
            'month': month,
            'month_entries': entry_dicts,
            }
    return render(request, 'bookings/month_archive.html', context)

def day_archive(request, year, month, day):
    day_entries = Reservation.objects.day_archive(int(year), int(month), int(day))
    entry_dicts = [entry.archive_dict() for entry in day_entries]
    context = {
            'year': year,
            'month': month,
            'day': day,
            'day_entries': day_entries,
            }
    return render(request, 'bookings/day_archive.html', context)


#################################
###   test_reservation_update ###
#################################

def test_reservation_update(request):
    """
    Allows user to update reservation details
    """
    reservation = request.GET['reservation']

    # Create the formset, specifying the form and formset we want to use
    DetailsFormSet = modelformset_factory(
                            ReservationDetail, 
                            fields=(
                                'camps', 
                                'num_guides', 
                                'eating_breakfast', 
                                'eating_lunch', 
                                'eating_dinner',
                                ),
                            formset=BaseDetailsFormSet,
                            )

    # Get our existing data for this reservation. This is used as initial data
    reservation_details = ReservationDetail.objects.filter(reservation=reservation).order_by('day_reserved')
    detail_data = [(0,
            {
                'camps': d.camps, 
                'eating_breakfast': d.eating_breakfast, 
                'eating_lunch': d.eating_lunch, 
                'eating_dinner': d.eating_dinner, 
                'num_guides': d.num_guides,
                }) 
            for d in reservation_details
            ]
    print(detail_data[0][1])
    if request.method == 'POST':
        reservation_form = ReservationUpdateForm(request.POST, initial={'reservation':reservation})
        details_formset = DailyDetailsForm(request.POST)

        if reservation_form.is_valid() and link_formset.is_valid():
            # save info
            reservation.arrival = reservation_form.cleaned_data.get('arrival')
            reservation.departure = reservation_form.cleaned_data.get('departure')
            reservation.save()

            # now save details data for each formset
            new_details = []

            for details_form in details_formset:
                camps = details_form.cleaned_data.get('camps')
                eating_breakfast = details_form.cleaned_data.get('eating_breakfast')
                eating_lunch = details_form.cleaned_data.get('eating_lunch')
                eating_dinner = details_form.cleaned_data.get('eating_dinner')
                num_guides = details_form.cleaned_data.get('num_guides')

                new_details.append(
                        ReservationDetail(
                            camps=camps, 
                            eating_breakfast=eating_breakfast, 
                            eating_lunch=eating_lunch, 
                            eating_dinner=eating_dinner, 
                            num_guides=num_guides
                            ))
            try:
                with transaction.atomic():
                #replace old with new
                    ReservationDetail.objects.filter(reservation=reservation).delete()
                    ReservationDetail.objects.bulk_create(new_details)

                    # and notify it worked
                    messages.success(request, 'You have updated the Reservation Details.')
            except IntegrityError: # if transaction fails
                messages.error(request, 'There was an error in saving the reservation  updates ')
                return redirect(reverse('reservation_detail'))

    else:
        reservation_form = ReservationUpdateForm(initial={'reservation':reservation})
        details_formset = DailyDetailsForm(initial=detail_data[0][1])

    context = {
        'reservation_form': reservation_form,
        'details_formset': details_formset,
        }
    print(context)
    return render(request, 'bookings/reservation/reservation_update.html', context)
