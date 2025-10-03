from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Fournisseurs
from django.urls import reverse_lazy
from .forms import FournisseurForm

class FournisseurListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Fournisseurs
    template_name = "fournisseurs/frs_list.html"
    context_object_name = "fournisseurs"
    permission_required = "fournisseurs.view_fournisseur"

class FournisseurCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = FournisseurForm
    model = Fournisseurs
    template_name = "fournisseurs/frs_form.html"
    success_url = reverse_lazy("fournisseurs:fournisseur-list")
    permission_required = "fournisseurs.add_fournisseur"

    def form_valid(self, form):
        return super().form_valid(form)


class FournisseurUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Fournisseurs
    form_class = FournisseurForm
    template_name = "fournisseurs/frs_form.html"
    success_url = reverse_lazy("fournisseurs:fournisseur-list")
    permission_required = "fournisseurs.change_fournisseur"

class FournisseurDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Fournisseurs
    template_name = "fournisseurs/frs_confirm_delete.html"
    success_url = reverse_lazy("fournisseurs:fournisseur-list")
    permission_required = "fournisseurs.delete_fournisseur"
