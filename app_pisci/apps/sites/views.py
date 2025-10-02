from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Site

class SiteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Site
    template_name = "sites/site_list.html"
    context_object_name = "sites"
    permission_required = "sites.view_site"

class SiteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Site
    template_name = "sites/site_form.html"
    fields = ["nom", "est-actif"]
    success_url = reverse_lazy("sites:site-list")
    permission_required = "sites.add_site"

class SiteUpdateView(LoginRequiredMixin, permission_required, UpdateView):
    model = Site
    template_name = "sites/site_form.html"
    fields = ["nom", "est-actif"]
    success_url = reverse_lazy("sites:site-list")
    permission_required = "sites.change_site"

class SiteDeleteView(LoginRequiredMixin, permission_required, DeleteView):
    model = Site
    template_name = "sites/site_confirm_delete.html"
    fields = ["nom", "est-actif"]
    success_url = reverse_lazy("sites:site-list")
    permission_required = "sites.delete_site"

class BassinListView(LoginRequiredMixin, ListView):
    model = Bassin
    template_name = "sites/bassin_list.html"
    context_object_name = "bassins"

    def get_queryset(self):
        site_id = self.kwargs.get("site_id")
        return Bassin.objects.filter(site_id=site_id, est_actif=True)

class BassinCreateView(LoginRequiredMixin, permission_required, CreateView):
    model = Bassin
    template_name = "sites/bassin_form.html"
    fields = ["nom", "est_actif"]
    success_url = reverse_lazy("sites:bassin-list")
    permission_required = "sites.add_bassin"

class BassinUpdateView(LoginRequiredMixin, permission_required, UpdateView):
    model = Bassin
    template_name = "sites/bassin_form.html"
    fields = ["nom", "est-actif"]
    success_url = reverse_lazy("sites:bassin-list")
    permission_required = "sites.change_bassin"

class BassinDeleteView(LoginRequiredMixin, permission_required, DeleteView):
    model = Bassin
    template_name = "sites/bassin_confirm_delete.html"
    fields = ["nom", "est-actif"]
    success_url = reverse_lazy("sites:bassin_list")
    permission_required = "sites.delete_bassin"
