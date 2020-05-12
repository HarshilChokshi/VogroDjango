from django.contrib import admin
from .models import *
from datetime import datetime, timedelta
import json

# Register your models here.
admin.site.register(VolunteerUser)
admin.site.register(ClientUser)
admin.site.register(MatchedTask)
admin.site.register(CompletedTask)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
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
