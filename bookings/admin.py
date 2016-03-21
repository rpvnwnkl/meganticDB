from django.contrib import admin

from .models import Person, Member, Guide, Camp, Reservation, ReservationDetail

#myModels = [Member, Guide, Camp, Reservation, Specific]
#admin.site.register(myModels)
# Register your models here.
admin.site.register(Member)

admin.site.register(Guide)

admin.site.register(Camp)

#admin.site.register(ReservationDetail)

#class SpecificInline(admin.TabularInline):
    #model = Specific
    
    

class ReservationAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Member Info', {'fields': ['member', 'party_size']}),
            ('Logistics', {'fields': ['arrival', 'departure', 'first_meal', 'last_meal']}),
            ]
    #inlines = [SpecificInline]
    list_display = ('member', 'id', 'arrival')
    list_filter = ['arrival']

class DetailAdmin(admin.ModelAdmin):
    list_display = ('day', 'id', 'reservation')
    list_filter = ['id', 'day']


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservationDetail, DetailAdmin)
