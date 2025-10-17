from django.urls import path
from .views import EspeceListView, EspeceCreateView, EspeceUpdateView, EspeceDeleteView, EspeceListJsonView

app_name = "especes"
urlpatterns = [
    path('', EspeceListView.as_view(), name='espece-list'),
    path('create/', EspeceCreateView.as_view(), name='espece-create'),
    path('<uuid:pk>/update/', EspeceUpdateView.as_view(), name='espece-update'),
    path('<uuid:pk>/delete/', EspeceDeleteView.as_view(), name='espece-delete'),
    path('list/json/', EspeceListJsonView.as_view(), name='espece-list-json'),
]
