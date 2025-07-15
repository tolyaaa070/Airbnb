from django.urls import path , include
from .views import *
from rest_framework import routers
from .views import (UserProfile, LogoutView, CustomLoginView, RegisterView,BookingCreateViewSet,
                    BookingListViewSet,ReviewsListApiViewSet,ReviewEditApiViewSet,
                    ReviewsCreateApiViewSet,PropertyCreateViewSet,PropertyUpdateAPIViewSet,PropertyDetailViewSet)

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('property/', PropertyListAPIViewSet.as_view(), name='property'),
    path('property/<int:pk>/', PropertyDetailViewSet.as_view(), name='property_detail'),
    path('property/create', PropertyCreateViewSet.as_view(), name='property_create'),
    path('property/<int:pk>/edit', PropertyUpdateAPIViewSet.as_view(), name='property_edit'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('booking/', BookingListViewSet.as_view(), name='booking'),
    path('booking/create', BookingCreateViewSet.as_view(), name='booking_create'),
    path('review/', ReviewsListApiViewSet.as_view(), name='review'),
    path('review/create', ReviewsCreateApiViewSet.as_view(), name='review_create'),
    path('review/<int:pk>/edit', ReviewEditApiViewSet.as_view(), name='review_edit'),

]

