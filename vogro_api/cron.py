from .models import Task, UnMatchedTask
from django.db.models import Q
from datetime import datetime

def moveAllExpiredTasksToUnMatchedTaskTable():
    # Grab all tasks that have expired
    expiredTasks = Task.objects.filter(latest_preferred_time__lt=datetime.utcnow())

    # Move all expired tasks to unmatched tasks table and then delete them
    for expiredTask in expiredTasks:
        unMatchedTask = UnMatchedTask(
            task_location = expiredTask.task_location,
            description = expiredTask.description,
            task_type = expiredTask.task_type,
            client_name = expiredTask.client_name,
            client_email = expiredTask.client_email,
            client_number = expiredTask.client_number,
            earliest_preferred_time = expiredTask.earliest_preferred_time,
            latest_preferred_time = expiredTask.latest_preferred_time,
            city = expiredTask.city,
            estimated_time = expiredTask.estimated_time
        )
        unMatchedTask.save()
        expiredTask.delete()
