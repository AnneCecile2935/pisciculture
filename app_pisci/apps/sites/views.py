from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Site, Bassin
from django.urls import reverse_lazy
from .forms import SiteForm, BassinForm
from django.urls import reverse
from django.http import JsonResponse
from typing import Any

class SiteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Site
    template_name = "sites/site_list.html"
    context_object_name = "sites"
    permission_required = "sites.view_site"

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

class SiteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Site
    template_name = "sites/site_confirm_delete.html"
    fields = ["nom", "est_actif"]
    success_url = reverse_lazy("sites:site-list")
    permission_required = "sites.delete_site"

class SiteListJsonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "sites.view_site"

    def get(self, request, *args, **kwargs):
        sites = list(Site.objects.all().values('id', 'nom', 'est_actif'))
        return JsonResponse(sites, safe=False)

class BassinListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Bassin
    template_name = "sites/bassin_list.html"
    context_object_name = "bassins"
    permission_required = "sites.view_bassin"


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

    def get_success_url(self):
        return reverse('sites:bassin-list', args=[self.kwargs['site.id']])

class BassinUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = BassinForm
    model = Bassin
    template_name = "sites/bassin_form.html"
    permission_required = "sites.change_bassin"

    def get_success_url(self):
        return reverse('sites:bassin-list', args=[self.object.site.id]) # type: ignore

class BassinDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Bassin
    template_name = "sites/bassin_confirm_delete.html"
    fields = ["nom", "est_actif"]
    permission_required = "sites.delete_bassin"
    def get_success_url(self):
        return reverse('sites:site-list')

class BassinListJsonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "sites.view_bassin"

    def get(self, request, *args, **kwargs):
        site_id = self.kwargs.get("site_id")
        bassins = list(Bassin.objects.filter(site_id=site_id, est_actif=True).values('id', 'nom', 'est_actif'))
        return JsonResponse(bassins, safe=False)


