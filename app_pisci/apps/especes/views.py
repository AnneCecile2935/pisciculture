from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Espece
from .forms import EspeceForm

class EspeceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Espece
    template_name = "especes/esp_list.html"
    context_object_name = "especes"
    permission_required = "especes.view_espece"

class EspeceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Espece
    form_class = EspeceForm
    template_name = "especes/esp_form.html"
    success_url = reverse_lazy("especes:espece-list")  
    permission_required = "especes.add_espece"

    def form_valid(self, form):
        return super().form_valid(form)

class EspeceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Espece
    form_class = EspeceForm
    template_name = "especes/esp_form.html"
    success_url = reverse_lazy("especes:espece-list")
    permission_required = "especes.change_espece"
    context_object_name = "espece"

    def form_valid(self, form):
        return super().form_valid(form)

class EspeceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Espece
    template_name = "especes/esp_confirm_delete.html"
    success_url = reverse_lazy("especes:espece-list")
    permission_required = "especes.delete_espece"
    context_object_name = "espece"
