from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import date
from apps.sites.models import Site
from apps.activite_quotidien.models import ReleveTempOxy
from apps.activite_quotidien.forms import ReleveForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'activité_quotidien/dashboard.html'
    
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
