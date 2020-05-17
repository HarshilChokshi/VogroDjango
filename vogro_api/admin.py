from django.contrib import admin
from .models import *
from .constants import *
from datetime import datetime, timedelta
import json


# Defined filters
class TaskByCityFilter(admin.SimpleListFilter):
    title = 'Task City'
    parameter_name = 'task_city'


    def lookups(self, request, model_admin):
        lookUpsList = []

        for city in ontarioCitiesList:
            cityTuple = (city, city)
            lookUpsList.append(cityTuple)

        return lookUpsList


    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()

        return queryset.filter(city=self.value())



class VolunteerUserByCityFilter(admin.SimpleListFilter):
    title = 'Volunteer City'
    parameter_name = 'volunteer_city'


    def lookups(self, request, model_admin):
        lookUpsList = []

        for city in ontarioCitiesList:
            cityTuple = (city, city)
            lookUpsList.append(cityTuple)

        return lookUpsList


    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()

        return queryset.filter(city=self.value())


class VolunteerUserByVerifiedFilter(admin.SimpleListFilter):
    title = 'Volunteer Verification'
    parameter_name = 'volunteer_verification'


    def lookups(self, request, model_admin):
        return [
            ('verified', 'verified'),
            ('not verified', 'not verified')
        ]


    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()

        isVerified = self.value() == 'verified'

        return queryset.filter(is_verified=isVerified)


class VolunteerUserByUsedAppFilter(admin.SimpleListFilter):
    title = 'Verified Volunteer App Usage'
    parameter_name = 'verified_volunteer_app_usage'


    def lookups(self, request, model_admin):
        return [
            ('y', 'used app at least once'),
            ('n', 'not used app')
        ]


    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()

        hasUsedApp = self.value() == 'y'

        return queryset.filter(has_used_app=hasUsedApp)


# Register models in amdin
@admin.register(VolunteerUser)
class VolunteerUserAdmin(admin.ModelAdmin):
    list_filter = (VolunteerUserByVerifiedFilter, VolunteerUserByUsedAppFilter, VolunteerUserByCityFilter)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = (TaskByCityFilter,)

    def save_model(self, request, obj, form, change):
        # Only make changes if user is adding object
        if(change is False):
            # Add 4 hours to the datetimes
            obj.earliest_preferred_time = obj.earliest_preferred_time + timedelta(hours=4)
            obj.latest_preferred_time = obj.latest_preferred_time + timedelta(hours=4)

            # Parse the lat,long and covert to json string
            locationList = obj.task_location.split(',')
            lat = locationList[0].strip()
            long = locationList[1].strip()
            locationDict = {
                "lat": float(lat),
                "long": float(long)
            }
            obj.task_location = json.dumps(locationDict)
        super().save_model(request, obj, form, change)

@admin.register(MatchedTask)
class MatchedTaskAdmin(admin.ModelAdmin):
    list_filter = (TaskByCityFilter,)

@admin.register(UnMatchedTask)
class UnMatchedTaskAdmin(admin.ModelAdmin):
    list_filter = (TaskByCityFilter,)

@admin.register(CompletedTask)
class CompletedTaskAdmin(admin.ModelAdmin):
    list_filter = (TaskByCityFilter,)
