from django.urls import path
from .views import LotCreateView, LotDeleteView, LotUpdateView, LotListView

app_name = 'stocks'
urlpatterns = [
    path('', LotListView.as_view(), name='lot-list'),
    path('create/', LotCreateView.as_view(), name='lot-create'),
    path('<int:pk>/update/', LotUpdateView.as_view(), name='lot-update'),
    path('<int:pk/delete/', LotDeleteView.as_view(), name='lot-delete'),
]

