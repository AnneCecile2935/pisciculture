# 📋 TODO - Améliorations pour Pisciculture

*Dernière mise à jour : 08/11/2025*

> **Légende** :
>
> - ⭐⭐⭐ = Critique (à faire en priorité)
> - ⭐⭐ = Important (quand tu as le temps)
> - ⭐ = Optionnel (si besoin)
> - 🚀 = Amélioration majeure
> - 🐛 = Correction de bug

---

## 🗃️ Structure du projet

### 1. Dossiers à créer

- [ ] `templates/includes/` : Pour les composants réutilisables (ex: `_delete_modal.html`)
- [ ] `scripts/` : Pour les scripts utilitaires (ex: `check_todos.py`)
- [ ] `docs/` : Pour la documentation générée (Sphinx)

---

## 🔧 Mixins et Vues

### StandardDeleteMixin (`apps/commun/views.py`) 🚀

#### ⭐⭐⭐ Corrections critiques

- [ ] Supprimer la redondance entre `delete()` et `form_valid()` :

  ```python
  def delete(self, request, *args, **kwargs):
      return super().delete(request, *args, **kwargs)  # Supprimer messages.success
  ```



 Ajouter une vérification des dépendances avant suppression :

```python
def form_valid(self, form):
    if hasattr(self.object, 'has_dependencies') and self.object.has_dependencies():
        messages.error(self.request, "Impossible de supprimer : des éléments dépendent de cet enregistrement.")
        return redirect(self.get_success_url())
    return super().form_valid(form)
```



#### ⭐⭐ Améliorations recommandées

-  Rendre `success_message` dynamique :

  ```python
  def get_success_message(self):
      return self.success_message % {"nom": str(self.object)}
  ```

-  Ajouter un template générique (`templates/confirm_delete.html`) :

  ```html
  {% extends "base.html" %}
  {% block content %}
  <div class="card bg-light mb-3">
      <div class="card-header bg-danger text-white">
          <h5>⚠️ Confirmer la suppression</h5>
      </div>
      <div class="card-body">
          <p>Êtes-vous sûr de vouloir supprimer <strong>{{ object }}</strong> ?</p>
          <form method="post" onsubmit="return confirm('Cette action est irréversible.')">
              {% csrf_token %}
              <button type="submit" class="btn btn-danger">Supprimer</button>
              <a href="{{ return_url }}" class="btn btn-secondary">Annuler</a>
          </form>
      </div>
  </div>
  {% endblock %}
  ```

-  Ajouter une confirmation JavaScript :

  ```javascript
  // Dans confirm_delete.html
  <form method="post" onsubmit="return confirm('Supprimer définitivement ?');">
  ```

#### ⭐ Améliorations optionnelles

-  Ajouter un logging des suppressions :

  ```python
  import logging
  logger = logging.getLogger(__name__)

  def form_valid(self, form):
      logger.warning(f"Suppression de {self.object} par {self.request.user}")
      return super().form_valid(form)
  ```

-  Permettre une suppression logique (soft delete) :

  ```python
  def form_valid(self, form):
      if hasattr(self.object, 'est_actif'):
          self.object.est_actif = False
          self.object.save()
          messages.success(self.request, "L'élément a été désactivé.")
      else:
          return super().form_valid(form)
      return redirect(self.get_success_url())
  ```

#### Tests

-  Écrire des tests pour `StandardDeleteMixin` :

  ```python
  # tests/test_mixins.py
  def test_delete_redirects_to_list(self):
      response = self.view.delete(self.request)
      self.assertRedirects(response, reverse_lazy("test_list"))
  ```

------

## 📝 Formulaires

### AlimentForm (`apps/stocks/forms.py`) ⭐⭐⭐

-  Ajouter `RegexValidator` pour `code_alim` :

  ```python
  from django.core.validators import RegexValidator

  class AlimentForm(forms.ModelForm):
      class Meta:
          widgets = {
              "code_alim": forms.TextInput(attrs={
                  "pattern": "[A-Z0-9]{6}",
                  "title": "6 caractères alphanumériques majuscules"
              })
          }
  ```

-  Filtrer les fournisseurs actifs dans `__init__` :

  ```python
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields["fournisseur"].queryset = self.fields["fournisseur"].queryset.filter(est_actif=True)
  ```

-  Ajouter validation côté client :

  ```javascript
  // static/js/aliment_form.js
  document.addEventListener('DOMContentLoaded', function() {
      const codeInput = document.getElementById('id_code_alim');
      if (codeInput) {
          codeInput.addEventListener('input', function() {
              this.value = this.value.toUpperCase().substring(0, 6);
          });
      }
  });
  ```

### LotDePoissonForm (`apps/stocks/forms.py`) ⭐⭐

-  Valider que `quantite_actuelle` ≤ `quantite` :

  ```python
  def clean(self):
      cleaned_data = super().clean()
      if cleaned_data.get("quantite_actuelle") > cleaned_data.get("quantite"):
          raise forms.ValidationError("La quantité actuelle ne peut pas dépasser la quantité initiale.")
      return cleaned_data
  ```

------

## 🗂️ Modèles

### Aliment (`apps/stocks/models.py`) ⭐⭐

-  Ajouter une méthode pour générer un `code_alim` automatique :

  ```python
  from django.db import models
  import random

  class Aliment(models.Model):
      def save(self, *args, **kwargs):
          if not self.code_alim:
              self.code_alim = f"{self.espece.code[:2]}{self.fournisseur.code[:2]}{random.randint(10, 99)}"
          super().save(*args, **kwargs)
  ```

-  Ajouter une propriété pour vérifier l'utilisation :

  ```python
  r@property
  def is_used(self):
      return self.nourrissage_set.exists()
  ```

### Bassin (`apps/sites/models.py`) ⭐⭐

-  Ajouter une méthode pour vérifier les dépendances :

  ```python
  def has_dependencies(self):
      return self.lots_poissons.exists() or self.releves.exists()
  ```

------

## 📄 Templates

### Base Template (`templates/base.html`) ⭐⭐

-  Ajouter un bloc pour les messages flash :

  ```python
  {% if messages %}
  <div class="container mt-3">
      {% for message in messages %}
      <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
          {{ message }}
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
      {% endfor %}
  </div>
  {% endif %}
  ```

-  Intégrer Font Awesome :

  ```html
  <head>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  </head>
  ```

### Listes (`templates/sites/bassin_list.html`) ⭐

-  Ajouter des badges pour les statuts :

  ```html
  <span class="badge {% if bassin.est_actif %}bg-success{% else %}bg-secondary{% endif %}">
      {{ bassin.get_statut_display }}
  </span>
  ```

-  Ajouter un filtre de recherche avancé :

  ```html
  r<form method="get" class="mb-3">
      <div class="input-group">
          <input type="text" name="q" class="form-control" placeholder="Rechercher...">
          <button class="btn btn-primary" type="submit"><i class="fas fa-search"></i></button>
      </div>
  </form>
  ```

------

## 🧪 Tests

### Tests unitaires ⭐⭐

-  Tester `StandardDeleteMixin` :

  ```python
  r# tests/test_views.py
  def test_delete_mixin_redirects(self):
      response = self.client.post(reverse('bassin_delete', args=[1]))
      self.assertRedirects(response, reverse('bassin_list'))
  ```

-  Tester les validations des formulaires :

  ```python
  def test_aliment_form_validation(self):
      form = AlimentForm(data={"code_alim": "abc!@#"})
      self.assertFalse(form.is_valid())
  ```
