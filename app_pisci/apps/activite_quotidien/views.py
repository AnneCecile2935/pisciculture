from django.shortcuts import render, redirect, get_object_or_404  # Utilisé pour les vues, redirections, et récupération d'objets
from django.http import HttpResponse, JsonResponse  # Utilisé pour les réponses HTTP et JSON
from django.db.models import Case, When, Value, CharField  # Utilisé dans NourrissageListJsonView pour les annotations
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, View, FormView, TemplateView  # Utilisé pour toutes les vues basées sur des classes
from django.urls import reverse_lazy  # Utilisé pour les URLs de redirection
from django.contrib.auth.mixins import LoginRequiredMixin  # Utilisé pour sécuriser les vues
from django.contrib import messages  # Utilisé pour les messages flash (succès/erreur)
from django.utils import timezone  # Utilisé pour gérer les dates/heures

# Modèles
from apps.sites.models import Site, Bassin  # Utilisés partout pour les sites et bassins
from apps.activite_quotidien.models import ReleveTempOxy, Nourrissage  # Modèles principaux
from apps.stocks.models import LotDePoisson  # Utilisé pour les lots de poissons
from apps.aliments.models import Aliment  # Utilisé pour les aliments

# Formulaires
from apps.activite_quotidien.forms import ReleveTempOxyForm, NourrissageForm, NourrissageFormSet  # Formulaires utilisés

# Mixins personnalisés
from apps.commun.view import StandardDeleteMixin  # Utilisé pour la suppression

# Librairies Python
from datetime import timedelta  # Utilisé pour les plages de dates dans les graphiques
import hashlib  # Utilisé pour générer des couleurs uniques dans les graphiques



class NourrissageCreateView(LoginRequiredMixin, CreateView):
    """
    Vue classique de création d’un nourrissage.
    """

    model = Nourrissage
    form_class = NourrissageForm
    template_name = "activite_quotidien/nourrissage_form.html"
    success_url = reverse_lazy("activite_quotidien:nourrissage-list")

    def get_form_kwargs(self):
        """
        Injection de paramètres dynamiques dans le form :

        - bassin sélectionné côté frontend
        - site sélectionné côté frontend
        """

        kwargs = super().get_form_kwargs()
        kwargs["bassin_id"] = self.request.POST.get("bassin")
        kwargs["site_id"] = self.request.POST.get("site_prod")
        return kwargs

    def form_valid(self, form):
        """
        Sauvegarde du nourrissage + enrichissement métier
        """

        form.instance.cree_par = self.request.user

        nourrissage = form.save(commit=False)

        # logique métier liée au lot de poissons
        lot = form.cleaned_data.get("crea_lot")
        if lot:
            lot.dernier_nourrissage = timezone.now()
            lot.save(update_fields=["dernier_nourrissage"])

        messages.success(self.request, "Le repas a été enregistré avec succès !")
        return super().form_valid(form)

class NourrissageListView(LoginRequiredMixin, ListView):
    """
    Vue pour lister tous les repas (nourrissages).
    Trie les repas par date décroissante et pagine les résultats.
    """
    model = Nourrissage
    template_name = 'activite_quotidien/nourrissage_list.html'
    context_object_name = 'nourrissages'
    paginate_by = 20

    def get_queryset(self):
        """
        Retourne la liste des repas triés par date décroissante.
        """
        return super().get_queryset().order_by('-date_repas')

class NourrissageDetailView(LoginRequiredMixin, DetailView):
    """
    Vue pour afficher les détails d'un repas.
    """
    model = Nourrissage
    template_name = 'activite_quotidien/nourrissage_detail.html'
    context_object_name = 'nourrissage'

class NourrissageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Mise à jour d’un nourrissage existant.
    Même logique que create.
    """

    model = Nourrissage
    form_class = NourrissageForm
    template_name = "activite_quotidien/nourrissage_form.html"
    success_url = reverse_lazy("activite_quotidien:nourrissage-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        # bassin figé sur l’objet existant
        kwargs["bassin_id"] = self.object.bassin_id

        # site possible en POST (si changement UI)
        kwargs["site_id"] = self.request.POST.get("site_prod")

        return kwargs

    def form_valid(self, form):
        form.instance.cree_par = self.request.user

        nourrissage = form.save(commit=False)

        lot = form.cleaned_data.get("crea_lot")
        if lot:
            lot.dernier_nourrissage = timezone.now()
            lot.save(update_fields=["dernier_nourrissage"])

        messages.success(self.request, "Le repas a été mis à jour avec succès !")
        return super().form_valid(form)

class NourrissageDeleteView(LoginRequiredMixin,StandardDeleteMixin, DeleteView):
    """
    Vue pour supprimer un repas.
    Utilise StandardDeleteMixin pour standardiser le comportement de suppression.
    """
    model = Nourrissage
    list_url_name='activite_quotidien:nourrissage-list'


class NourrissageListJsonView(LoginRequiredMixin, View):
    """
    API JSON des nourrissages.

    Sert à :
    - dashboard
    - frontend dynamique
    - reporting
    """

    def get(self, request, *args, **kwargs):
        nourrissages = Nourrissage.objects.select_related(
            'site_prod', 'bassin', 'crea_lot', 'aliment', 'cree_par'
        ).annotate(
            # transformation du code motif -> label humain
            motif_nom=Case(
                *[
                    When(motif_absence=m[0], then=Value(m[1]))
                    for m in Nourrissage.MOTIFS_ABSENCE
                ],
                default=Value(None),
                output_field=CharField()
            )
        ).values(
            'id',
            'site_prod__nom',
            'bassin__nom',
            'crea_lot__code_lot',
            'qte',
            'date_repas',
            'aliment__nom',
            'cree_par__username',
            'notes',
            'motif_absence',
            'motif_nom',
            'crea_lot__dernier_nourrissage'
        ).order_by('-date_repas')

        return JsonResponse(list(nourrissages), safe=False)

import json

class NourrissageParSiteView(LoginRequiredMixin, FormView):
    """
    Vue critique métier :

    Permet de saisir les nourrissages de TOUS les bassins d’un site en une seule fois.
    """

    template_name = "activite_quotidien/nourrissage_par_site_form.html"
    form_class = NourrissageFormSet
    success_url = reverse_lazy("activite_quotidien:nourrissage-list")

    def get_form_kwargs(self):
        """
        Préremplissage des bassins + dernier aliment connu
        """

        kwargs = super().get_form_kwargs()

        site = get_object_or_404(Site, id=self.kwargs["site_id"])
        bassins = Bassin.objects.filter(site=site)

        initial = []

        for bassin in bassins:
            last = (
                Nourrissage.objects
                .filter(bassin=bassin, aliment__isnull=False)
                .order_by("-date_repas")
                .first()
            )

            initial.append({
                "bassin": bassin,
                "aliment": last.aliment if last else None
            })

        kwargs["initial"] = initial
        return kwargs

    def form_valid(self, formset):
        """
        Transformation du FormSet en bulk_create.

        ⚠️ point critique performance + cohérence métier
        """

        site = get_object_or_404(Site, id=self.kwargs["site_id"])
        objects = []

        date_repas = self.request.POST.get("date_repas") or timezone.now().date()

        for form in formset:
            if not form.cleaned_data:
                continue

            bassin = form.cleaned_data["bassin"]
            aliment = form.cleaned_data.get("aliment")
            qte = form.cleaned_data.get("qte")
            motif = form.cleaned_data.get("motif_absence")

            # récupération du lot actif du bassin
            lot = bassin.lots_poissons.first()

            objects.append(
                Nourrissage(
                    site_prod=site,
                    bassin=bassin,
                    crea_lot=lot,

                    # règle métier : motif annule aliment
                    aliment=aliment if not motif else None,

                    # sécurité : jamais None en base
                    qte=qte if qte is not None else 0,

                    motif_absence=motif if motif else None,
                    date_repas=date_repas,
                    cree_par=self.request.user,
                )
            )

        Nourrissage.objects.bulk_create(objects)

        messages.success(self.request, f"{len(objects)} repas enregistrés")

        return super().form_valid(formset)



class ChoixSiteEnregistrementRepasView(LoginRequiredMixin, TemplateView):
    """
    Vue pour permettre à l'utilisateur de choisir un site avant de saisir les repas.
    """
    template_name = 'activite_quotidien/choix_site_enregistrement_repas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites'] = Site.objects.all()
        return context

class ListRelevesView(LoginRequiredMixin, ListView):
    """
    Vue pour lister les relevés de température, oxygène et débit.
    Filtre les relevés par site si un site est spécifié dans la requête GET.
    """
    model = ReleveTempOxy
    template_name = 'activite_quotidien/releve_list.html'
    context_object_name = 'releves'

    def get_queryset(self):
        """
        Retourne les relevés du jour, filtrables par site.
        """
        today = timezone.now().date()
        site_id = self.request.GET.get('site')
        releves = ReleveTempOxy.objects.filter(date_releve=today).order_by('site__nom', 'moment_jour')
        if site_id:
            releves = releves.filter(site_id=site_id)
        return releves

    def get_context_data(self, **kwargs):
        """
        Ajoute la liste des sites et la date du jour au contexte du template.
        """
        context = super().get_context_data(**kwargs)
        context['sites'] = Site.objects.all()
        context['today'] = timezone.now().date()
        return context

class CreateReleveView(LoginRequiredMixin, CreateView):
    """
    Vue pour créer un nouveau relevé.
    """
    model = ReleveTempOxy
    form_class = ReleveTempOxyForm
    template_name = 'activite_quotidien/releve_form.html'
    success_url = reverse_lazy('activite_quotidien:releve-list')

    def get_initial(self):
        """
        Initialise le formulaire avec la date du jour par défaut.
        """
        initial = super().get_initial()
        initial['date_releve'] = timezone.now().date()
        return initial


class UpdateReleveView(LoginRequiredMixin, UpdateView):
    """
    Vue pour mettre à jour un relevé existant.
    """
    model = ReleveTempOxy
    form_class = ReleveTempOxyForm
    template_name = 'activite_quotidien/releve_form.html'
    success_url = reverse_lazy('activite_quotidien:releve-list')

class DeleteReleveView(LoginRequiredMixin, DeleteView):
    """
    Vue pour supprimer un relevé.
    """
    model = ReleveTempOxy
    template_name = 'activite_quotidien/releve_delete.html'
    success_url = reverse_lazy('activite_quotidien:releve-list')

class RelevesListJsonView(LoginRequiredMixin, View):
    """
    Vue pour retourner la liste des relevés au format JSON.
    Filtre les relevés par site et/ou date si spécifiés dans la requête GET.
    """
    def get(self, request, *args, **kwargs):
        site_id = request.GET.get('site')
        date_releve = request.GET.get('date')  # Optionnel : filtre par date si fourni
        releves = ReleveTempOxy.objects.all().order_by('-date_releve', 'site__nom', 'moment_jour')
        if site_id:
            releves = releves.filter(site_id=site_id)
        if date_releve:
            releves = releves.filter(date_releve__date=date_releve)
        data = [
            {
                'id': str(releve.id),
                'site': releve.site.nom,
                'temperature': float(releve.temperature) if releve.temperature else None,
                'oxygene': float(releve.oxygene) if releve.oxygene else None,
                'debit': float(releve.debit) if releve.debit else None,
                'moment_jour': releve.get_moment_jour_display(),
                'date_releve': releve.date_releve.strftime("%Y-%m-%d %H:%M:%S") if releve.date_releve else None
            }
            for releve in releves
        ]
        return JsonResponse(data, safe=False)

class TempChartDataView(LoginRequiredMixin, View):
    """
    Vue pour retourner les données de température au format JSON, pour alimenter un graphique.
    Retourne les températures des 21 derniers jours pour chaque site.
    """
    def get(self, request, *args, **kwargs):
        start_date = timezone.now().date() - timedelta(days=21)
        releves = ReleveTempOxy.objects.filter(
            date_releve__gte=start_date,
            temperature__isnull=False
        ).select_related('site').order_by('site__nom', 'date_releve')

        all_dates = sorted(set(releve.date_releve for releve in releves))
        labels = [date.strftime("%Y-%m-%d") for date in all_dates]
        sites = set(releve.site for releve in releves)

        datasets = []
        for site in sites:
            # Génère une couleur à partir de l'UUID du site
            uuid_str = str(site.id).encode('utf-8')
            hash_object = hashlib.md5(uuid_str)
            color = hash_object.hexdigest()[:6]  # Prend les 6 premiers caractères du hash

            site_data = []
            for date in all_dates:
                releve = releves.filter(site=site, date_releve=date).first()
                site_data.append(releve.temperature if releve else None)

            datasets.append({
                'label': site.nom,
                'data': site_data,
                'borderColor': f'#{color}',
                'tension': 0.1,
                'fill': False
            })

        return JsonResponse({'labels': labels, 'datasets': datasets})

class OxygenChartDataView(LoginRequiredMixin,View):
    """
    Vue pour retourner les données d'oxygène au format JSON, pour alimenter un graphique.
    Retourne les niveaux d'oxygène des 21 derniers jours pour chaque site.
    """
    def get(self, request, *args, **kwargs):
        start_date = timezone.now().date() - timedelta(days=21)
        releves = ReleveTempOxy.objects.filter(
            date_releve__gte=start_date,
            oxygene__isnull=False
        ).select_related('site').order_by('site__nom', 'date_releve')
        all_dates = sorted(set(releve.date_releve for releve in releves))
        labels = [date.strftime("%Y-%m-%d") for date in all_dates]
        sites = set(releve.site for releve in releves)
        datasets = []
        for site in sites:
            uuid_str = str(site.id).encode('utf-8')
            hash_object = hashlib.md5(uuid_str)
            color = hash_object.hexdigest()[:6]
            site_data = []
            for date in all_dates:
                releve = releves.filter(site=site, date_releve=date).first()
                site_data.append(releve.oxygene if releve else None)
            datasets.append({
                'label': site.nom,
                'data': site_data,
                'borderColor': f'#{color}',
                'tension': 0.1,
                'fill': False
            })
        return JsonResponse({'labels': labels, 'datasets': datasets})

class FlowChartDataView(LoginRequiredMixin, View):
    """
    Vue pour retourner les données de débit au format JSON, pour alimenter un graphique.
    Retourne les débits des 28 derniers jours pour chaque site.
    """
    def get(self, request, *args, **kwargs):
        start_date = timezone.now().date() - timedelta(days=28)
        releves = ReleveTempOxy.objects.filter(
            date_releve__gte=start_date,
            debit__isnull=False
        ).select_related('site').order_by('site__nom', 'date_releve')
        all_dates = sorted(set(releve.date_releve for releve in releves))
        labels = [date.strftime("%Y-%m-%d") for date in all_dates]
        sites = set(releve.site for releve in releves)
        datasets = []
        for site in sites:
            uuid_str = str(site.id).encode('utf-8')
            hash_object = hashlib.md5(uuid_str)
            color = hash_object.hexdigest()[:6]
            site_data = []
            for date in all_dates:
                releve = releves.filter(site=site, date_releve=date).first()
                site_data.append(releve.debit if releve else None)
            datasets.append({
                'label': site.nom,
                'data': site_data,
                'borderColor': f'#{color}',
                'tension': 0.1,
                'fill': False
            })
        return JsonResponse({'labels': labels, 'datasets': datasets})

class DashboardTemperatureView(LoginRequiredMixin, TemplateView):
    """
    Vue pour afficher le tableau de bord avec les graphiques de température, oxygène et débit.
    """
    template_name = 'dashboard.html'
