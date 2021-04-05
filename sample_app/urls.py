app_name = "sample_app"
from django.urls import path
from . import views

urlpatterns = [
    # Task
    path('task/all/', views.task_list, name="task_list"),
    path('task/<int:task_id>/', views.task_details, name="task_details"),
    path('task/new/', views.create_task, name="create_task"), 
    path('task/new/add', views.add_task, name="add_task"), 
    # set task response as closed/completed

    # Task Responses
    path('task/<int:task_id>/response/<int:response_id>/', views.response_details, name="response_details"),
    path('task/<int:task_id>/response/new/', views.create_response, name="create_response"),
    # set task response as accepted
]