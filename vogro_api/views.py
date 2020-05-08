import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .constants import *
from .view_helpers import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

# Create your views here.
@csrf_exempt
def addVolunteerUser(request):
    # Make sure request is POST method and content type is application/json
    if request.method != 'POST':
        return HttpResponse('Only the POST verb can be used on this endpoint.', status=405)
    if request.content_type != 'application/json':
        return HttpResponse('The content-type must be application/json.', status=415)

    # get the request body and convert it to python dict object
    body_dict = json.loads(request.body)

    # Create the VolunteerUser object and save it to database
    volunteerUser = VolunteerUser(
        id = body_dict['id'],
        full_name = body_dict['full_name'],
        email = body_dict['email'],
        phone_number = body_dict['phone_number'],
        persona_id = body_dict['persona_id'],
        persona_government_id_url = body_dict['persona_government_id_url'],
        is_verified = body_dict['is_verified'],
    )

    # Save the user to the database and return response.
    volunteerUser.save()
    return HttpResponse('Successfully added VolunteerUser object', status=200)



@csrf_exempt
def volunteerUser(request, user_id):
    # Make sure content type is application/json
    if request.content_type != 'application/json':
        return HttpResponse('The content-type must be application/json.', status=415)

    # grab the volunteer user from db
    volunteerUser = None
    try:
        volunteerUser = VolunteerUser.objects.get(id=user_id)
    except VolunteerUser.DoesNotExist:
        return HttpResponse(f'Volunteer user with id: {user_id}, does not exist', status=404)

    # Make sure request is GET or PATCH
    if request.method == 'GET':
        volunteerUser_dict = VolunteerUser.convertToJsonDict(volunteerUser)
        return JsonResponse(volunteerUser_dict)
    elif request.method == 'PATCH':
        # Get the request body
        body_dict = json.loads(request.body)
        fields_to_change_list = body_dict['fields_to_change']
        for field_name, field_new_value in fields_to_change_list.items():
            try:
                getattr(volunteerUser, field_name)
            except AttributeError:
                continue
            setattr(volunteerUser, field_name, field_new_value)
        volunteerUser.save()
        return HttpResponse('Successfully updated VolunteerUser object', status=200)
    else:
        return HttpResponse('Only the GET and PATCH verbs can be used on this endpoint.', status=405)



@csrf_exempt
def addClientUser(request):
    # Make sure request is POST method and content type is application/json
    if request.method != 'POST':
        return HttpResponse('Only the POST verb can be used on this endpoint.', status=405)
    if request.content_type != 'application/json':
        return HttpResponse('The content-type must be application/json.', status=415)

    # get the request body and convert it to python dict object
    body_dict = json.loads(request.body)

    # Serialize address to strings
    user_address_string = json.dumps(body_dict['address'])

    # Create the ClientUser object and save it to database
    clientUser = ClientUser(
        full_name = body_dict['full_name'],
        email = body_dict['email'],
        phone_number = body_dict['phone_number'],
        address = user_address_string,
        address_name = body_dict['address_name'],
        reason = body_dict['reason'],
    )

    # Save the object to the database and return response
    clientUser.save()
    return HttpResponse('Successfully added ClientUser object', status=200)



@csrf_exempt
def clientUser(request, user_id):
    # Make sure content type is application/json
    if request.content_type != 'application/json':
        return HttpResponse('The content-type must be application/json.', status=415)

    # grab the client user from db
    clientUser = None
    try:
        clientUser = ClientUser.objects.get(id=user_id)
    except ClientUser.DoesNotExist:
        return HttpResponse(f'Client user with id: {user_id}, does not exist', status=404)

    # Make sure request is GET or PATCH
    if request.method == 'GET':
        clientUser_dict = ClientUser.convertToJsonDict(clientUser)
        return JsonResponse(clientUser_dict)
    elif request.method == 'PATCH':
        # Get the request body
        body_dict = json.loads(request.body)
        fields_to_change_list = body_dict['fields_to_change']
        for field_name, field_new_value in fields_to_change_list.items():
            try:
                getattr(clientUser, field_name)
            except AttributeError:
                continue
            if field_name == 'address':
                field_new_value = json.dumps(field_new_value)
            setattr(clientUser, field_name, field_new_value)
        # Save the client object to the database and return response
        clientUser.save()
        return HttpResponse('Successfully updated ClientUser object', status=200)
    else:
        return HttpResponse('Only the GET and PATCH verbs can be used on this endpoint.', status=405)

@csrf_exempt
def createTask(request):
    # Make sure request is POST method and content type is application/json
    if request.method != 'POST':
        return HttpResponse('Only the POST verb can be used on this endpoint.', status=405)
    if request.content_type != 'application/json':
        return HttpResponse('The content-type must be application/json.', status=415)

    # get the request body and convert it to python dict object
    body_dict = json.loads(request.body)

    # Serialize task location
    task_location_string = json.dumps(body_dict['task_location'])

    # Parse out datetime objects from strings in json
    earliest_preferred_time = datetime.strptime(body_dict['earliest_preferred_time'], dateFormatString)
    latest_preferred_time = datetime.strptime(body_dict['latest_preferred_time'], dateFormatString)

    # Create the Task object and save to database
    task = Task(
        task_location = task_location_string,
        description = body_dict['description'],
        task_type = body_dict['task_type'],
        client_name = body_dict['client_name'],
        client_number = body_dict['client_number'],
        earliest_preferred_time = earliest_preferred_time,
        latest_preferred_time = latest_preferred_time,
    )
    task.save()
    return HttpResponse('Successfully added Task object', status=200)


@csrf_exempt
def task(request, task_id):
    # Make sure the content type is application/json
    if request.content_type != 'application/json':
        return HttpResponse('The content-type must be application/json.', status=415)

    # Grab the taks object from database
    task = None
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
          return HttpResponse(f'Task with id: {task_id}, does not exist', status=404)

    if request.method == 'DELETE':
        task.delete()
        return HttpResponse(f'Successfully deleted Task object with id {task_id}', status=200)
    elif request.method == 'POST':
        # grab volunteer id from request body
        body_dict = json.loads(request.body)
        volunteer_id = body_dict['volunteer_id']

        # Check if volunteer with id exists in database
        try:
            Volunteer.objects.get(id=volunteer_id)
        except Volunteer.DoesNotExist:
            return HttpResponse(f'Volunteer with id: {volunteer_id}, does not exist', status=404)

        # Create the MatchedTask object and save to database
        matchedTask = MatchedTask(
            volunteer_id_id = volunteer_id,
            task_location = task.task_location,
            description = task.description,
            task_type = task.task_type,
            client_name = task.client_name,
            client_number = task.client_number,
            earliest_preferred_time = task.earliest_preferred_time,
            latest_preferred_time = task.latest_preferred_time,
        )
        matchedTask.save()

        # Delete the task object
        task.delete()

        return HttpResponse(f'Successfully created MatchedTask object', status=200)
    else:
        return HttpResponse('Only the POST and DELETE verbs can be used on this endpoint.', status=405)


@csrf_exempt
def getNearByTasks(request):
    # Make sure request is POST method and content type is application/json
    if request.method != 'POST':
        return HttpResponse('Only the GET verb can be used on this endpoint.', status=405)
    if request.content_type != 'application/json':
        return HttpResponse('The content-type must be application/json.', status=415)

    # get the request body and convert it to python dict object
    body_dict = json.loads(request.body)

    # Parse out the time from the body_dict
    volunteerUserEarliestTime = datetime.strptime(body_dict['earliest_preferred_time'], dateFormatString)
    volunteerUserLatestTime = datetime.strptime(body_dict['latest_preferred_time'], dateFormatString)

    # Parse out lat, long, and target radius from dict object
    volunteer_lat = body_dict['lat']
    volunteer_long = body_dict['long']
    radius = body_dict['radius']

    # Set the time filters for query
    earliestTimeFilter = Q(earliest_preferred_time__range=[volunteerUserEarliestTime, volunteerUserLatestTime])
    latestTimeFilter = Q(latest_preferred_time__range=[volunteerUserEarliestTime, volunteerUserLatestTime])

    # run the query and filter by time
    taskResultSet = Task.objects.filter(earliestTimeFilter | latestTimeFilter)

    tasksNearMeList = []

    for task in taskResultSet:
        # Parse out the task location lat and long
        task_address_dict = json.loads(task.task_location)
        task_lat = task_address_dict['lat']
        task_long = task_address_dict['long']

        # Get the distance
        distance = getMeterDistanceBetweenTwoLocations(volunteer_lat, volunteer_long, task_lat, task_long)

        # Filter by radius
        if distance <= radius:
            tasksNearMeList.append(Task.convertToJsonDict(task))

    # return json object
    return JsonResponse(tasksNearMeList)


@csrf_exempt
def matchedTask(request, task_id):
    # Make sure the content type is application/json
    if request.content_type != 'application/json':
        return HttpResponse('The content-type must be application/json.', status=415)

    # Grab the tasks object from database
    task = None
    try:
        task = MatchedTask.objects.get(id=task_id)
    except MatchedTask.DoesNotExist:
          return HttpResponse(f'MatchedTask with id: {task_id}, does not exist', status=404)

    if request.method == 'DELETE':
        task.delete()
        return HttpResponse(f'Successfully deleted MatchedTask object with id {task_id}', status=200)
    elif request.method == 'POST':
        # Create the CompletedTask object and save to database
        completedTask = CompletedTask(
            volunteer_id_id = task.volunteer_id.id,
            task_location = task.task_location,
            description = task.description,
            task_type = task.task_type,
            client_name = task.client_name,
            client_number = task.client_number,
            earliest_preferred_time = task.earliest_preferred_time,
            latest_preferred_time = task.latest_preferred_time,
        )
        completedTask.save()

        # Delete the matched task object
        task.delete()

        return HttpResponse(f'Successfully created CompletedTask object', status=200)
    else:
        return HttpResponse('Only the POST and DELETE verbs can be used on this endpoint.', status=405)


@csrf_exempt
def moveMatchedTaskBackToTask(request, task_id):
    # Make sure method is POST and the content type is application/json
    if request.method != 'POST':
        return HttpResponse('Only the POST verb can be used on this endpoint.', status=405)
    if request.content_type != 'application/json':
        return HttpResponse('The content-type must be application/json.', status=415)

    # Grab the tasks object from database
    matchedTask = None
    try:
        matchedTask = MatchedTask.objects.get(id=task_id)
    except MatchedTask.DoesNotExist:
          return HttpResponse(f'MatchedTask with id: {task_id}, does not exist', status=404)

    # Create the task object and save to database
    task = Task(
        task_location = task.task_location,
        description = task.description,
        task_type = task.task_type,
        client_name = task.client_name,
        client_number = task.client_number,
        earliest_preferred_time = task.earliest_preferred_time,
        latest_preferred_time = task.latest_preferred_time,
    )
    task.save()

    # Delete the matched task object
    matchedTask.delete()

    return HttpResponse(f'Successfully moved MatchedTask back to Task.', status=200)


@csrf_exempt
def getAllMatchedTasksBelongingToVolunteerUser(request, user_id):
    # Make sure request is GET method and content type is application/json
    if request.method != 'GET':
        return HttpResponse('Only the GET verb can be used on this endpoint.', status=405)
    if request.content_type != 'application/json':
        return HttpResponse('The content-type must be application/json.', status=415)

    matchedTaskList = MatchedTask.objects.filter(volunteer_id_id=user_id)

    matchedTaskJsonList = []
    for task in matchedTaskList:
        matchedTaskJsonList.append(MatchedTask.convertToJsonDict(task))

    return JsonResponse({"result_list": matchedTaskJsonList})


@csrf_exempt
def getAllCompletedTasksBelongingToVolunteerUser(request, user_id):
    # Make sure request is GET method and content type is application/json
    if request.method != 'GET':
        return HttpResponse('Only the GET verb can be used on this endpoint.', status=405)
    if request.content_type != 'application/json':
        return HttpResponse('The content-type must be application/json.', status=415)

    completedTaskList = CompletedTask.objects.filter(volunteer_id_id=user_id)

    completedaskJsonList = []
    for task in completedTaskList:
        completedaskJsonList.append(CompletedTask.convertToJsonDict(task))

    return JsonResponse({"result_list": completedaskJsonList})
