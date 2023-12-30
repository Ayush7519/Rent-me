from django.contrib import admin
from .models import Hostel
# Register your models here.
class Hostel_Admin(admin.ModelAdmin):
    list_display=('id',
                'photo',
                'photo1',
                'photo2',
                'hostel_name',
                'description', 
                'address',
                'contact',
                'price',
                'no_of_rooms', 
                'no_of_beds', 
                'rating',
                'high_recommendation',
                'date_created',
                'date_updated', 
                'no_of_bed_availabe',
                "owner",
                "approved",
            )

admin.site.register(Hostel,Hostel_Admin)
