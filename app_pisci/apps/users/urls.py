from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('', include(router.urls)),
]
