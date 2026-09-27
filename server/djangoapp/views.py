from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .restapis import get_request, analyze_review_sentiments, post_review

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
from .models import CarMake, CarModel
def get_cars(request):
    car_models = CarModel.objects.select_related("car_make").all()

    car_models_list = []

    for car_model in car_models:
        car_models_list.append({
            "CarMake": car_model.car_make.name,
            "CarModel": car_model.name
        })

    return JsonResponse({
        "CarModels": car_models_list
    })

def get_dealers(request, state=None):
    if state:
        dealers = get_request(f"/fetchDealers/{state}")
    else:
        dealers = get_request("/fetchDealers")

    return JsonResponse({
        "status": 200,
        "dealers": dealers
    })

def get_dealer(request, dealer_id):
    dealer = get_request(f"/fetchDealer/{dealer_id}")
    return JsonResponse({
        "status": 200,
        "dealer": dealer
    })

def get_dealer_reviews(request, dealer_id):
    reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")

    if reviews:
        for review in reviews:
            sentiment_data = analyze_review_sentiments(
                review.get("review", "")
            )

            if sentiment_data:
                review["sentiment"] = sentiment_data.get("sentiment")

    return JsonResponse({
        "status": 200,
        "reviews": reviews
    })

@csrf_exempt
def add_review(request):
    data = json.loads(request.body)

    review = post_review(data)

    return JsonResponse({
        "status": 200,
        "review": review
    })