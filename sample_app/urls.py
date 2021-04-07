app_name = "sample_app"
from django.urls import path
from . import views

urlpatterns = [
    # Task
    path('', views.task_list, name="task_list"), # if no URL is provided, go to task list page
    path('task/all/', views.task_list, name="task_list"), # URL to view all tasks (task list page)
    path('task/<int:task_id>/', views.task_details, name="task_details"), # URL to view task details for a given task ID
    path('task/new/', views.create_task, name="create_task"), # URL for create task page
    path('task/add/', views.add_task, name="add_task"), # URL to add a new task 
    path('task/<int:task_id>/update/<str:update>/', views.update_task, name="update_task"), # URL to update task status to Closed or to set it again to Open
    # Task Responses
    path('task/<int:task_id>/response/<int:response_id>/', views.response_details, name="response_details"), # URL to view response details for a given response ID and task ID
    path('task/<int:task_id>/response/new/', views.create_response, name="create_response"), # URL for create response page for a given task ID
    path('task/<int:task_id>/response/add/', views.add_response, name="add_response"), # URL to add a new response for a given task ID
    path('response/<int:response_id>/judge/<int:judgement>/', views.judge_response, name="judge_response") # URL to approve/reject responses
]