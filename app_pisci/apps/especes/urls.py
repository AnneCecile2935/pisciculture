from django.urls import path
from .views import EspeceListView, EspeceCreateView, EspeceUpdateView, EspeceDeleteView

app_name = "especes"
urlpatterns = [
    path('', EspeceListView.as_view(), name='espece-list'),
    path('create/', EspeceCreateView.as_view(), name='espece-create'),
    path('<int:pk>/update/', EspeceUpdateView.as_view(), name='espece-update'),
    path('<int:pk>/delete/', EspeceDeleteView.as_view(), name='espece-delete'),
]
