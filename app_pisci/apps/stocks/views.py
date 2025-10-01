from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Aliment
from .forms import AlimentForms

class AlimentListView(ListView):
    model = Aliment
    template_name = 'stocks/aliment_list.html'
    context_object_name = 'aliments'

class AlimentCreateView(CreateView):
    model = Aliment
    form_class = AlimentForms
    template_name = 'stocks/aliment_form.html'
    success_url = reverse_lazy('aliment_list')

    def form_valid(self, form):
        return super().form_valid(form)

class AlimentUpdateView(UpdateView):
    model = Aliment
    form_class = AlimentForms
    template_name = 'stocks/aliment_form.html'
    success_url = reverse_lazy('aliment_list')
