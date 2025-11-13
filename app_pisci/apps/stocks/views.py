from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.commun.view import StandardDeleteMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import LotDePoisson
from .forms import LotForm
from django.http import JsonResponse

class LotListView(LoginRequiredMixin, ListView):
    model = LotDePoisson
    template_name = "stocks/lotdepoisson_list.html"
    context_object_name = "lots"

class LotCreateView(LoginRequiredMixin, CreateView):
    model = LotDePoisson
    form_class = LotForm
    template_name = "stocks/lot_form.html"
    success_url = reverse_lazy("stocks:list")

    def form_valid(self, form):
        response = super().form_valid(form)  # Appelle form.save() qui appelle save() du modèle
        messages.success(self.request, "Le lot a été créé avec succès")
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)

class LotUpdateView(LoginRequiredMixin, UpdateView):
    model = LotDePoisson
    form_class = LotForm
    template_name = "stocks/lot_form.html"
    success_url = reverse_lazy("stocks:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Le lot a été mis à jour avec succès")
        return response

class LotDeleteView(LoginRequiredMixin, UserPassesTestMixin, StandardDeleteMixin, DeleteView):
    model = LotDePoisson
    list_url_name= "stocks:list"

    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas les droits pour effectuer cette action.")
        return super().handle_no_permission()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Supprimer le lot {self.object.code_lot}"
        return context


class LotListJsonView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        lots = list(LotDePoisson.objects.all().order_by('-date_arrivee').values(
            'id', 'code_lot', 'espece__nom_commun', 'site_prod__nom',
            'statut', 'quantite', 'quantite_actuelle', 'poids', 'poids_moyen', 'date_arrivee'
        ))
        # Ajoutez les noms des bassins manuellement
        for lot in lots:
            lot_id = lot['id']
            lot_obj = LotDePoisson.objects.get(id=lot_id)
            lot['bassins'] = [bassin.nom for bassin in lot_obj.bassins.all()]
            if lot_obj.quantite_actuelle > 0:
                lot['poids_moyen'] = round((lot_obj.poids * 1000) / lot_obj.quantite_actuelle, 2)
            else:
                lot['poids_moyen'] = None
        return JsonResponse(lots, safe=False)
