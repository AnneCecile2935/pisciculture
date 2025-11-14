# TODO - Améliorations du projet Pisciculture

> **Priorités** :
> - ⭐⭐⭐ = Critique (à faire dès que possible)
> - ⭐⭐ = Important (quand tu as le temps)
> - ⭐ = Optionnel (si besoin)

---

## 📝 Formulaires

### AlimentForm (`apps/stocks/forms.py`)
**Objectif** : Renforcer les validations pour éviter les erreurs de saisie.

#### Validations côté serveur (⭐⭐⭐)
- [ ] Ajouter `RegexValidator` dans le modèle `Aliment` pour `code_alim` :
  ```python
  from django.core.validators import RegexValidator

  class Aliment(models.Model):
      code_alim = models.CharField(
          max_length=6,
          unique=True,
          validators=[
              RegexValidator(
                  regex='^[A-Z0-9]{6}\$',
                  message='Le code doit être composé de 6 caractères alphanumériques majuscules.',
                  code='invalid_code_alim'
              )
          ]
      )

- [ ] AJouter une méthode clean_code_alim() dans AlimentForm
```bash
def clean_code_alim(self):
    code_alim = self.cleaned_data.get("code_alim")
    if code_alim:
        code_alim = code_alim.upper()  # Normalisation en majuscules
        if not code_alim.isalnum():
            raise forms.ValidationError("Seuls les caractères alphanumériques sont autorisés.")
    return code_alim
```
- [ ] Filtrer les fournisseurs actifs dans __init__:
```bash
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields["fournisseur"].queryset = self.fields["fournisseur"].queryset.filter(est_actif=True)
```

#### Validations côté serveur (⭐⭐⭐)

- [ ] AJouter un script JavaScript pour:

Limiter à 6 caractères
Convertir en majuscules automatiquement
Valider le format en temps réel
```bash
// static/js/aliment_form.js
document.addEventListener('DOMContentLoaded', function() {
    const codeAlimInput = document.getElementById('id_code_alim');
    if (codeAlimInput) {
        codeAlimInput.addEventListener('input', function(e) {
            this.value = this.value.toUpperCase().substring(0, 6);  // Majuscules + limite à 6
        });
    }
});
```
#### Template (⭐⭐)
- [ ] Améliorer l'affichage des erreurs et des help_text dans aliment_form.html:
```bash
<div class="form-group">
    <label for="{{ form.code_alim.id_for_label }}">{{ form.code_alim.label }}</label>
    {{ form.code_alim }}
    <small class="form-text text-muted">{{ form.code_alim.help_text }}</small>
    {% if form.code_alim.errors %}
        <div class="invalid-feedback d-block">
            {% for error in form.code_alim.errors %}
                {{ error }}
            {% endfor %}
        </div>
    {% endif %}
</div>
```

#### Tests(⭐)

- [ ] Ajouter des tests pour valider:
Les codes invalides (trop longs, caractères spéciaux)
Les fournisseurs inactifs
Les champs obligatoires

```bash
# tests.py
def test_code_alim_validation(self):
    form = AlimentForm(data={"code_alim": "abc!@#"})
    self.assertFalse(form.is_valid())
    self.assertIn("alphanumériques", str(form.errors))

class AlimentFormTest(TestCase):
    def test_code_alim_invalid(self):
        form = AlimentForm(data={"code_alim": "abcdefg"})  # Trop long
        self.assertFalse(form.is_valid())
```
