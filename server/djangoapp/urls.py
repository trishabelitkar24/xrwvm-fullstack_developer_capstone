
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Authentication
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),

    # Cars
    path('get_cars', views.get_cars, name='get_cars'),

    # Dealers
    path('get_dealers', views.get_dealers, name='get_dealers'),
    path(
        'get_dealers/<str:state>',
        views.get_dealers,
        name='get_dealers_by_state'
    ),
    path(
        'dealer/<int:dealer_id>',
        views.get_dealer,
        name='get_dealer'
    ),

    # Reviews
    path('add_review', views.add_review, name='add_review'),
    path(
    'reviews/dealer/<int:dealer_id>',
    views.get_reviews,
    name='get_reviews'
),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
