from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, UserViewSet
from apps.users.views import CustomLoginView, CustomLogoutView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('api/', include(router.urls)),
]
