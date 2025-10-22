from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Fournisseur
from apps.commun.view import StandardDeleteMixin
from django.urls import reverse_lazy
from .forms import FournisseurForm
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied


class FournisseurListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Fournisseur
    template_name = "fournisseurs/frs_list.html"
    context_object_name = "fournisseurs"
    permission_required = "fournisseurs.view_fournisseur"

class FournisseurCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = FournisseurForm
    model = Fournisseur
    template_name = "fournisseurs/frs_form.html"
    success_url = reverse_lazy("fournisseurs:fournisseur-list")
    permission_required = "fournisseurs.add_fournisseur"

    def form_valid(self, form):
        messages.success(self.request, "Le fournisseur a été ajouté avec succès !")
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Vérifie que l'utilisateur a la permission d'ajouter un fournisseur
        if not request.user.has_perm('fournisseurs.add_fournisseur'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class FournisseurUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = "fournisseurs/frs_form.html"
    success_url = reverse_lazy("fournisseurs:fournisseur-list")
    permission_required = "fournisseurs.change_fournisseur"

    def form_valid(self, form):
        messages.success(self.request, "Le fournisseur a été mis à jour avec succès !")
        return super().form_valid(form)

class FournisseurDeleteView(LoginRequiredMixin, PermissionRequiredMixin, StandardDeleteMixin, DeleteView):
    model = Fournisseur
    list_url_name = "fournisseurs:fournisseur-list"
    permission_required = "fournisseurs.delete_fournisseur"
    contextçobject_name = "fournisseur"

class FournisseurListJsonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "fournisseurs.view_fournisseur"

    def get(self, request, *args, **kwargs):
        fournisseurs = list(Fournisseur.objects.values(
            'id', 'nom', 'type_fournisseur', 'ville', 'contact', 'est_actif'
        ))
        return JsonResponse(fournisseurs, safe=False)
