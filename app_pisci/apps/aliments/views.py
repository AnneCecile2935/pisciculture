from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from apps.commun.view import StandardDeleteMixin
from django.urls import reverse_lazy
from .models import Aliment
from .forms import AlimentForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse


class AlimentListView(LoginRequiredMixin, ListView):
    model = Aliment
    template_name = "aliments/alim_list.html"
    context_object_name = "aliments"
    login_url = '/login/'

class AlimentCreateView(LoginRequiredMixin, CreateView):
    model = Aliment
    form_class = AlimentForm
    template_name = "aliments/alim_form.html"
    success_url = reverse_lazy("aliments:list")
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "Accès réservé aux administrateurs.")
        return redirect("aliments:list")

    def form_valid(self, form):
        messages.success(self.request, "L'aliment a été créé avec succès")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("FORM ERRORS:", form.errors)
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        print("USER:", request.user)
        print("STAFF:", request.user.is_staff)
        return super().dispatch(request, *args, **kwargs)


class AlimentUpdateView(LoginRequiredMixin, UpdateView):
    model = Aliment
    form_class = AlimentForm
    template_name = "aliments/alim_form.html"
    success_url = reverse_lazy("aliments:list")
    login_url = '/login/'

    def form_valid(self, form):
        messages.success(self.request, "L'aliment a été mis à jour avec succès")
        return super().form_valid(form)

class AlimentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Aliment
    template_name = "confirm_delete.html"
    list_url_name= "aliments:list"
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "Accès réservé aux administrateurs.")
        return redirect("aliments:list")

    def get_success_url(self):
        return reverse_lazy("aliments:list")

class AlimentListJsonView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        aliments = Aliment.objects.all().values(
            "id",
            "code_alim",
            "nom",
            "fournisseur__nom"
        )
        return JsonResponse(list(aliments), safe=False)
