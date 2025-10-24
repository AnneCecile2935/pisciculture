from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Case, When, Value, CharField
from datetime import date
from apps.sites.models import Site, Bassin
from apps.activite_quotidien.models import ReleveTempOxy
from apps.activite_quotidien.forms import ReleveForm
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
    paginate_by = 10

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
        """Vérifie la cohérence bassin/site/lot."""
        bassin = form.cleaned_data['bassin']
        site_prod = form.cleaned_data['site_prod']
        if bassin.site != site_prod:
            messages.error(self.request, "Le bassin ne appartient pas au site sélectionné.")
            return self.form_invalid(form)

        crea_lot = form.cleaned_data['crea_lot']
        if crea_lot.bassin != bassin:
            messages.error(self.request, "Le lot ne appartient pas au bassin sélectionné.")
            return self.form_invalid(form)

        messages.success(self.request, "Le repas a été mis à jour avec succès!")
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
        return [
            {
                'site_prod': str(site.id),  # UUID du site
                'bassin': str(bassin.id),   # UUID du bassin (pas le nom !)
                'crea_lot': str(bassin.lots_poissons.first().id) if bassin.lots_poissons.exists() else None,
                'aliment': str(Nourrissage.objects.filter(bassin=bassin).order_by('-date_repas').first().aliment.id)
                        if Nourrissage.objects.filter(bassin=bassin).exists() and Nourrissage.objects.filter(bassin=bassin).first().aliment
                        else None,
            }
            for bassin in bassins
        ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Transmettre site_id à chaque sous-formulaire
        for subform in form:
            subform.site_id = self.kwargs['site_id']  # Passe site_id à chaque sous-formulaire
            subform.fields['bassin'].queryset = Bassin.objects.filter(site_id=self.kwargs['site_id'])
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = get_object_or_404(Site, id=self.kwargs['site_id'])
        context['site'] = site
        context['today'] = timezone.now().date()
        return context

    def form_valid(self, form):
        self.formset = form  # Stocke le formset pour form_valid
        date_repas = self.request.POST.get('date_repas')
        notes = self.request.POST.get('notes')
        nourrissages = []
        erreurs = False

        for subform in self.formset:
            subform.site_id = self.kwargs['site_id']
            bassin = subform.cleaned_data['bassin']
            qte_str = subform.cleaned_data.get('qte')
            motif = subform.cleaned_data.get('motif_absence')
            aliment= subform.cleaned_data.get('aliment')
            crea_lot = subform.cleaned_data.get('crea_lot')

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

            # Vérifie la cohérence quantité/motif/aliment
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

            # Récupère le lot
            lot = bassin.lots_poissons.first()
            if not lot:
                subform.add_error(None, f"Aucun lot trouvé pour le bassin {bassin.nom}.")
                erreurs = True
                continue

            # Crée le repas
            nourrissage = Nourrissage(
                site_prod=bassin.site,
                bassin=bassin,
                crea_lot=lot,
                aliment=aliment,
                qte=qte,
                motif_absence=motif if qte is None or qte == 0 else None,
                date_repas=date_repas,
                cree_par=self.request.user,
                notes=notes,
            )
            nourrissages.append(nourrissage)

        # Enregistrement
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


def index(request):
    return HttpResponse("Bienvenue!")

def liste_releves(request):
    today = date.today()
    site_id = request.GET.get('site')
    releves = ReleveTempOxy.objects.filter(date_creation__date=today).order_by('site__nom', 'moment_jour')
    if site_id:
        releves = releves.filter(site_id=site_id)
    sites = Site.objects.all()
    return render(request, 'activite_quotidien/liste_releves.html', {
        'releves': releves,
        'sites': sites,
        'today': today,
    })

def ajouter_releve(request):
    if request.method == 'POST':
        form = ReleveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_releves')
    else:
        form = ReleveForm()
    return render(request, 'activite_quotidien/ajouter_releve.html', {'form': form})

def releves_manquants(request):
    today = date.today()
    manquants = []
    for site in Site.objects.all():
        matin = ReleveTempOxy.objects.filter(site=site, moment_jour='matin', date_creation__date=today).exists()
        soir = ReleveTempOxy.objects.filter(site=site, moment_jour='soir', date_creation__date=today).exists()
        if not matin or not soir:
            manquants.append({
                'site': site,
                'matin_manquant': not matin,
                'soir_manquant': not soir,
            })
    return render(request, 'activite_quotidien/releves_manquants.html', {'manquants': manquants, 'today': today})
