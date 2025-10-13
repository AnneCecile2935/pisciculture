from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Aliment
from .forms import AlimentForm
from django.contrib import messages
from django.shortcuts import redirect


class AlimentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Aliment
    template_name = "aliments/alim_list.html"
    context_object_name = "aliments"
    permission_required = "aliments.view_aliment"
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

class AlimentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Aliment
    template_name = "aliments/alim_confirm_delete.html"
    success_url = reverse_lazy("aliments:list")
    permission_required = "aliments.delete_aliment"
    login_url = '/login/'

    def get_success_url(self):
        messages.success(self.request, f"L'aliment a été supprimé avec succès")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Supprimer l'aliment {self.object.code_alim}"
        return context
