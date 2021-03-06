from django.contrib import admin

from .models import Person, Member, Guide, GuideDetail, Camp, CampDetail, Reservation, ReservationDetail

#myModels = [Member, Guide, Camp, Reservation, Specific]
#admin.site.register(myModels)
# Register your models here.
admin.site.register(Member)

admin.site.register(Guide)

admin.site.register(Camp)

admin.site.register(CampDetail)

admin.site.register(GuideDetail)
class CampDetailInline(admin.TabularInline):
    model = CampDetail
    
    

class ReservationAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Member Info', {'fields': ['member']}),
            ('Logistics', {'fields': ['arrival', 'departure']}),
            ]
    #inlines = [SpecificInline]
    list_display = ('member', 'id', 'arrival')
    list_filter = ['arrival']

class DetailAdmin(admin.ModelAdmin):
    list_display = ('day_reserved', 'id', 'reservation')
    list_filter = ['day_reserved']
    inlines = [CampDetailInline]
    admin_order_field = 'reservation__id'


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservationDetail, DetailAdmin)
