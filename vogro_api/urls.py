from django.urls import path
from . import views

urlpatterns = [
    # Volunteer user endpoints
    path('volunteer_user/add_user', views.addVolunteerUser),
    path('volunteer_user/<str:user_id>', views.volunteerUser),
    # Client user endpoints
    path('client_user/add_user', views.addClientUser),
    path('client_user/<int:user_id>', views.clientUser),
    # Task endpoints
    path('task/create_task', views.createTask),
    path('task/<int:task_id>', views.task),
    path('task/get_nearby_tasks', views.getNearByTasks),
    # Matched Task endpoints
    path('matched_task/<int:task_id>', views.matchedTask),
    path('matched_task/volunteer_user/<str:user_id>', views.getAllMatchedTasksBelongingToVolunteerUser),
    # Completed Task endpoints
    path('completed_task/volunteer_user/<str:user_id>', views.getAllCompletedTasksBelongingToVolunteerUser),
]
