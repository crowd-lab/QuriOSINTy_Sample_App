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
        
        # NOTE API CALL SETUP: call task POST API to add a new task to the database for a given flag ID
        flag_id = "1" # this should not be fixed (in the future), we need to associate a task to a specific verification flag
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
        print("DATA REQUEST", json.dumps(request))

        # sending post request and saving the response as response object
        url = "https://quriosinty-dev.herokuapp.com/api/v1/task/" # URL for API call
        data = json.dumps(request) # convert dictionary to JSON
        headers = {'content-type': 'application/json'} # header type
        response = requests.post(url = url, data = data, headers = headers) # make the post request
        data = response.json() # extracting response data in json format
        print("DATA RESPONSE", data)

        task_id = data["id"]
        return HttpResponse(status=200,content=str(task_id)) # return task ID
    else:
        return HttpResponse(status=400)

def close_task(request, task_id):
    # NOTE API CALL SETUP: call task GET API to add a new task to the database for a given flag ID
    url = "https://quriosinty-dev.herokuapp.com/api/v1/task/"+str(task_id)+"/" # URL for API call
    patch = {"status": "Closed"} # create the patch object
    data = json.dumps(patch) # convert dictionary to JSON
    headers = {'content-type': 'application/json'} # header type
    response = requests.patch(url = url, data = data, headers = headers) # make the patch request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE", data) 

    if response.status_code == 200: # if updating the task as closed was succesful
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

def task_list(request):
    # NOTE API CALL SETUP: call task GET API to get all tasks
    url = "https://quriosinty-dev.herokuapp.com/api/v1/task/" # URL for API call
    response = requests.get(url = url) # make the get request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE", data)

    # parse the response
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
    # NOTE API CALL SETUP: call task GET API to get one task
    url = "https://quriosinty-dev.herokuapp.com/api/v1/task/"+str(task_id)+"/" # URL for API call
    response = requests.get(url = url) # make the get request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE Task", data)
    description = json.loads(data['description'])

    task = {
            "id": data['id'],
            "name": data['name'],
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

    # NOTE API CALL SETUP: call task GET API to get all responses for a given task
    url = "https://quriosinty-dev.herokuapp.com/api/v1/task/"+str(task_id)+"/response" # URL for API call
    response = requests.get(url = url) # make the get request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE Task_Response", data)

    responses = []
    for response in data: 
        ans = json.loads(response['data'])
        temp_response = { 
                    "id": response['id'],
                    "date_created": response['date_created'],
                    "created_by": response['created_by'],
                    "status": response['status'],
                    "ans1": ans['ans1'],
                    "ans2": ans['ans2'],
                    "ans3": ans['ans3'],
                }
        print("TEMP RESPONSE", temp_response)
        responses.append(temp_response)

    context = {'task': task,
               'responses': responses    
            }
    return render(request, 'task_details.html', context)

# VIEWS FOR TASK RESPONSES
def create_response(request, task_id):
    # NOTE API CALL SETUP: call task GET API to get one task (to display to the user)
    url = "https://quriosinty-dev.herokuapp.com/api/v1/task/"+str(task_id)+"/"  # URL for API call
    response = requests.get(url = url) # make the get request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE", data)

    description = json.loads(data['description'])
    task = {"name": data['name'],
            "status": data['status'],
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
        description = {"ans1":ans1, "ans2":ans2, "ans3":ans3}

        # NOTE API CALL SETUP: call response POST API to add a new response for a given task ID
        # create the request object (don't foget to convert to json with json.dumps)
        request = { 
                    "task": task_id,
                    "created_by": "Response User",
                    "status": "Pending",
                    "data": str(json.dumps(description)) # convert dictionary to JSON
                }
        print("DATA REQUEST", json.dumps(request)) 

        # set up to make the POST request
        url = "https://quriosinty-dev.herokuapp.com/api/v1/response/" # URL for API call
        data = json.dumps(request) # convert dictionary to JSON
        headers = {'content-type': 'application/json'} # header type
        response = requests.post(url = url, data = data, headers = headers) # make the post request
        data = response.json() # extracting response data in json format
        print("DATA RESPONSE", data)

        task_id = data["id"]
        return HttpResponse(status=200,content=str(task_id)) # return task ID
    else:
        return HttpResponse(status=400)

def close_response(request, task_id, response_id):
    # NOTE API CALL SETUP: call task GET API to add a new task to the database for a given flag ID
    url = "https://quriosinty-dev.herokuapp.com/api/v1/task/"+str(task_id)+"/" # URL for API call
    patch = {"status": "Closed"} # create the patch object
    data = json.dumps(patch) # convert dictionary to JSON
    headers = {'content-type': 'application/json'} # header type
    response = requests.patch(url = url, data = data, headers = headers) # make the patch request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE", response)

def response_details(request, task_id, response_id):
    # NOTE API CALL SETUP: call response GET API to get one response
    url = "https://quriosinty-dev.herokuapp.com/api/v1/response/"+str(response_id)+"/" # URL for API call
    response = requests.get(url = url) # make the get request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE", data)

    # API returns the response and its parent task details, parse it
    description = json.loads(data['task']['description'])
    task = {"name": data['task']['name'],
            "status": data['task']['status'],
            "date_created": data['task']['date_created'],
            "img_url": description['img_url'],
            "q1": description['q1'],
            "q2": description['q2'],
            "q3": description['q3'],
            "num_responses": data['task']['request_responses'],
            "num_completed": "0"
        }
    
    # API returns response details, parse the response
    ans = json.loads(data['data'])
    response = {
        "id": data['id'],
        "ans1": ans['ans1'],
        "ans2": ans['ans2'],
        "ans3": ans['ans3'],
        "created_by": data['created_by'],
        "date_created": data['date_created'],
        "status": data['status']
    }

    context = {'task':task, 'response': response}
    return render(request, 'response_details.html', context)