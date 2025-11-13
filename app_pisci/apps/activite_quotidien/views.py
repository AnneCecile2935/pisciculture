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
    Vue pour la création d'un nouveau repas (nourrissage).
    Vérifie la cohérence entre le bassin, le site et le lot, et associe automatiquement l'utilisateur connecté.
    Met à jour la date du dernier nourrissage pour le lot concerné.
    """
    model = Nourrissage
    form_class = NourrissageForm
    template_name = 'activite_quotidien/nourrissage_form.html'
    success_url = reverse_lazy('activite_quotidien:nourrissage-list')

    def form_valid(self, form):
        """
        Valide le formulaire et sauvegarde le repas.
        Vérifie que le bassin appartient bien au site sélectionné et que le lot appartient au bassin.
        Met à jour la date du dernier nourrissage pour le lot.
        """
        bassin = form.cleaned_data['bassin']
        site_prod = form.cleaned_data['site_prod']
        # Vérifie que le bassin appartient au site sélectionné
        if bassin.site != site_prod:
            messages.error(self.request, "Le bassin ne appartient pas au site sélectionné.")
            return self.form_invalid(form)
        crea_lot = form.cleaned_data['crea_lot']
        # Vérifie que le lot appartient au bassin sélectionné
        if crea_lot.bassin != bassin:
            messages.error(self.request, "Le lot n'appartient pas au bassin sélectionné.")
            return self.form_invalid(form)

        # Associe l'utilisateur connecté pour la traceabilité
        form.instance.cree_par = self.request.user
        # Met à jour la date du dernier nourrissage pour le lot
        if crea_lot:
            crea_lot.dernier_nourrissage = timezone.now()
            crea_lot.save(update_fields=['dernier_nourrissage'])
        messages.success(self.request, "Le repas a été enregistré avec succès!")
        return super().form_valid(form)

    def get_initial(self):
        """
        Initialise le formulaire avec la date du jour par défaut.
        """
        initial = super().get_initial()
        initial['date_repas'] = timezone.now().date()
        return initial

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
    Vue pour mettre à jour un repas existant.
    Valide la quantité, l'aliment et le motif d'absence.
    Met à jour la date du dernier nourrissage pour le lot associé.
    """
    model = Nourrissage
    form_class = NourrissageForm
    template_name = 'activite_quotidien/nourrissage_form.html'
    success_url = reverse_lazy('activite_quotidien:nourrissage-list')

    def get_form(self, form_class=None):
        """
        Initialise le formulaire avec le bassin actuel et filtre les bassins par site si nécessaire.
        """
        form = super().get_form(form_class)
        # Initialise le champ bassin avec la valeur actuelle
        if hasattr(self, 'object') and self.object:
            form.fields['bassin'].initial = self.object.bassin
            # Filtre les bassins par site si nécessaire
            if hasattr(self.object, 'site_prod'):
                form.fields['bassin'].queryset = Bassin.objects.filter(site=self.object.site_prod)
        return form

    def form_valid(self, form):
        """
        Valide et sauvegarde les modifications apportées à un repas.
        Vérifie la cohérence des données (quantité positive, aliment requis si quantité > 0, motif requis si quantité nulle).
        """
        nourrissage = form.save(commit=False)
        site_prod = nourrissage.site_prod
        date_repas = self.request.POST.get('date_repas') or nourrissage.date_repas or timezone.now().date()
        notes = self.request.POST.get('notes') or nourrissage.notes
        erreurs = False

        # Validation de la quantité
        qte_str = form.cleaned_data.get('qte')
        try:
            if qte_str:
                qte_str = str(qte_str).replace(',', '.')
                qte = float(qte_str)
                if qte <= 0:
                    form.add_error('qte', "La quantité doit être positive.")
                    erreurs = True
            else:
                qte = None
        except ValueError:
            form.add_error('qte', "Saisissez un nombre valide.")
            erreurs = True
            qte = None

        # Cohérence quantité/motif/aliment
        motif = form.cleaned_data.get('motif_absence')
        aliment = form.cleaned_data.get('aliment')
        if qte is None or qte == 0:
            if not motif:
                form.add_error('motif_absence', "Un motif est requis si la quantité est vide ou nulle.")
                erreurs = True
        else:
            if not aliment:
                form.add_error('aliment', "Un aliment est requis si une quantité est saisie.")
                erreurs = True

        # Lot associé
        bassin = form.cleaned_data.get('bassin')
        lot = bassin.lots_poissons.first() if bassin else None
        if not lot:
            form.add_error(None, f"Aucun lot trouvé pour le bassin {bassin.nom if bassin else ''}.")
            erreurs = True

        if erreurs:
            return self.form_invalid(form)

        # Mise à jour de l'objet Nourrissage
        nourrissage.qte = qte
        nourrissage.motif_absence = motif if qte is None or qte == 0 else None
        nourrissage.aliment = aliment
        nourrissage.crea_lot = lot
        nourrissage.date_repas = date_repas
        nourrissage.notes = notes
        nourrissage.save()

        # Met à jour dernier_nourrissage du lot
        if lot:
            lot.dernier_nourrissage = timezone.now()
            lot.save(update_fields=['dernier_nourrissage'])

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
    Vue pour retourner la liste des repas au format JSON.
    Utilisée pour alimenter une interface dynamique.
    """
    def get(self, request, *args, **kwargs):
        """
        Retourne la liste des repas avec leurs informations associées (site, bassin, lot, aliment, etc.) au format JSON.
        """
        nourrissages = Nourrissage.objects.select_related(
            'site_prod', 'bassin', 'crea_lot', 'aliment', 'cree_par'
        ).annotate(
            # Annote les motifs d'absence pour les afficher sous forme de libellés
            motif_nom=Case(
                *[When(motif_absence=m[0], then=Value(m[1])) for m in Nourrissage.MOTIFS_ABSENCE],
                default=Value(None),
                output_field=CharField()
            )
        ).values(
            'id', 'site_prod__nom', 'bassin__nom', 'crea_lot__code_lot', 'qte',
            'date_repas', 'aliment__nom', 'cree_par__username', 'notes',
            'motif_absence', 'motif_nom', 'crea_lot__dernier_nourrissage'
        ).order_by('-date_repas')

        return JsonResponse(list(nourrissages), safe=False)

import json

class NourrissageParSiteView(LoginRequiredMixin, FormView):
    """
    Vue pour saisir plusieurs repas pour tous les bassins d'un site en une seule fois.
    Utilise un FormSet pour gérer un formulaire par bassin.
    """
    template_name = 'activite_quotidien/nourrissage_par_site_form.html'
    success_url = reverse_lazy('activite_quotidien:nourrissage-list')
    form_class = NourrissageFormSet

    def get_form_kwargs(self):
        """
        Passe les données initiales au FormSet.
        """
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = self.get_initial_data()
        return kwargs

    def get_initial_data(self):
        """
        Initialise les données du FormSet avec les bassins du site et les derniers aliments utilisés.
        """
        site = get_object_or_404(Site, id=self.kwargs['site_id'])
        bassins = Bassin.objects.filter(site=site).prefetch_related('lots_poissons')
        initial_data = []

        for bassin in bassins:
            last_nourrissage = Nourrissage.objects.filter(bassin=bassin).order_by('-date_repas').first()
            aliment_id = str(last_nourrissage.aliment.id) if last_nourrissage and last_nourrissage.aliment else None
            initial_data.append({
                'bassin': bassin,
                'aliment': aliment_id,
            })
        return initial_data

    def get_form(self, form_class=None):
        """
        Initialise chaque sous-formulaire avec la liste des bassins du site.
        """
        form = super().get_form(form_class)
        for subform in form:
            subform.site_id = self.kwargs['site_id']
            subform.fields['bassin'].queryset = Bassin.objects.filter(site_id=self.kwargs['site_id'])
        return form

    def get_context_data(self, **kwargs):
        """
        Ajoute le site et la date du jour au contexte du template.
        """
        context = super().get_context_data(**kwargs)
        site = get_object_or_404(Site, id=self.kwargs['site_id'])
        context['site'] = site
        context['today'] = timezone.now().date()
        return context

    def form_valid(self, form):
        """
        Valide et sauvegarde les repas pour chaque bassin.
        Ignore les bassins sans lot et gère les erreurs par repas.
        """
        self.formset = form
        date_repas = self.request.POST.get('date_repas') or timezone.now().date()
        notes = self.request.POST.get('notes')
        nourrissages = []

        for subform in self.formset:
            bassin = subform.cleaned_data.get('bassin')
            if not bassin:
                continue  # Ignore si pas de bassin (cas rare)

            # Vérifie si le bassin a un lot
            lot = bassin.lots_poissons.first()
            if not lot:
                continue  # On passe au suivant

            qte_str = subform.cleaned_data.get('qte')
            aliment = subform.cleaned_data.get('aliment')
            motif = subform.cleaned_data.get('motif_absence')

            # Gestion spéciale pour "à jeun"
            if motif == 'ajeun':
                qte = 0  # Force la quantité à 0
            else:
                # Validation normale pour les autres cas
                try:
                    if qte_str:
                        qte_str = str(qte_str).replace(',', '.')
                        qte = float(qte_str)
                        if qte < 0:  # Accepte 0 pour les autres motifs
                            subform.add_error('qte', "La quantité ne peut pas être négative.")
                            continue
                    else:
                        qte = None
                except ValueError:
                    subform.add_error('qte', "Saisissez un nombre valide.")
                    continue

            # Motif requis si quantité est None ou 0
            if qte is None or qte == 0:
                if not motif:
                    subform.add_error('motif_absence', "Un motif est requis si la quantité est vide ou nulle.")
                    continue
            else:
                # Aliment requis uniquement si quantité > 0
                if not aliment:
                    subform.add_error('aliment', "Un aliment est requis si une quantité est saisie.")
                    continue

            # Création du repas
            nourrissage = Nourrissage(
                site_prod=bassin.site,
                bassin=bassin,
                crea_lot=lot,
                aliment=aliment,
                qte=qte,
                motif_absence=motif if (qte is None or qte == 0) else None,
                date_repas=date_repas,
                notes=notes,
                cree_par=self.request.user,
            )
            nourrissages.append(nourrissage)


        # Enregistrement des repas valides
        if nourrissages:
            try:
                Nourrissage.objects.bulk_create(nourrissages)

                for nourrissage in nourrissages:
                    if nourrissage.crea_lot:
                        nourrissage.crea_lot.dernier_nourrissage = timezone.now()
                        nourrissage.crea_lot.save(update_fields=['dernier_nourrissage'])
                messages.success(self.request, f"{len(nourrissages)} repas enregistrés !")
            except Exception as e:

                messages.error(self.request, f"Erreur lors de l'enregistrement: {e}")
                return self.form_invalid(form)
        else:
            messages.warning(self.request, "Aucun repas valide à enregistrer.")
            return self.form_invalid(form)

        return super().form_valid(form)  # Redirection



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
