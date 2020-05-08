from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(VolunteerUser)
admin.site.register(ClientUser)
admin.site.register(Task)
admin.site.register(MatchedTask)
admin.site.register(CompletedTask)
