from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import LotDePoisson
from .forms import LotForm

class LotListView(LoginRequiredMixin, ListView):
    model = LotDePoisson
    template_name = "stocks/lotdepoisson_list.html"
    context_object_name = "lots"

class LotCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = LotDePoisson
    form_class = LotForm
    template_name = "stocks/lot_form.html"
    success_url = reverse_lazy("stocks:list")

    def test_func(self):
        return self.request.user.is_admin  # Seuls les admins peuvent créer

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas les droits pour effectuer cette action.")
        return super().handle_no_permission()

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Le lot a été créé avec succès")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class LotUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LotDePoisson
    form_class = LotForm
    template_name = "stocks/lot_form.html"
    success_url = reverse_lazy("stocks:list")

    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas les droits pour effectuer cette action.")
        return super().handle_no_permission()


    def form_valid(self, form):
        messages.success(self.request, "Le lot a été mis à jour avec succès")
        return super().form_valid(form)

class LotDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LotDePoisson
    template_name = "stocks/lot_confirm_delete.html"
    success_url = reverse_lazy("stocks:list")

    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas les droits pour effectuer cette action.")
        return super().handle_no_permission()


    def form_valid(self, form):
        # Déplace ta logique personnalisée ici
        messages.success(self.request, "Le lot a été supprimé avec succès.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Supprimer le lot {self.object.code_lot}"
        return context
