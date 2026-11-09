from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
import logging
import json
from django.views.decorators.csrf import csrf_exempt

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
