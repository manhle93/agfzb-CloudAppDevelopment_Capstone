from django.contrib import admin

# from .models import related models

# Register your models here.
from .models import CarModel
from .models import CarMake

# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    
# Register models here
admin.site.register(CarModel)
admin.site.register(CarMake)
