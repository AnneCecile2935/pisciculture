from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import date
from apps.sites.models import Site, Bassin
from apps.activite_quotidien.models import ReleveTempOxy
from apps.activite_quotidien.forms import ReleveForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, View, FormView, TemplateView
from apps.commun.view import StandardDeleteMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Nourrissage
from .forms import NourrissageForm, NourrissageParSiteForm
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
        ).values(
            'id',
            'site_prod__nom',  # Notez les doubles underscores pour les relations
            'bassin__nom',
            'crea_lot__code_lot',
            'qte',
            'date_repas',
            'aliment__nom',
            'cree_par__username',  # Notez les doubles underscores pour les relations
            'notes'
        ).order_by('-date_repas')

        print(list(nourrissages))  # Pour débogage

        return JsonResponse(list(nourrissages), safe=False)

class NourrissageParSiteView(FormView):
    template_name = 'activite_quotidien/nourrissage_par_site_form.html'
    form_class = NourrissageParSiteForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['site_id'] = self.kwargs['site_id']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = get_object_or_404(Site, id=self.kwargs['site_id'])

        # Passe les bassins en JSON
        form = context['form']
        bassins = form.bassins
        unique_bassins = []
        bassin_ids = set()

        for bassin in bassins:
            if bassin.id not in bassin_ids:
                bassin_ids.add(bassin.id)
                unique_bassins.append(bassin)

        context['bassins_json'] = json.dumps([
            {
                'id': str(bassin.id),
                'nom': bassin.nom,
                'dernier_aliment_id': str(bassin.dernier_aliment_id) if bassin.dernier_aliment_id else None,
                'lot_id': str(bassin.lots_poissons.first().id) if bassin.lots_poissons.first() else None
            }
            for bassin in unique_bassins])

        # Passe les aliments en JSON
        aliments = Aliment.objects.all().values('id', 'nom')
        aliments_list = list(aliments)
        for aliment in aliments_list:
            aliment['id'] = str(aliment['id'])
        context['aliments_json'] = json.dumps(aliments_list)

        return context

    def form_valid(self, form):
        form.save(self.request.user)
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
