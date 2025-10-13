from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Site, Bassin
from django.urls import reverse_lazy
from .forms import SiteForm, BassinForm
from django.urls import reverse

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

class BassinListView(LoginRequiredMixin, ListView):
    model = Bassin
    template_name = "sites/bassin_list.html"
    context_object_name = "bassins"

    def get_queryset(self):
        site_id = self.kwargs.get("site_id")
        return Bassin.objects.filter(site_id=site_id, est_actif=True)

class BassinCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = BassinForm
    model = Bassin
    template_name = "sites/bassin_form.html"
    permission_required = "sites.add_bassin"

    def get_success_url(self):
        return reverse('sites:bassin-list', args=[self.object.site.id])

class BassinUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = BassinForm
    model = Bassin
    template_name = "sites/bassin_form.html"
    permission_required = "sites.change_bassin"

    def get_success_url(self):
        return reverse('sites:bassin-list', args=[self.object.site.id])

class BassinDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Bassin
    template_name = "sites/bassin_confirm_delete.html"
    fields = ["nom", "est_actif"]
    permission_required = "sites.delete_bassin"
    def get_success_url(self):
        return reverse('sites:site-list')
