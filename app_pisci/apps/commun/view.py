from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render



class StandardDeleteMixin:
    template_name = "confirm_delete.html"
    success_message = "L'élément a été supprimé avec succès !"
    list_url_name = None  # À redéfinir dans chaque vue

    def get_success_url(self):
        if self.list_url_name:
            return reverse_lazy(self.list_url_name)
        raise ImproperlyConfigured("Tu dois définir `list_url_name` dans ta vue.")

    def get_template_names(self):
        return ["confirm_delete.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["return_url"] = self.get_success_url()
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)  # `self.request` est déjà disponible
        return super().delete(request, *args, **kwargs)  # `request` est passé automatiquement

    def form_valid(self, form):
        print("form_valid appelé !")
        messages.success(self.request, self.success_message)
        return super().form_valid(form)  # Appelle la méthode parente pour finaliser la suppression
