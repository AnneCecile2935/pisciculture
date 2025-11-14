from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render



class StandardDeleteMixin:
    """
    Mixin standardisé pour les vues de suppression (DeleteView).

    Ce mixin fournit une configuration par défaut pour les vues de suppression,
    incluant :
    - Un template de confirmation générique
    - Un message de succès personnalisable
    - Une redirection vers une liste après suppression
    - Une gestion des messages utilisateur

    Attributes:
        template_name (str): Chemin du template de confirmation.
            Par défaut : "confirm_delete.html"
        success_message (str): Message affiché après une suppression réussie.
            Par défaut : "L'élément a été supprimé avec succès !"
        list_url_name (str): Nom de l'URL pour la redirection après suppression.
            **Doit être redéfini dans chaque vue héritante** pour éviter une erreur.
    """

    template_name = "confirm_delete.html"
    """str: Chemin du template utilisé pour afficher la confirmation de suppression."""
    success_message = "L'élément a été supprimé avec succès !"
    """str: Message affiché à l'utilisateur après une suppression réussie."""
    list_url_name = None  # À redéfinir dans chaque vue
    """str: Nom de l'URL (reverse_lazy) vers laquelle rediriger après suppression.
    Exemple : "bassin_list" pour rediriger vers la liste des bassins.
    **Obligatoire** : Doit être redéfini dans chaque classe héritante."""

    def get_success_url(self):
        """
        Construit l'URL de redirection après une suppression réussie.

        Returns:
            str: URL générée via `reverse_lazy` à partir de `list_url_name`.

        Raises:
            ImproperlyConfigured: Si `list_url_name` n'est pas défini.
                Empêche les erreurs silencieuses et force la configuration.

        Example:
            Si `list_url_name = "bassin_list"`, redirige vers l'URL nommée "bassin_list".
        """
        if self.list_url_name:
            return reverse_lazy(self.list_url_name)
        raise ImproperlyConfigured("Tu dois définir `list_url_name` dans ta vue.")

    def get_template_names(self):
        """
        Retourne la liste des templates possibles pour cette vue.

        Override cette méthode si tu veux utiliser plusieurs templates
        (ex: un template spécifique par modèle).

        Returns:
            list: Liste contenant le template par défaut.
        """
        return ["confirm_delete.html"]

    def get_context_data(self, **kwargs):
        """
        Ajoute des données supplémentaires au contexte du template.

        Args:
            **kwargs: Arguments supplémentaires pour le contexte.

        Returns:
            dict: Contexte enrichi avec :
                - return_url (str): URL de redirection après suppression.
                - **kwargs: Données du contexte parent.

        Example:
            Le template peut utiliser `return_url` pour un bouton "Annuler" :
            ```html
            <a href="{{ return_url }}" class="btn btn-secondary">Annuler</a>
            ```
        """
        context = super().get_context_data(**kwargs)
        context["return_url"] = self.get_success_url()
        return context

    def delete(self, request, *args, **kwargs):
        """
        Surcharge la méthode `delete` pour ajouter un message de succès.

        Args:
            request (HttpRequest): Requête HTTP actuelle.
            *args: Arguments positionnels.
            **kwargs: Arguments nommés.

        Returns:
            HttpResponseRedirect: Redirige vers `get_success_url()` après suppression.

        Notes:
            - Utilise `self.request` (déjà disponible) pour afficher le message.
            - Appelle la méthode parente pour effectuer la suppression réelle.
        """
        messages.success(self.request, self.success_message)  # `self.request` est déjà disponible
        return super().delete(request, *args, **kwargs)  # `request` est passé automatiquement

    def form_valid(self, form):
        """
        Gère le cas où le formulaire de confirmation est valide.

        Args:
            form (ModelForm): Formulaire de confirmation (généralement vide).

        Returns:
            HttpResponseRedirect: Redirige vers `get_success_url()`.

        Notes:
            - Affiche un message de succès (redondant avec `delete()`, à harmoniser).
            - Appelle la méthode parente pour finaliser la suppression.
            - **TODO**: Supprimer la redondance avec `delete()` (voir TODO.md).
        """
        print("form_valid appelé !")
        messages.success(self.request, self.success_message)
        return super().form_valid(form)  # Appelle la méthode parente pour finaliser la suppression
