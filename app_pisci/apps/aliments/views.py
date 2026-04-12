from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

class AlimentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Aliment
    form_class = AlimentForm
    template_name = "aliments/alim_form.html"
    success_url = reverse_lazy("aliments:list")
    permission_required = "aliments.add_aliment"
    login_url = '/login/'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(f'{self.login_url}?next={self.request.path}')
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, "L'aliment a été créé avec succès")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("FORM ERRORS:", form.errors)
        return super().form_invalid(form)


class AlimentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Aliment
    form_class = AlimentForm
    template_name = "aliments/alim_form.html"
    success_url = reverse_lazy("aliments:list")
    permission_required = "aliments.change_aliment"
    login_url = '/login/'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(f'{self.login_url}?next={self.request.path}')
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, "L'aliment a été mis à jour avec succès")
        return super().form_valid(form)

class AlimentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, StandardDeleteMixin, DeleteView):
    model = Aliment
    list_url_name= "aliments:list"
    login_url = '/login/'
    permission_required = "aliments.delete_aliment"

    def test_func(self):
        has_perm = self.request.user.has_perm('aliments.delete_aliment')
        print(f"User has permission: {has_perm}, is_staff: {self.request.user.is_staff}")
        return has_perm and self.request.user.is_staff  # ⭐ Vérifie aussi is_staff


class AlimentListJsonView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        aliments = Aliment.objects.all().values(
            "id",
            "code_alim",
            "nom",
            "fournisseur__nom"
        )
        return JsonResponse(list(aliments), safe=False)
