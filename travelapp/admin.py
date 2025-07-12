from django.contrib import admin
from .models import Package, Booking, Passenger, Payment, Client

# Register your models here.

class PackageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("package_name","country")}

admin.site.register(Package,PackageAdmin)
admin.site.register(Booking)
admin.site.register(Passenger)
admin.site.register(Payment)
admin.site.register(Client)