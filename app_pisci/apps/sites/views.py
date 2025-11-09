from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Site, Bassin
from apps.activite_quotidien.models import Nourrissage
from apps.commun.view import StandardDeleteMixin
from django.urls import reverse_lazy
from .forms import SiteForm, BassinForm
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from typing import Any
from django.utils import timezone
from apps.stocks.models import LotDePoisson
from django.db.models import Q

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
        sites = Site.objects.prefetch_related('bassins__lots_poissons__espece').filter(est_actif=True)
        data = []

        today = timezone.now().date()

        for site in sites:
            bassins = []

            for bassin in site.bassins.filter(est_actif=True):
                lot = bassin.lots_poissons.first()
                lot_data = None
                nourrissages_today = 0
                a_jeun = False

                if lot:
                    # Compter les repas d'aujourd'hui
                    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
                    nourrissages_today = Nourrissage.objects.filter(
                        bassin=bassin,
                        date_repas__gte=today_start,
                        date_repas__lte=today_end
                    ).count()

                    # Vérifier le dernier repas à jeun
                    dernier_ajeun = Nourrissage.objects.filter(
                        bassin=bassin
                    ).filter(
                        Q(motif_absence__icontains='ajeun') | Q(qte=0)
                    ).order_by('-date_repas').first()

                    dernier_nourrissage_data = None
                    motif_absence = None

                    if dernier_ajeun:
                        if dernier_ajeun.qte == 0 or (dernier_ajeun.motif_absence and dernier_ajeun.motif_absence.lower() == 'ajeun'):
                            a_jeun = True
                            motif_absence = dernier_ajeun.motif_absence
                            dernier_nourrissage_data = {
                                'motif_absence': dernier_ajeun.motif_absence,
                                'qte': dernier_ajeun.qte,
                                'date_repas': dernier_ajeun.date_repas.isoformat(),
                            }

                    # Préparer lot_data
                    lot_data = {
                        'code': lot.code_lot,
                        'espece': lot.espece.nom_commun,
                        'quantite_actuelle': lot.quantite_actuelle,
                        'poids_moyen': lot.poids_moyen,
                        'poids': lot.poids,
                        'statut': lot.get_statut_display(),
                        'date_arrivee': lot.date_arrivee.strftime('%d/%m/%Y'),
                        'dernier_nourrissage': dernier_nourrissage_data,
                        'nourrissages_today': nourrissages_today,
                        'motif_absence': motif_absence,
                        'a_jeun': a_jeun,
                    }

                bassins.append({
                    'id': str(bassin.id),
                    'nom': bassin.nom,
                    'type': bassin.type,
                    'a_un_lot': bool(lot),
                    'lot': lot_data,
                })

            data.append({
                'id': str(site.id),
                'nom': site.nom,
                'bassins': bassins,
            })

        return JsonResponse(data, safe=False)


class CarteBassinsView(LoginRequiredMixin, TemplateView):
    template_name = 'sites/carte.html'  # Chemin vers ton template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(require_GET, name='dispatch')
class BassinLotDetailsView(LoginRequiredMixin, View):

    def get(self, request, bassin_id, *args, **kwargs):
        bassin = Bassin.objects.get(id=bassin_id)
        lot = bassin.lots_poissons.first()  # type: ignore
        repas = Nourrissage.objects.filter(bassin=bassin).order_by('-date_repas')[:7]

        data = {
            "bassin_nom": bassin.nom,
            "site_nom": bassin.site.nom,
            "site_id": str(bassin.site.id),
            "code_lot": lot.code_lot if lot else None,
            "espece": lot.espece.nom_commun if lot and lot.espece else None,
            "quantite_actuelle": lot.quantite_actuelle if lot else 0,
            "poids_moyen": lot.poids_moyen if lot else None,
            "poids_total": lot.poids if lot else None,
            "date_arrivee": lot.date_arrivee.strftime("%d/%m/%Y") if lot and lot.date_arrivee else None,
            "derniers_repas": [
                {
                    "date": repas.date_repas.strftime("%d/%m/%Y %H:%M"),
                    "type_aliment": repas.aliment.nom if repas.aliment else "Non spécifié", # type: ignore
                    "quantite": repas.qte,
                }
                for repas in repas
            ] if repas else [],
        }
        return JsonResponse(data)
