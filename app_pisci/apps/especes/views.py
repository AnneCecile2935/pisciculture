from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Espece
from .forms import EspeceForm
from django.http import JsonResponse
from django.contrib import messages

class EspeceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Espece
    template_name = "especes/esp_list.html"
    context_object_name = "especes"
    permission_required = "especes.view_espece"

    def form_valid(self, form):
        messages.success(self.request, "L'espèce a été ajoutée avec succès !")
        return super().form_valid(form)

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
        messages.success(self.request, "L'espèce a été mise à jour avec succès !")
        return super().form_valid(form)

class EspeceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Espece
    template_name = "especes/esp_confirm_delete.html"
    success_url = reverse_lazy("especes:espece-list")
    permission_required = "especes.delete_espece"
    context_object_name = "espece"

    def form_valid(self, form):
        messages.success(self.request, "L'espèce a été supprimée avec succès !")
        return super().form_valid(form)

class EspeceListJsonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "especes.view_espece"

    def get(self, request, *args, **kwargs):
        especes = Espece.objects.all().values(
            'id', 'nom_commun', 'nom_scientifique', 'est_actif'
        )
        return JsonResponse(list(especes), safe=False)
