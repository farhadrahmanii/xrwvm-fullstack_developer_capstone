from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1


class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_make', 'type', 'year']


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
