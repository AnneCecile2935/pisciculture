from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Case, When, Value, CharField
from datetime import timedelta
from apps.sites.models import Site, Bassin
from apps.activite_quotidien.models import ReleveTempOxy
from apps.activite_quotidien.forms import ReleveTempOxyForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, View, FormView, TemplateView
from apps.commun.view import StandardDeleteMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Nourrissage
from .forms import NourrissageForm, NourrissageFormSet
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Max
from apps.stocks.models import LotDePoisson
from django import forms
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
import json
from django.http import JsonResponse
from apps.aliments.models import Aliment
from django.forms import formset_factory
import hashlib


class NourrissageCreateView(LoginRequiredMixin, CreateView):
    model = Nourrissage
    form_class = NourrissageForm
    template_name = 'activite_quotidien/nourrissage_form.html'
    success_url = reverse_lazy('activite_quotidien:nourrissage-list')

    def form_valid(self, form):
        """Vérifie la cohérence bassin/site/lot (pas de restriction par utilisateur)."""
        bassin = form.cleaned_data['bassin']
        site_prod = form.cleaned_data['site_prod']
        if bassin.site != site_prod:
            messages.error(self.request, "Le bassin ne appartient pas au site sélectionné.")
            return self.form_invalid(form)

        crea_lot = form.cleaned_data['crea_lot']
        if crea_lot.bassin != bassin:
            messages.error(self.request, "Le lot ne appartient pas au bassin sélectionné.")
            return self.form_invalid(form)

        # Associe l'utilisateur connecté (pour trace
        form.instance.cree_par = self.request.user
        messages.success(self.request, "Le repas a été enregistré avec succès!")
        return super().form_valid(form)

    def get_initial(self):
        """Pré-remplit la date avec la date du jour."""
        initial = super().get_initial()
        initial['date_repas'] = timezone.now().date()
        return initial

class NourrissageListView(LoginRequiredMixin, ListView):
    model = Nourrissage
    template_name = 'activite_quotidien/nourrissage_list.html'
    context_object_name = 'nourrissages'
    paginate_by = 20

    def get_queryset(self):
        """Tri par défaut : repas les plus récents en premier."""
        return super().get_queryset().order_by('-date_repas')

class NourrissageDetailView(LoginRequiredMixin, DetailView):
    model = Nourrissage
    template_name = 'activite_quotidien/nourrissage_detail.html'
    context_object_name = 'nourrissage'

class NourrissageUpdateView(LoginRequiredMixin, UpdateView):
    model = Nourrissage
    form_class = NourrissageForm
    template_name = 'activite_quotidien/nourrissage_form.html'
    success_url = reverse_lazy('activite_quotidien:nourrissage-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Initialise le champ bassin avec la valeur actuelle
        if hasattr(self, 'object') and self.object:
            form.fields['bassin'].initial = self.object.bassin
            # Filtre les bassins par site si nécessaire
            if hasattr(self.object, 'site_prod'):
                form.fields['bassin'].queryset = Bassin.objects.filter(site=self.object.site_prod)
        return form

    def form_valid(self, form):
        nourrissage = form.save(commit=False)

        # ✅ Récupère site_prod depuis l'objet existant
        site_prod = nourrissage.site_prod

        # Récupère date_repas et notes depuis POST si disponibles
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

        # Mise à jour de l'objet
        nourrissage.qte = qte
        nourrissage.motif_absence = motif if qte is None or qte == 0 else None
        nourrissage.aliment = aliment
        nourrissage.crea_lot = lot
        nourrissage.date_repas = date_repas
        nourrissage.notes = notes
        nourrissage.save()

        messages.success(self.request, "Le repas a été mis à jour avec succès !")
        return super().form_valid(form)

class NourrissageDeleteView(LoginRequiredMixin,StandardDeleteMixin, DeleteView):
    model = Nourrissage
    list_url_name='activite_quotidien:nourrissage-list'


class NourrissageListJsonView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        nourrissages = Nourrissage.objects.select_related(
            'site_prod', 'bassin', 'crea_lot', 'aliment', 'cree_par'
        ).annotate(
            motif_nom=Case(
                *[When(motif_absence=m[0], then=Value(m[1])) for m in Nourrissage.MOTIFS_ABSENCE],
                default=Value(None),
                output_field=CharField()
            )
        ).values(
            'id', 'site_prod__nom', 'bassin__nom', 'crea_lot__code_lot', 'qte',
            'date_repas', 'aliment__nom', 'cree_par__username', 'notes',
            'motif_absence', 'motif_nom'
        ).order_by('-date_repas')

        return JsonResponse(list(nourrissages), safe=False)

import json

class NourrissageParSiteView(FormView):
    template_name = 'activite_quotidien/nourrissage_par_site_form.html'
    success_url = reverse_lazy('activite_quotidien:nourrissage-list')
    form_class = NourrissageFormSet

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = self.get_initial_data()
        return kwargs

    def get_initial_data(self):
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
        form = super().get_form(form_class)
        for subform in form:
            subform.site_id = self.kwargs['site_id']
            subform.fields['bassin'].queryset = Bassin.objects.filter(site_id=self.kwargs['site_id'])
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = get_object_or_404(Site, id=self.kwargs['site_id'])
        context['site'] = site
        context['today'] = timezone.now().date()
        return context

    def form_valid(self, form):
        self.formset = form
        date_repas = self.request.POST.get('date_repas') or timezone.now().date()
        notes = self.request.POST.get('notes')
        nourrissages = []
        erreurs = False

        for subform in self.formset:
            bassin = subform.cleaned_data.get('bassin')
            qte_str = subform.cleaned_data.get('qte')
            aliment = subform.cleaned_data.get('aliment')
            motif = subform.cleaned_data.get('motif_absence')

            # Validation de la quantité
            try:
                if qte_str:
                    qte_str = str(qte_str).replace(',', '.')
                    qte = float(qte_str)
                    if qte <= 0:
                        subform.add_error('qte', "La quantité doit être positive.")
                        erreurs = True
                        continue
                else:
                    qte = None
            except ValueError:
                subform.add_error('qte', "Saisissez un nombre valide.")
                erreurs = True
                continue

            # Cohérence quantité / motif / aliment
            if qte is None or qte == 0:
                if not motif:
                    subform.add_error('motif_absence', "Un motif est requis si la quantité est vide ou nulle.")
                    erreurs = True
                    continue
            else:
                if not aliment:
                    subform.add_error('aliment', "Un aliment est requis si une quantité est saisie.")
                    erreurs = True
                    continue

            # Lot automatique
            lot = bassin.lots_poissons.first() if bassin else None
            if not lot:
                subform.add_error(None, f"Aucun lot trouvé pour le bassin {bassin.nom if bassin else ''}.")
                erreurs = True
                continue

            # Création de l'objet Nourrissage
            nourrissage = Nourrissage(
                site_prod=bassin.site,
                bassin=bassin,
                crea_lot=lot,
                aliment=aliment,
                qte=qte,
                motif_absence=motif if qte is None or qte == 0 else None,
                date_repas=date_repas,
                notes=notes,
                cree_par=self.request.user,
            )
            nourrissages.append(nourrissage)

        # Enregistrement en base
        if nourrissages:
            Nourrissage.objects.bulk_create(nourrissages)
            messages.success(self.request, f"{len(nourrissages)} repas enregistrés !")
        else:
            messages.warning(self.request, "Aucun repas valide à enregistrer.")

        if erreurs:
            return self.form_invalid(form)

        return super().form_valid(form)

class ChoixSiteEnregistrementRepasView(TemplateView):
    template_name = 'activite_quotidien/choix_site_enregistrement_repas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites'] = Site.objects.all()
        return context

class ListRelevesView(LoginRequiredMixin, ListView):
    model = ReleveTempOxy
    template_name = 'activite_quotidien/releve_list.html'
    context_object_name = 'releves'

    def get_queryset(self):
        today = timezone.now().date()
        site_id = self.request.GET.get('site')
        releves = ReleveTempOxy.objects.filter(date_releve=today).order_by('site__nom', 'moment_jour')
        if site_id:
            releves = releves.filter(site_id=site_id)
        return releves

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites'] = Site.objects.all()
        context['today'] = timezone.now().date()
        return context

class CreateReleveView(LoginRequiredMixin, CreateView):
    model = ReleveTempOxy
    form_class = ReleveTempOxyForm
    template_name = 'activite_quotidien/releve_form.html'
    success_url = reverse_lazy('activite_quotidien:releve-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['date_releve'] = timezone.now().date()
        return initial


class UpdateReleveView(LoginRequiredMixin, UpdateView):
    model = ReleveTempOxy
    form_class = ReleveTempOxyForm
    template_name = 'activite_quotidien/releve_form.html'
    success_url = reverse_lazy('activite_quotidien:releve-list')

class DeleteReleveView(LoginRequiredMixin, DeleteView):
    model = ReleveTempOxy
    template_name = 'activite_quotidien/releve_delete.html'
    success_url = reverse_lazy('activite_quotidien:releve-list')

class RelevesListJsonView(LoginRequiredMixin, View):
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

class TempChartDataView(View):
    def get(self, request, *args, **kwargs):
        start_date = timezone.now().date() - timedelta(days=14)
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
    def get(self, request, *args, **kwargs):
        start_date = timezone.now().date() - timedelta(days=14)
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

class DashboardTemperatureView(TemplateView):
    template_name = 'dashboard.html'
