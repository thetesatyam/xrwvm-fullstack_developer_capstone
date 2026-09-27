from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
import logging
import json
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


# Login
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)

    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)

    data = {"userName": username}

    if user is not None:
        login(request, user)
        data = {
            "userName": username,
            "status": "Authenticated"
        }

    return JsonResponse(data)


# Logout
def logout_request(request):
    logout(request)

    data = {
        "userName": "",
        "status": "Logged out"
    }

    return JsonResponse(data)


# Registration
@csrf_exempt
def registration(request):
    data = json.loads(request.body)

    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("{} is a new user".format(username))

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        login(request, user)

        data = {
            "userName": username,
            "status": "Authenticated"
        }

        return JsonResponse(data)

    data = {
        "userName": username,
        "error": "Already Registered"
    }

    return JsonResponse(data)