from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseRedirect
import json
import requests
import datetime
from dateutil.parser import parse

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
        num_responses = int(post['num_responses'].strip())
        q1 = post['q1'].strip()
        q2 = post['q2'].strip()
        q3 = post['q3'].strip()
        
        # call task POST API
        flag_id = "1"
        description = {"img_url":img_url, "q1":q1, "q2":q2, "q3":q3}

        # create the request object (don't foget to convert to json with json.dumps)
        request = { 
                    "tool_name": "Photo Verification Sample App",
                    "name": task_name,
                    "status": "Open",
                    "description": str(json.dumps(description)),
                    "request_responses": num_responses,
                    "flag": {
                        "id": flag_id
                    }
                }
        # print("DATA REQUEST", json.dumps(request))
        # sending post request and saving the response as response object
        url = "https://quriosinty-dev.herokuapp.com/api/v1/task/"
        data = json.dumps(request) # convert to json parseable format
        headers = {'content-type': 'application/json'} # header type
        response = requests.post(url = url, data = data, headers = headers)
        # extracting response data in json format
        data = response.json()
        # print("DATA RESPONSE", data)
        task_id = data["id"]
        return HttpResponse(status=200,content=str(task_id)) # return task ID
    else:
        return HttpResponse(status=400)

def task_list(request):
    # call tasks GET API to get all tasks
    url = "https://quriosinty-dev.herokuapp.com/api/v1/task/"
    response = requests.get(url = url)
    data = response.json()
    print("DATA RESPONSE", data)
    # template_task = {
    #     "id": "1",
    #     "q1": "find this",
    #     "q2": "find that",
    #     "q3": "find there",
    #     "created_by": "USER ADMIN",
    #     "date_created": "today",
    #     "num_responses": "10",
    #     "num_completed": "5"
    # }
    tasks = []
    for task in data:
        if task["tool_name"] == "Photo Verification Sample App" :
            description = json.loads(task['description'])
            temp_task = {
                "id": task['id'],
                "name": task['name'],
                "status": task['status'],
                # "created_by": data['created_by'],
                "date_created": task['date_created'],
                "img_url": description['img_url'],
                "q1": description['q1'],
                "q2": description['q2'],
                "q3": description['q3'],
                "num_responses": task['request_responses'],
                "num_completed": "0"
            }
            tasks.append(temp_task)

    context = {'tasks': tasks}
    return render(request, 'tasks.html', context)

def task_details(request, task_id):
    # call task GET API to get one task
    url = "https://quriosinty-dev.herokuapp.com/api/v1/task/"+str(task_id)+"/"
    response = requests.get(url = url)
    data = response.json()
    # print("DATA RESPONSE",data)
    description = json.loads(data['description'])

    task = {"name": data['name'],
            "status": data['status'],
            # "created_by": data['created_by'],
            "date_created": data['date_created'],
            "img_url": description['img_url'],
            "q1": description['q1'],
            "q2": description['q2'],
            "q3": description['q3'],
            "num_responses": data['request_responses'],
            "num_completed": "0"
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
    # call task GET API to get one task
    url = "https://quriosinty-dev.herokuapp.com/api/v1/task/"+str(task_id)+"/"
    response = requests.get(url = url)
    data = response.json()
    
    description = json.loads(data['description'])

    task = {"name": data['name'],
            "status": data['status'],
            # "created_by": data['created_by'],
            "date_created": data['date_created'],
            "img_url": description['img_url'],
            "q1": description['q1'],
            "q2": description['q2'],
            "q3": description['q3'],
            "num_responses": data['request_responses'],
            "num_completed": "0"
        }

    context = {'task': task}
    return render(request, 'create_response.html', context)


def add_response(request, task_id) :
    if request.method == 'POST':
        post = request.POST
        ans1 = post['ans1'].strip()
        ans2 = post['ans2'].strip()
        ans3 = post['ans3'].strip()
        
        # call response POST API
        description = {"ans1":ans1, "ans2":ans2, "ans3":ans3}

        # create the request object (don't foget to convert to json with json.dumps)
        request = { 
                    "task": task_id,
                    "created_by": "Response User",
                    "status": "Pending",
                    "data": str(json.dumps(description))
                }
        # print("DATA REQUEST", json.dumps(request))
        # sending post request and saving the response as response object
        url = "https://quriosinty-dev.herokuapp.com/api/v1/response/"
        data = json.dumps(request) # convert to json parseable format
        headers = {'content-type': 'application/json'} # header type
        response = requests.post(url = url, data = data, headers = headers)
        # extracting response data in json format
        data = response.json()
        print("DATA RESPONSE",data)
        task_id = data["id"]
        return HttpResponse(status=200,content=str(task_id)) # return task ID
    else:
        return HttpResponse(status=400)

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