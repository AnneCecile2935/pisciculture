from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, UserViewSet
from apps.users.views import UserUpdateView, UserListView
from .views import user_list_json

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
     # URLs pour les templates (vues classiques)
    path('signup/', SignupView.as_view(), name='signup'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('', UserListView.as_view(), name='user_list'),

    path('api/list/json/', user_list_json, name='list_json'),

    # URLs pour l'API (DRF)
    path('api/drf/', include(router.urls)),

]
