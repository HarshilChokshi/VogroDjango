import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .constants import *
from .view_helpers import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import operator

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        # user.set_password(validated_data['password'])
        user.save()
        return user

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def auth_test(request, format=None):
    content = {
        'user': "test_user",  # `django.contrib.auth.User` instance.
        'auth': "test_auth",  # None
    }
    return Response(content)

@api_view(['POST'])
@permission_classes((AllowAny,))
def refresh_token(request):
    # Transforming data for User table
    data = request.data
    data['username'] = data['id']

    serialized = UserSerializer(data=data)
    refresh_user = User.objects.get(username=data['id'])
    token, created =  Token.objects.get_or_create(user=refresh_user)
    if created: #A user needs to be created first
        return HttpResponse('Create a user first', status=status.HTTP_400_BAD_REQUEST)
    token.delete()
    token = Token.objects.create(user=refresh_user)
    token.save()
    response = {}
    response['Authorization'] = f'Token {token.key}'
    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    # Transforming data for User table
    data = request.data
    data['username'] = data['id']

    serialized = UserSerializer(data=data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
# @api_view(['POST'])
# @permission_classes((AllowAny,))
@csrf_exempt
def addVolunteerUser(request):
    # Make sure request is POST method and content type is application/json
    if request.method != 'POST':
        return HttpResponse('Only the POST verb can be used on this endpoint.', status=405)

    # get the request body and convert it to python dict object
    body_dict = json.loads(request.body)

    #Creates user used for token authentication
    create_user(request)
    token = Token.objects.create(user=User.objects.get(username=body_dict['id']))

    # Create the VolunteerUser object and save it to database
    volunteerUser = VolunteerUser(
        id = body_dict['id'],
        first_name = body_dict['first_name'],
        last_name = body_dict['last_name'],
        email = body_dict['email'],
        phone_number = body_dict['phone_number'],
        is_verified = body_dict['is_verified'],
        has_used_app = body_dict['has_used_app'],
        city_id = body_dict['city'],
    )

    # Save the user to the database and return response.
    volunteerUser.save()
    response = {}
    response['Authorization'] = f'Token {token.key}'
    return JsonResponse(response, status=200)



@csrf_exempt
def volunteerUser(request, user_id):
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
            if field_name == 'city':
                volunteerUser.city.city_name = field_new_value
            else:
                setattr(volunteerUser, field_name, field_new_value)
        volunteerUser.save()
        return HttpResponse('Successfully updated VolunteerUser object', status=200)
    else:
        return HttpResponse('Only the GET and PATCH verbs can be used on this endpoint.', status=405)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def addClientUser(request):
    # Make sure request is POST method and content type is application/json
    if request.method != 'POST':
        return HttpResponse('Only the POST verb can be used on this endpoint.', status=405)

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



@api_view(['GET', 'PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def clientUser(request, user_id):
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

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def createTask(request):
    # Make sure request is POST method and content type is application/json
    if request.method != 'POST':
        return HttpResponse('Only the POST verb can be used on this endpoint.', status=405)

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
        task_type_id = body_dict['task_type'],
        client_name = body_dict['client_name'],
        client_email = body_dict['client_email'],
        client_number = body_dict['client_number'],
        earliest_preferred_time = earliest_preferred_time,
        latest_preferred_time = latest_preferred_time,
        city_id = body_dict['city'],
        estimated_time = body_dict['estimated_time'],
    )
    task.save()
    return HttpResponse('Successfully added Task object', status=200)


@api_view(['POST', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def task(request, task_id):
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
            VolunteerUser.objects.get(id=volunteer_id)
        except VolunteerUser.DoesNotExist:
            return HttpResponse(f'Volunteer with id: {volunteer_id}, does not exist', status=404)

        # Create the MatchedTask object and save to database
        matchedTask = MatchedTask(
            volunteer_id_id = volunteer_id,
            task_location = task.task_location,
            description = task.description,
            task_type = task.task_type,
            client_name = task.client_name,
            client_email = task.client_email,
            client_number = task.client_number,
            earliest_preferred_time = task.earliest_preferred_time,
            latest_preferred_time = task.latest_preferred_time,
            city = task.city,
            estimated_time = task.estimated_time,
        )
        matchedTask.save()

        # Delete the task object
        task.delete()

        return HttpResponse(f'Successfully created MatchedTask object', status=200)
    else:
        return HttpResponse('Only the POST and DELETE verbs can be used on this endpoint.', status=405)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getNearByTasks(request):
    # Make sure request is POST method and content type is application/json
    if request.method != 'POST':
        return HttpResponse('Only the POST verb can be used on this endpoint.', status=405)

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

    tasksNearMeTupleSet = []

    for task in taskResultSet:
        # Parse out the task location lat and long
        task_address_dict = json.loads(task.task_location)
        task_lat = task_address_dict['lat']
        task_long = task_address_dict['long']

        # Get the distance
        distance = getMeterDistanceBetweenTwoLocations(volunteer_lat, volunteer_long, task_lat, task_long)

        # Filter by radius
        if distance <= radius:
            taskTuple = (Task.convertToJsonDict(task), distance)
            tasksNearMeTupleSet.append(taskTuple)

    # Sort the resuts by distance
    tasksNearMeTupleSet.sort(key=operator.itemgetter(1))

    # Convert the set of tuples to json
    sortedTasksJsonList = []
    for task in tasksNearMeTupleSet:
        task_dict = {}
        task_dict['task'] = task[0]
        task_dict['distance'] = task[1]
        sortedTasksJsonList.append(task_dict)

    # return json object
    return JsonResponse({'task_list': sortedTasksJsonList});


@api_view(['POST', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def matchedTask(request, task_id):
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
            client_email = task.client_email,
            client_number = task.client_number,
            earliest_preferred_time = task.earliest_preferred_time,
            latest_preferred_time = task.latest_preferred_time,
            city = task.city,
            estimated_time = task.estimated_time,
        )
        completedTask.save()

        # Delete the matched task object
        task.delete()

        return HttpResponse(f'Successfully created CompletedTask object', status=200)
    else:
        return HttpResponse('Only the POST and DELETE verbs can be used on this endpoint.', status=405)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def moveMatchedTaskBackToTask(request, task_id):
    # Make sure method is POST and the content type is application/json
    if request.method != 'POST':
        return HttpResponse('Only the POST verb can be used on this endpoint.', status=405)

    # Grab the tasks object from database
    matchedTask = None
    try:
        matchedTask = MatchedTask.objects.get(id=task_id)
    except MatchedTask.DoesNotExist:
          return HttpResponse(f'MatchedTask with id: {task_id}, does not exist', status=404)

    # Create the task object and save to database
    task = Task(
        task_location = matchedTask.task_location,
        description = matchedTask.description,
        task_type = matchedTask.task_type,
        client_name = matchedTask.client_name,
        client_email = matchedTask.client_email,
        client_number = matchedTask.client_number,
        earliest_preferred_time = matchedTask.earliest_preferred_time,
        latest_preferred_time = matchedTask.latest_preferred_time,
        city = matchedTask.city,
        estimated_time = matchedTask.estimated_time,
    )
    task.save()

    # Delete the matched task object
    matchedTask.delete()

    return HttpResponse(f'Successfully moved MatchedTask back to Task.', status=200)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllMatchedTasksBelongingToVolunteerUser(request, user_id):
    # Make sure request is GET method and content type is application/json
    if request.method != 'GET':
        return HttpResponse('Only the GET verb can be used on this endpoint.', status=405)

    matchedTaskList = MatchedTask.objects.filter(volunteer_id_id=user_id)

    matchedTaskJsonList = []
    for task in matchedTaskList:
        matchedTaskJsonList.append(MatchedTask.convertToJsonDict(task))

    return JsonResponse({'task_list': matchedTaskJsonList})


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def repostTask(request, task_id):
    # Make sure request is POST method and content type is application/json
    if request.method != 'POST':
        return HttpResponse('Only the POST verb can be used on this endpoint.', status=405)

    # Grab the unmatched task from database
    unMatchedTask = None
    try:
        unMatchedTask = UnMatchedTask.objects.get(id=task_id)
    except UnMatchedTask.DoesNotExist:
          return HttpResponse(f'UnMatchedTask with id: {task_id}, does not exist', status=404)

    # Grab the new datetimes from the request
    body_dict = json.loads(request.body)
    newEarliestPreferredTime = datetime.strptime(body_dict['earliest_preferred_time'], dateFormatString)
    newLatestPreferredTime = datetime.strptime(body_dict['latest_preferred_time'], dateFormatString)

    # Create the task object and save to database and delete the unmatched task
    task = Task(
        task_location = unMatchedTask.task_location,
        description = unMatchedTask.description,
        task_type = unMatchedTask.task_type,
        client_name = unMatchedTask.client_name,
        client_email = unMatchedTask.client_email,
        client_number = unMatchedTask.client_number,
        earliest_preferred_time = newEarliestPreferredTime,
        latest_preferred_time = newLatestPreferredTime,
        city = unMatchedTask.city,
        estimated_time = unMatchedTask.estimated_time,
    )
    task.save()

    unMatchedTask.delete()
    return HttpResponse(f'Successfully moved UnMatchedTask to Task.', status=200)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllCompletedTasksBelongingToVolunteerUser(request, user_id):
    # Make sure request is GET method and content type is application/json
    if request.method != 'GET':
        return HttpResponse('Only the GET verb can be used on this endpoint.', status=405)

    completedTaskList = CompletedTask.objects.filter(volunteer_id_id=user_id).order_by('-latest_preferred_time')

    completedaskJsonList = []
    for task in completedTaskList:
        completedaskJsonList.append(CompletedTask.convertToJsonDict(task))

    return JsonResponse({'task_list': completedaskJsonList})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllCities(request):
    # Make sure request is GET method and content type is application/json
    if request.method != 'GET':
        return HttpResponse('Only the GET verb can be used on this endpoint.', status=405)

    # Grab all the cities
    cities = City.objects.all()
    city_list = []

    # Parse out the city name string from each one
    for city in cities:
        city_list.append(city.city_name)

    # Return json object
    return JsonResponse({'cities': city_list})
