from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Fournisseurs
from .forms import FournisseurForm

class FournisseurListView(ListView):
    model = Fournisseurs
    template_name = 'fournisseurs/fournisseur_list.html'
    context_object_name = 'fournisseurs'

class FournisseurCreateView(CreateView):
    model = Fournisseurs
    form_class = FournisseurForm
    template_name = 'fournisseurs/fournisseur_form.html'
    success_url = reverse_lazy('fournisseur_list')

class FournisseurUpdateView(UpdateView):
    model = Fournisseurs
    form_class = FournisseurForm
    template_name= 'fournisseurs/fournisseur_form.html'
    success_url = reverse_lazy('founisseur_list')
