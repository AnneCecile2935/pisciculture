from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import LotDePoisson
from .forms import LotForm
from django.contrib import messages

class LotListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = LotDePoisson
    template_name = "lots/lot_list.html"
    context_object_name = "lots"
    permission_required = "stocks.pisiculture_view_lot"
    raise_exception = True

class LotCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = LotDePoisson
    form_class = LotForm
    template_name = "lots/lot_form.html"
    success_url = reverse_lazy("lots:list")
    permission_required = "stocks.pisciculture_add_lot"
    raise_exception = True

    def form_valide(self, form):
        messages.success(self.request, "Le lot a été créé avec succès")
        return super().form_valid(form)

class LotUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = LotDePoisson
    form_class = LotForm
    template_name = "lots/lot_form.html"
    success_url = reverse_lazy("lots:list")
    permission_required = "stocks.pisciculture_change_lot"
    raise_exception = True

    def form_valid(self, form):
        messages.success(self.request, "Le lot a été mis à jour avec succès")
        return super().form_valid(form)

class LotDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = LotDePoisson
    template_name = "lots/lot_confirm_delete.html"
    success_url = reverse_lazy("lots:list")
    permission_required = "stocks.pisciculture_delete_lot"
    raise_exception = True

    def delete(self, request, *args, **kwargs):
        lot = self.get_object()
        messages.success(self.request, "Le lot {code_lot} a été supprimé avec succès")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Supprimer le lot {self.object.code_lot}"
        return context
