from django.urls import path
from .views import AlimentListView, AlimentCreateView, AlimentUpdateView

urlpatterns = [
    path('', AlimentListView.as_view(), name='aliment_list'),
    path('ajouter/', AlimentCreateView.as_view(), name='aliment_add'),
    path('<int:pk>/modifier/', AlimentUpdateView.as_view, name='aliment_edit'),
]
