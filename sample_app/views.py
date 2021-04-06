from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseRedirect

# Create your views here.

# VIEWS FOR TASKS
def create_task(request):
    task = {}
    context = {'task': task}
    return render(request, 'create_task.html', context)

def add_task(request) :
    if request.method == 'POST':
        post = request.POST
        task_name = post['task_name'].strip()
        img_url = post['img_url'].strip()
        num_responses = post['num_responses'].strip()
        q1 = post['q1'].strip()
        q2 = post['q2'].strip()
        q3 = post['q3'].strip()
        # call task API
        print("REQUEST:",post)
        task_id = 1
        return HttpResponse(status=200,content=str(task_id))
    else:
        return HttpResponse(status=400)

def task_list(request):
    # events = call get tasks API
    task = {
        "id": "1",
        "q1": "find this",
        "q2": "find that",
        "q3": "find there",
        "created_by": "USER ADMIN",
        "date_created": "today",
        "num_responses": "10",
        "num_completed": "5"
    }
    tasks = []
    tasks.append(task)
    context = {'tasks': tasks}
    return render(request, 'tasks.html', context)

def task_details(request, task_id):
    # get task API
    name = "Special task name"
    img_url = "https://i.imgur.com/FTIHC7d.jpg"
    q1 = "find this"
    q2 = "find that"
    q3 = "find there"
    status = "active"
    num_responses = "5"
    num_completed = "3"

    task = {"name": name,
            "img_url": img_url,
            "q1": q1,
            "q2": q2,
            "q3": q3,
            "status": status,
            "num_responses": num_responses,
            "num_completed": num_completed
        }

    response = {
        "id": "1",
        "q1": "not here",
        "q2": "not that",
        "q3": "not then",
        "created_by": "USER 1",
        "date_created": "today"
    }
    responses = []
    responses.append(response)

    context = {'task': task,
               'responses': responses    
            }
    return render(request, 'task_details.html', context)

# VIEWS FOR TASK RESPONSES
def create_response(request, task_id):
    task_id = "1"
    name = "Special task name"
    img_url = "https://i.imgur.com/FTIHC7d.jpg"
    q1 = "find this"
    q2 = "find that"
    q3 = "find there"
    status = "active"
    num_responses = "5"
    num_completed = "3"

    task = {"id": task_id,
            "name": name,
            "img_url": img_url,
            "q1": q1,
            "q2": q2,
            "q3": q3,
            "status": status,
            "num_responses": num_responses,
            "num_completed": num_completed
        }
    context = {'task': task}
    return render(request, 'create_response.html', context)

def add_response(request) :
    # do soemthing
    b = 0

def response_details(request, task_id, response_id):
    # get response API
    response = {
        "id": "1",
        "q1": "not here",
        "q2": "not that",
        "q3": "not then",
        "created_by": "USER 1",
        "date_created": "today"
    }
    context = {'response': response}
    return render(request, 'response_details.html', context)