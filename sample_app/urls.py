app_name = "sample_app"
from django.urls import path
from . import views

urlpatterns = [
    # Task
    path('', views.home, name="home"), # if no URL is provided, go to task list page
    path('task/all/', views.task_list, name="task_list"), # URL to view all tasks (task list page)
    path('task/', views.task_details, name="task_details"), # URL to view task details for a given task ID
    path('task/new/', views.create_task, name="create_task"), # URL for create task page
    path('task/<int:task_id>/update/<str:update>/<str:auth_token>/', views.update_task, name="update_task"), # URL to update task status to Closed or to set it again to Open
    # Task Responses
    path('response/', views.response_details, name="response_details"), # URL to view response details for a given response ID and task ID
    path('response/new/', views.create_response, name="create_response"), # URL for create response page for a given task ID
    path('response/<int:response_id>/judge/<int:judgement>/<str:auth_token>/', views.judge_response, name="judge_response") # URL to approve/reject responses
]