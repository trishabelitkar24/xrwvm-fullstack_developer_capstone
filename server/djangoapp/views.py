
from pathlib import Path
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from .restapis import get_request, post_review, analyze_review_sentiments
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Login view
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            data = {
                "userName": username,
                "status": "Authenticated"
            }
        else:
            data = {
                "userName": username,
                "status": "Invalid credentials"
            }

        return JsonResponse(data)

    return JsonResponse({"error": "POST request required"}, status=405)


# Logout view
@csrf_exempt
def logout_request(request):
    if request.method == 'GET' or request.method == 'POST':
        username = request.user.username if request.user.is_authenticated else ""
        logout(request)

        data = {
            "userName": username,
            "status": "Logged out"
        }
        return JsonResponse(data)

    return JsonResponse({"error": "GET or POST request required"}, status=405)


# Get unique car makes and models
def get_cars(request):
    if request.method == 'GET':
        data_file = (
            Path(__file__).resolve().parent.parent
            / 'database'
            / 'data'
            / 'car_records.json'
        )

        with open(data_file, 'r') as file:
            data = json.load(file)

        car_models = []
        seen = set()

        for car in data['cars']:
            pair = (car['make'], car['model'])

            if pair not in seen:
                seen.add(pair)
                car_models.append({
                    'CarMake': car['make'],
                    'CarModel': car['model']
                })

        return JsonResponse({'CarModels': car_models})

    return JsonResponse({'error': 'GET request required'}, status=405)


# Get all dealers or dealers filtered by state
def get_dealers(request, state=None):
    if request.method == 'GET':

        if state and state != 'All':
            endpoint = f'fetchDealers/{state}'
        else:
            endpoint = 'fetchDealers'

        dealers = get_request(endpoint)

        if dealers is None:
            return JsonResponse({
                'status': 503,
                'dealers': []
            }, status=503)

        return JsonResponse({
            'status': 200,
            'dealers': dealers
        })

    return JsonResponse({
        'error': 'GET request required'
    }, status=405)


# Get an individual dealer by ID
def get_dealer(request, dealer_id):
    if request.method == 'GET':

        dealer = get_request(f'fetchDealer/{dealer_id}')

        if dealer is None:
            return JsonResponse({
                'status': 503,
                'dealer': []
            }, status=503)

        return JsonResponse({
            'status': 200,
            'dealer': dealer
        })

    return JsonResponse({
        'error': 'GET request required'
    }, status=405)


@csrf_exempt
def add_review(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            review_text = data.get('review', '')
            sentiment = analyze_review_sentiments(review_text)

            if sentiment is not None:
                data['sentiment'] = sentiment

            response = post_review(data)

            if response is not None:
                return JsonResponse({'status': 200})

            return JsonResponse({
                'status': 503,
                'error': 'Unable to submit review'
            }, status=503)

        except (json.JSONDecodeError, KeyError, TypeError) as error:
            logger.error("Review submission error: %s", error)
            return JsonResponse({
                'status': 400,
                'error': 'Invalid review data'
            }, status=400)

    return JsonResponse({
        'error': 'POST request required'
    }, status=405)


# Get reviews for a specific dealer
def get_reviews(request, dealer_id):
    reviews = get_request(f'fetchReviews/dealer/{dealer_id}')

    if reviews is None:
        return JsonResponse({
            'status': 500,
            'reviews': []
        }, status=500)

    return JsonResponse({
        'status': 200,
        'reviews': reviews
    })


