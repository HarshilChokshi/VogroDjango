from django.urls import path
from . import views

urlpatterns = [
    #Just a test function
    path('auth_test', views.auth_test),
    path('refresh_token', views.refresh_token),
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
    path('matched_task/move_back/<int:task_id>', views.moveMatchedTaskBackToTask),
    path('matched_task/volunteer_user/<str:user_id>', views.getAllMatchedTasksBelongingToVolunteerUser),
    #UnMatched Task endpoints
    path('unmatched_task/repost_task/<int:task_id>', views.repostTask),
    # Completed Task endpoints
    path('completed_task/volunteer_user/<str:user_id>', views.getAllCompletedTasksBelongingToVolunteerUser),
]
