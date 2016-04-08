from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms

from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from .models import Reservation
from .forms import SearchDatesForm, ReservationStepOne


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
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

class ReservationFormViewTwo(TemplateView):
    template_name = 'bookings/reservation/step_two.html'

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

