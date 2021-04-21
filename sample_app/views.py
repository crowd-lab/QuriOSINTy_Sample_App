from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseRedirect
import json
import requests
import datetime
from dateutil.parser import parse

# Set the base URL here:
API_BASE_URL = "https://quriosinty-dev.herokuapp.com/api/v1/"
# API_BASE_URL = "http://localhost:8080/api/v1/"
# Create your views here.

# VIEWS FOR TASKS
def home(request):
    return render(request, 'home.html')

def create_task(request):
    if request.method == 'GET':
        task = {}
        context = {'page_type': 'task',
                'task': task}
        return render(request, 'create_task.html', context)

    elif request.method == 'POST':
        post = request.POST
        # get it from the POST request
        auth_token = str(post['token'].strip())
        tool_id = int(post['tool'].strip())
        event_id = int(post['event'].strip()) 

        data = {"img_url":post['img_url'].strip(), "q1":post['q1'].strip(), "q2":post['q2'].strip(), "q3":post['q3'].strip()}

        # create the request object with data from the POST request
        request = { 
                    "tool": tool_id,
                    "event_id": event_id,
                    "name": post['task_name'].strip(),
                    "status": "Open",
                    "description": post['task_description'].strip(),
                    "time_estimate": post['time_estimate'].strip(),
                    "data": data,
                    "request_responses": int(post['num_responses'].strip())
                }
        print("DATA REQUEST", json.dumps(request))

        # sending post request and saving the response as response object
        url = API_BASE_URL + "task/" # URL for API call
        data = json.dumps(request) # convert dictionary to JSON
    
        headers = {'content-type': 'application/json', 'Authorization': 'Token {}'.format(auth_token)}  # header type and authorization
        response = requests.post(url = url, data = data, headers = headers) # make the post request
        data = response.json() # extracting response data in json format
        print("DATA RESPONSE Create Task", data, response)

        content = {
            "task": data["id"],
            "event": event_id,
            "token": auth_token,
            "tool": tool_id
        }
        return HttpResponse(status=200,content=json.dumps(content))
    
    else:
        return HttpResponse(status=400)

def update_task(request, task_id, update, auth_token):
    print("UPDATING TASK")
    patch = {} # create the patch object
    if update == "closed":
        patch = {"status": "Closed"} # set to Closed
    elif update == "open":
        patch = {"status": "Open"} # set to Opened
    else :
        return HttpResponse(status=400) # error

    # NOTE API CALL SETUP: call task GET API to update status of a task as closed
    url = API_BASE_URL + "task/"+str(task_id)+"/" # URL for API call
    
    data = json.dumps(patch) # convert dictionary to JSON

    headers = {'content-type': 'application/json', 'Authorization': 'Token {}'.format(auth_token)}  # header type and authorization
    response = requests.patch(url = url, data = data, headers = headers) # make the patch request [PATCH is for partial updates; while PUT updates all required fields; POST is for creating new objects]
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE", data)

    if response.status_code == 200: # if updating the task as closed was succesful
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

def task_list(request):
    # NOTE API CALL SETUP: call task GET API to get all tasks
    url = API_BASE_URL + "task/" # URL for API call
    response = requests.get(url = url) # make the get request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE TASK LIST", data)

    # parse the response
    tasks = []
    for task in data:
        if task["tool_name"] == "Photo Verification Sample App" : 
            # NOTE API CALL SETUP: call task GET API to get all responses for a given task 
            # NOTE This is an inefficient way to do it, we are working on an API call that just returns a) total number of responses and b) number of completed responses
            url = API_BASE_URL + "task/"+str(task['id'])+"/response" # URL for API call
            response = requests.get(url = url) # make the get request
            data = response.json() # extracting response data in json format
            print("DATA RESPONSE Task_Response", data)
            num_completed = len(data)

            data = task['data']
            temp_task = {
                "id": task['id'],
                "name": task['name'],
                "status": task['status'],
                "description": task['description'],
                "date_created": task['date_created'],
                "img_url": data['img_url'],
                "q1": data['q1'],
                "q2": data['q2'],
                "q3": data['q3'],
                "num_responses": task['request_responses'],
                "num_completed": num_completed
            }
            tasks.append(temp_task)

    context = {'page_type': 'task',
               'tasks': tasks}
    return render(request, 'tasks.html', context)

def task_details(request):
    # NOTE API CALL SETUP: call task GET API to get all responses for a given task 
    # NOTE This is an inefficient way to do it, we are working on an API call that just returns a) total number of responses and b) number of completed responses
    task_id = request.GET["task"]
    url = API_BASE_URL + "task/"+str(task_id)+"/response" # URL for API call
    response = requests.get(url = url) # make the get request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE Task_Response", data)
    num_completed = len(data)

    # NOTE API CALL SETUP: call task GET API to get one task
    url = API_BASE_URL + "task/"+str(task_id)+"/" # URL for API call
    response = requests.get(url = url) # make the get request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE Task", data)
    t_data = data['data']
    requested_responses = data['request_responses']

    task = {
            "id": data['id'],
            "name": data['name'],
            "status": data['status'],
            "description": data['description'],
            "date_created": data['date_created'],
            "img_url": t_data['img_url'],
            "q1": t_data['q1'],
            "q2": t_data['q2'],
            "q3": t_data['q3'],
            "num_responses": data['request_responses'],
            "num_completed": num_completed
        }

    # NOTE API CALL SETUP: call task GET API to get all responses for a given task
    url = API_BASE_URL + "task/"+str(task_id)+"/response" # URL for API call
    response = requests.get(url = url) # make the get request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE Task_Response", data)

    responses = []
    for response in data: 
        ans = response['data']
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

    responses_allowed = False
    print("NUMBER OF RESPONSES REQUESTED", requested_responses)
    print("NUMBER OF RESPONSES COMPLETED", num_completed)
    if num_completed < requested_responses :
        responses_allowed = True

    context = {'page_type': 'task',
               'token': request.GET["token"],
               'event': request.GET["event"],
               'tool': request.GET["tool"],
               'task': task,
               'responses': responses,
               'responses_allowed': responses_allowed   
            }
    return render(request, 'task_details.html', context)

# VIEWS FOR TASK RESPONSES
def create_response(request):
    if request.method == 'GET':
        # print("REQUEST",request.GET) # this is to view the URL query parameters (e.g., "/?token=<string>&event=<int>&tool=<tool>")
        auth_token = request.GET["token"] # get the authorization token for that user from the URL query string ("token=<string>")
        tool_id = int(request.GET["tool"]) # get the tool ID from the URL query string ("tool=<int>")
        event_id = int(request.GET["event"]) # get the event ID from the URL query string ("event=<int>")
        task_id = int(request.GET["task"]) # get the task ID from the URL query string ("task=<int>")

        # NOTE API CALL SETUP: call task GET API to get all responses for a given task 
        # NOTE This is an inefficient way to do it, we are working on an API call that just returns a) total number of responses and b) number of completed responses
        url = API_BASE_URL + "task/"+str(task_id)+"/response/" # URL for API call
        response = requests.get(url = url) # make the get request
        data = response.json() # extracting response data in json format
        print("DATA RESPONSE Task_Response", data)
        num_completed = len(data)

        # NOTE API CALL SETUP: call task GET API to get one task (to display to the user)
        url = API_BASE_URL + "task/"+str(task_id)+"/"  # URL for API call
        response = requests.get(url = url) # make the get request
        data = response.json() # extracting response data in json format
        print("DATA RESPONSE Task", data)

        t_data = data['data']
        task = {"id": data['id'],
                "name": data['name'],
                "status": data['status'],
                "description": data['description'],
                "date_created": data['date_created'],
                "img_url": t_data['img_url'],
                "q1": t_data['q1'],
                "q2": t_data['q2'],
                "q3": t_data['q3'],
                "num_responses": data['request_responses'],
                "num_completed": num_completed
            }

        responses_allowed = False
        print("NUMBER OF RESPONSES REQUESTED", data['request_responses'])
        print("NUMBER OF RESPONSES COMPLETED", num_completed)
        if num_completed < data['request_responses'] :
            responses_allowed = True

        context = {'page_type': 'response',
                'responses_allowed': responses_allowed,
                'task': task}
        return render(request, 'create_response.html', context)
    
    elif request.method == 'POST':
        post = request.POST
        auth_token = str(post['token'].strip())
        tool_id = int(post['tool'].strip())
        event_id = int(post['event'].strip()) 
        task_id = int(post['task'].strip())

        description = {"ans1":post['ans1'].strip(), "ans2":post['ans2'].strip(), "ans3":post['ans3'].strip()}

        # NOTE API CALL SETUP: call response POST API to add a new response for a given task ID
        # create the request object (don't foget to convert to json with json.dumps)
        request = { 
                    "task_id": task_id,
                    # "status": "Pending",
                    "data": description 
                }
        print("DATA REQUEST", json.dumps(request)) 

        # set up to make the POST request
        url = API_BASE_URL + "response/" # URL for API call
        data = json.dumps(request) # convert dictionary to JSON

        headers = {'content-type': 'application/json', 'Authorization': 'Token {}'.format(auth_token)}  # header type and authorization
        response = requests.post(url = url, data = data, headers = headers) # make the post request
        data = response.json() # extracting response data in json format
        print("DATA RESPONSE", data)

        content = {
            "response": data["id"],
            "task": task_id,
            "event": event_id,
            "token": auth_token,
            "tool": tool_id
        }
        return HttpResponse(status=200,content=json.dumps(content))

    else:
        return HttpResponse(status=400)

def judge_response(request, response_id, judgement, auth_token):
    decision = "Pending"
    if judgement == 0:
        decision = "Approved"
    elif judgement == 1:
        decision = "Rejected"
    else :
        pass

    # NOTE API CALL SETUP: call task PATCH API to update the status of a response
    patch = {"status": decision} # create the patch object
    data = json.dumps(patch) # convert dictionary to JSON
    print("UPDATE Task_Response to: ", patch)
    url = API_BASE_URL + "response/"+str(response_id)+"/" # URL for API call

    headers = {'content-type': 'application/json', 'Authorization': 'Token {}'.format(auth_token)}  # header type and authorization
    response = requests.put(url = url, data = data, headers = headers) # make the post request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE", data)

    if response.status_code == 200: # if updating the response was succesful
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

def response_details(request):
    # NOTE API CALL SETUP: call response GET API to get one response
    response_id = request.GET["response"]
    url = API_BASE_URL + "response/"+str(response_id)+"/" # URL for API call
    response = requests.get(url = url) # make the get request
    data = response.json() # extracting response data in json format
    print("DATA RESPONSE", data)

    # API returns the response and its parent task details, parse it
    task_id = data["task_id"]
    # NOTE API CALL SETUP: call task GET API to get one task
    url = API_BASE_URL + "task/"+str(task_id)+"/" # URL for API call
    response = requests.get(url = url) # make the get request
    t_data = response.json() # extracting response data in json format
    print("DATA RESPONSE Task", t_data)
    t_qdata = t_data['data']
    requested_responses = t_data['request_responses']

    task = {
            "id": task_id,
            "created_by": t_data['created_by'],
            "name": t_data['name'],
            "status": t_data['status'],
            "description": t_data['description'],
            "date_created": t_data['date_created'],
            "img_url": t_qdata['img_url'],
            "q1": t_qdata['q1'],
            "q2": t_qdata['q2'],
            "q3": t_qdata['q3'],
            "num_responses": t_data['request_responses'],
        }
    
    # API returns response details, parse the response
    ans = data['data']
    response_data = {
        "id": data['id'],
        "ans1": ans['ans1'],
        "ans2": ans['ans2'],
        "ans3": ans['ans3'],
        "created_by": data['created_by'],
        "date_created": data['date_created'],
        "status": data['status']
    }
    print("RESPONSE",response_data)

    auth_token = request.GET["token"]
    url = API_BASE_URL + "task/"+str(task_id)+"/istaskowner/" # URL for API call
    headers = {'content-type': 'application/json', 'Authorization': 'Token {}'.format(auth_token)}  # header type and authorization
    response = requests.get(url = url, headers = headers) # make the patch request [PATCH is for partial updates; while PUT updates all required fields; POST is for creating new objects]
    is_task_owner = False
    if response.status_code != 404:
        owner_data = response.json() # extracting response data in json format
        print("DATA RESPONSE IsTaskOwner:", owner_data)
        is_task_owner = str(owner_data["IsTaskOwner"])

    context = {'page_type': 'response',
               'task':task,
               'response': response_data,
               'is_task_owner': is_task_owner
              }
    return render(request, 'response_details.html', context)