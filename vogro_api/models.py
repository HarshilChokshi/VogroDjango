from django.db import models
import json
#from .constants import *
from datetime import datetime
from .constants import *

# Classes to be used by model Classes
class Location(object):
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    @staticmethod
    def createFromJsonDict(jsonDict):
        return Location(jsonDict['lat'], jsonDict['lng'])


# Create your models here.
class City(models.Model):
    city_name = models.CharField(max_length=50, primary_key=True)


class TaskType(models.Model):
    task_type = models.CharField(max_length=30, primary_key=True)


class VolunteerUser(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=25)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    is_verified  = models.BooleanField(default=False)
    has_used_app = models.BooleanField(default=False)


    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @staticmethod
    def convertToJsonDict(volunteerUser):
        return {
            'id': volunteerUser.id,
            'first_name': volunteerUser.first_name,
            'last_name': volunteerUser.last_name,
            'email': volunteerUser.email,
            'phone_number': volunteerUser.phone_number,
            'city': volunteerUser.city.city_name,
            'is_verified': volunteerUser.is_verified,
            'has_used_app': volunteerUser.has_used_app,
        }


class ClientUser(models.Model):
    full_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    address_name = models.CharField(max_length=100)
    reason = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

    @staticmethod
    def convertToJsonDict(clientUser):
        return {
            'id': clientUser.id,
            'full_name': clientUser.full_name,
            'email': clientUser.email,
            'phone_number': clientUser.phone_number,
            'address': json.loads(clientUser.address),
            'address_name': clientUser.address_name,
            'reason': clientUser.reason,
        }


class Task(models.Model):
    task_location = models.TextField()
    description = models.TextField()
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=30)
    client_email = models.CharField(max_length=50)
    client_number = models.CharField(max_length=20)
    earliest_preferred_time = models.DateTimeField()
    latest_preferred_time = models.DateTimeField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    estimated_time = models.CharField(max_length=20)

    def __str__(self):
        return self.task_type + ' (' + self.client_name + ')'

    @staticmethod
    def convertToJsonDict(task):
        return {
            "id": task.id,
            "task_location": json.loads(task.task_location),
            "description": task.description,
            "task_type": task.task_type.task_type,
            "client_name": task.client_name,
            "client_email": task.client,
            "client_number": task.client_number,
        	"earliest_preferred_time": task.earliest_preferred_time.strftime(dateFormatString),
        	"latest_preferred_time": task.latest_preferred_time.strftime(dateFormatString),
            "city": task.city.city,
            "estimated_time": task.estimated_time,
        }


class UnMatchedTask(models.Model):
    task_location = models.TextField()
    description = models.TextField()
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=30)
    client_email = models.CharField(max_length=50)
    client_number = models.CharField(max_length=20)
    earliest_preferred_time = models.DateTimeField()
    latest_preferred_time = models.DateTimeField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    estimated_time = models.CharField(max_length=20)

    def __str__(self):
        return self.task_type + ' (' + self.client_name + ')'

    @staticmethod
    def convertToJsonDict(task):
        return {
            "id": task.id,
            "task_location": json.loads(task.task_location),
            "description": task.description,
            "task_type": task.task_type.task_type,
            "client_name": task.client_name,
            "client_email": task.client,
            "client_number": task.client_number,
        	"earliest_preferred_time": task.earliest_preferred_time.strftime(dateFormatString),
        	"latest_preferred_time": task.latest_preferred_time.strftime(dateFormatString),
            "city": task.city.city,
            "estimated_time": task.estimated_time,
        }


class MatchedTask(models.Model):
    volunteer_id = models.ForeignKey(VolunteerUser, on_delete=models.CASCADE)
    task_location = models.TextField()
    description = models.TextField()
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=30)
    client_email = models.CharField(max_length=50)
    client_number = models.CharField(max_length=20)
    earliest_preferred_time = models.DateTimeField()
    latest_preferred_time = models.DateTimeField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    estimated_time = models.CharField(max_length=20)

    def __str__(self):
        return self.task_type + ' (' + self.client_name + ')'

    @staticmethod
    def convertToJsonDict(task):
        return {
            "id": task.id,
            "volunteer_id": task.volunteer_id.id,
            "task_location": json.loads(task.task_location),
            "description": task.description,
            "task_type": task.task_type.task_type,
            "client_name": task.client_name,
            "client_email": task.client,
            "client_number": task.client_number,
        	"earliest_preferred_time": task.earliest_preferred_time.strftime(dateFormatString),
        	"latest_preferred_time": task.latest_preferred_time.strftime(dateFormatString),
            "city": task.city.city,
            "estimated_time": task.estimated_time,
        }

class CompletedTask(models.Model):
    volunteer_id = models.ForeignKey(VolunteerUser, on_delete=models.CASCADE)
    task_location = models.TextField()
    description = models.TextField()
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=30)
    client_email = models.CharField(max_length=50)
    client_number = models.CharField(max_length=20)
    earliest_preferred_time = models.DateTimeField()
    latest_preferred_time = models.DateTimeField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    estimated_time = models.CharField(max_length=20)

    def __str__(self):
        return self.task_type + ' (' + self.client_name + ')'

    @staticmethod
    def convertToJsonDict(task):
        return {
            "id": task.id,
            "volunteer_id": task.volunteer_id.id,
            "task_location": json.loads(task.task_location),
            "description": task.description,
            "task_type": task.task_type.task_type,
            "client_name": task.client_name,
            "client_email": task.client,
            "client_number": task.client_number,
        	"earliest_preferred_time": task.earliest_preferred_time.strftime(dateFormatString),
        	"latest_preferred_time": task.latest_preferred_time.strftime(dateFormatString),
            "city": task.city.city,
            "estimated_time": task.estimated_time,
        }
