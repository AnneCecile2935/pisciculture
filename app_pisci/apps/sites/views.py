from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Site, Bassin
from apps.commun.view import StandardDeleteMixin
from django.urls import reverse_lazy
from .forms import SiteForm, BassinForm
from django.urls import reverse
from django.http import JsonResponse
from typing import Any

class SiteListView(LoginRequiredMixin, ListView):
    model = Site
    template_name = "sites/site_list.html"
    context_object_name = "sites"


class SiteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = SiteForm
    model = Site
    template_name = "sites/site_form.html"
    success_url = reverse_lazy("sites:site-list")
    permission_required = "sites.add_site"

class SiteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Site
    template_name = "sites/site_form.html"
    fields = ["nom", "est_actif"]
    success_url = reverse_lazy("sites:site-list")
    permission_required = "sites.change_site"

class SiteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, StandardDeleteMixin, DeleteView):
    model = Site
    fields = ["nom", "est_actif"]
    list_url_name = "sites:site-list"
    permission_required = "sites.delete_site"

class SiteListJsonView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        sites = list(Site.objects.all().values('id', 'nom', 'est_actif'))
        return JsonResponse(sites, safe=False)

class BassinListView(LoginRequiredMixin, ListView):
    model = Bassin
    template_name = "sites/bassin_list.html"
    context_object_name = "bassins"


    def get_queryset(self):
        self.site = Site.objects.get(pk=self.kwargs.get("site_id"))
        return Bassin.objects.filter(site_id=self.kwargs.get("site_id"), est_actif=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = self.site
        return context

class BassinCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = BassinForm
    model = Bassin
    template_name = "sites/bassin_form.html"
    permission_required = "sites.add_bassin"

    def form_valid(self, form):
        form.instance.site_id = self.kwargs['site_id']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupère le site_id depuis les arguments de l'URL
        context['site_id'] = self.kwargs.get('site_id')
        return context

    def get_success_url(self):
        return reverse('sites:bassin-list', kwargs={'site_id': self.kwargs.get('site_id')})

class BassinUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = BassinForm
    model = Bassin
    template_name = "sites/bassin_form.html"
    permission_required = "sites.change_bassin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_id'] = self.object.site.id
        return context

    def get_success_url(self):
        return reverse('sites:bassin-list', args=[self.object.site.id]) # type: ignore

class BassinDeleteView(LoginRequiredMixin, PermissionRequiredMixin, StandardDeleteMixin, DeleteView):
    model = Bassin
    fields = ["nom", "est_actif"]
    permission_required = "sites.delete_bassin"
    list_url_name = 'sites:site-list'

class BassinListJsonView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        site_id = self.kwargs.get("site_id")
        bassins = list(Bassin.objects.filter(site_id=site_id, est_actif=True).values('id', 'nom', 'est_actif'))
        return JsonResponse(bassins, safe=False)

class BassinsAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Récupère tous les sites avec leurs bassins et lots associés
        sites = Site.objects.prefetch_related(
            'bassins__lots_poissons__espece'
        ).filter(est_actif=True)

        data = []
        for site in sites:
            bassins = []
            for bassin in site.bassins.filter(est_actif=True):
                lot = bassin.lots_poissons.first()  # Un seul lot par bassin (grâce à ta validation)

                bassins.append({
                    'nom': bassin.nom,
                    'type': bassin.type,
                    'volume': bassin.volume,
                    'a_un_lot': bool(lot),
                    'lot': {
                        'code': lot.code_lot if lot else None,
                        'espece': lot.espece.nom_commun if lot else None,
                        'quantite': lot.quantite_actuelle if lot else 0,
                        'poids_moyen': lot.poids_moyen if lot else None,
                        'statut': lot.get_statut_display() if lot else None,
                        'date_arrivee': lot.date_arrivee.strftime('%d/%m/%Y') if lot else None,
                        'dernier_nourrissage': '30/10/2025' if lot else None,  # À remplacer par tes données
                    } if lot else None
                })
            data.append({
                'nom': site.nom,
                'bassins': bassins,
            })
        return JsonResponse(data, safe=False)

class CarteBassinsView(LoginRequiredMixin, TemplateView):
    template_name = 'sites/carte.html'  # Chemin vers ton template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tu peux ajouter des données supplémentaires au contexte ici si besoin
        # Exemple : context['titre'] = "Ma Carte des Bassins"
        return context
