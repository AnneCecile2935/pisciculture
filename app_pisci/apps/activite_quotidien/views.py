from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import date
from apps.sites.models import Site
from apps.activite_quotidien.models import ReleveTempOxy
from apps.activite_quotidien.forms import ReleveForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Nourrissage
from .forms import NourrissageForm
from django.contrib import messages
from django.utils import timezone

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

class NourrissageDeleteView(LoginRequiredMixin, DeleteView):
    model = Nourrissage
    template_name = 'activite_quotidien/nourrissage_confirm_delete.html'
    success_url = reverse_lazy('activite_quotidien:nourrissage-list')

    def form_valid(self, form):
        messages.success(self.request, "Le repas a bien été supprimé.")
        return super().form_valid(form)


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
