# **Rétrospective Complète – Projet Pisciculture (MVP)**
*Contexte* : Développement d’une application web pour la gestion de piscicultures, incluant le suivi des nourrissages, la gestion des sites/bassins, et des tableaux de bord analytiques. Projet réalisé en **4 sprints** (2025-09-01 → 2025-11-01) avec Django, PostgreSQL, et Docker.

---

## **📌 Bilan Global du Projet**
   **Aspect**               | **Réalisations**                                                                                     | **Preuves**                                                                                     |
 |--------------------------|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
 | **Fonctionnalités**      | 100% des modèles (Site, Bassin, Nourrissage, etc.), formulaires dynamiques, et dashboard analytique. |
 | **Tests**                | 94% de couverture (232/249 tests passés), tests unitaires et d’intégration.                        |                |
 | **Infrastructure**       | Dockerisé (services `db`, `db_test`, `web`, `test`), CI/CD prêt pour GitHub Actions.               | [docker-compose.yml](lien_vers_fichier)                                                        |
 | **Documentation**       | Journal de développement, rétrospectives par sprint, et documentation technique.                  |                                                         |

---

## **✅ Succès Majeurs**
### **1. Architecture Modulaire et Scalable**
- **Réalisations** :
  - **Séparation claire des apps Django** (`sites`, `activite_quotidien`, `stocks`, etc.) avec des dépendances minimales.
  - **Modèles bien conçus** (ex: `Nourrissage` avec relations ForeignKey vers `Bassin` et `Aliment`).
  - **Utilisation de `factory_boy`** pour générer des données de test réalistes.
- **Preuves** :
  - [Structure des apps](https://github.com/AnneCecile2935/pisciculture/tree/main/app_pisci/apps)
  - [Modèle Nourrissage](https://github.com/AnneCecile2935/pisciculture/blob/main/app_pisci/apps/activite_quotidien/models.py)

### **2. Intégration de DataTables**
- **Réalisations** :
  - Toutes les listes (nourrissages, aliments, espèces) sont **dynamiques** (tri, pagination, recherche).
  - **Optimisation des requêtes** avec `select_related` pour éviter les N+1 queries.
- **Preuves** :
  - [Commit DataTables](https://github.com/AnneCecile2935/pisciculture/commit/868d3af)

### **3. Dashboard Analytique**
- **Réalisations** :
  - **3 graphiques** (Chart.js) :
    - Nourrissages par site (barres).
    - Température moyenne (ligne).
    - Mortalité (camembert).
  - **API dédiée** (`/api/dashboard/data/`) pour alimenter les graphiques.
- **Preuves** :
  - [Code du dashboard](https://github.com/AnneCecile2935/pisciculture/blob/main/app_pisci/templates/dashboard.html)



---

## **⚠️ Défis et Solutions**
 | **Défi**                          | **Cause**                                  | **Solution**                                                                                     | **Leçon Apprise**                                                                                     |
 |-----------------------------------|--------------------------------------------|------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
 | **Conflits de migration**         | Modifications fréquentes des modèles.      | Utilisation de `python manage.py makemigrations --merge` et réinitialisation des migrations.     | Toujours **versionner les migrations** et éviter les modifications après un `makemigrations`.     |
 | **Base de test non créée**         | Mauvaise configuration Docker/PostgreSQL.  | Ajout d’un `healthcheck` et création manuelle de l’utilisateur `test_user`.                  | Vérifier les **permissions PostgreSQL** et les `healthchecks` dans `docker-compose.yml`.           |
 | **17 tests en échec**             | Validations manquantes dans les formulaires. | Ajout de `MinValueValidator` et correction des templates (`esp_confirm_delete.html`).         | **Prioriser les tests de formulaire** dès le début du sprint.                                        |
 | **Sous-estimation du temps**       | Complexité du dashboard (Chart.js).        | Découpage en sous-tâches (backend API → frontend).                                              | Ajouter **20% de marge** pour les tâches front-end complexes.                                      |

---

## **🎯 Leçons Apprises**
### **1. Tests**
- **Prioriser les tests de formulaire** :
  - Les validations (ex: quantité > 0) doivent être **testées en premier**.
- **Automatiser les tests** :
  - Configurer **GitHub Actions** pour exécuter les tests à chaque push.
  - *Exemple de workflow* :
    ```yaml
    name: Tests
    on: [push]
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - run: pip install -r requirements-test.txt
          - run: pytest --cov=app_pisci --cov-report=xml
    ```

### **2. Docker et PostgreSQL**
- **Séparer les environnements** :
  - Utiliser des **services Docker distincts** (`db` vs `db_test`).
  - **Noms de bases différents** (`pisciculture` vs `pisciculture_test`).
- **Healthchecks** :
  - Toujours ajouter un `healthcheck` pour les services de base de données.
  - *Exemple* :
    ```yaml
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    ```

### **3. Front-end (Chart.js, DataTables)**
- **Découper les tâches** :
  - Commencer par le **backend** (API pour les données) avant le frontend.
  - *Exemple* :
    ```python
    # views.py
    def dashboard_data(request):
        data = {
            'nourrissages': list(Nourrissage.objects.values('site__nom').annotate(total=Count('id')))
        }
        return JsonResponse(data)
    ```
- **Optimiser les performances** :
  - Utiliser `select_related` pour éviter les requêtes N+1.
  - *Exemple* :
    ```python
    Nourrissage.objects.select_related('site', 'aliment').all()
    ```

### **4. Gestion de Projet**
- **Estimer réalistement** :
  - Ajouter **20% de marge** pour les tâches front-end ou complexes.
  - *Exemple* :
 | Tâche               | Estimation Initiale | Estimation Révisée |
 |----------------------|---------------------|--------------------|
 | Dashboard            | 1 jour               | 1.2 jours          |
- **Rétrospectives** :
  - Toujours inclure :
    - **3 succès** (avec preuves).
    - **3 défis** (avec solutions).
    - **3 actions SMART** pour le prochain sprint.

---

## **📊 Métriques Clés du Projet**
 | **Métrique**               | **Valeur**       | **Commentaire**                                                                 |
 |-----------------------------|------------------|---------------------------------------------------------------------------------|
 | **Vélocité moyenne**        | 10/10 tâches    | Amélioration progressive (Sprint 1: 7/10 → Sprint 4: 10/10).                   |
 | **Couverture de tests**      | 94%              | 17 tests à corriger (liés aux faites sur les formulaires).                                     |
 | **Temps passé vs. prévu**    | +12%             | Principalement dû au dashboard et aux tests.                                   |
 | **Bugs résolus**            | 100% (4/4)       | Tous les bugs critiques corrigés.                                             |
 | **Tâches reportées**        | 2/7              | Seules les tâches P2 reportées (ex: bouton "Annuler").                         |

---

## **🎯 Actions pour la Suite (Post-MVP)**
 | **Action**                          | **Priorité** | **Échéance**   | **Critère de Succès**                          |
 |-------------------------------------|--------------|----------------|-----------------------------------------------|
 | **Corriger les 17 tests restants**  | Haute         | 2025-11-05     | 100% des tests passent (`pytest --cov`).      |
 | **Automatiser les tests (CI/CD)**   | Haute         | 2025-11-10     | Workflow GitHub Actions fonctionnel.         |
 | **Modification et séparation création lot et création stock** | Moyenne       | 2025-11-15     | ON peut créer un stock de poisson indépendamment de la création d'un lot |
 | **Implémenter le stock en bassin**         | Moyenne       | 2025-11-20     | Pouvoir gérer et consulter le stock en bassin |
 | **Implémenter fonctionnalité Mortalité et poids moyen pour livrer l'application**         | Moyenne       | 2025-11-20     | Pouvoir enregistrer mortalité et suivre la croissance des poissons |


---

## **📎 Preuves et Liens**
### **1. Code Source**
- [Dépôt GitHub](https://github.com/AnneCecile2935/pisciculture)
- [Commits clés](https://github.com/AnneCecile2935/pisciculture/commits) :
  - [Intégration DataTables](https://github.com/AnneCecile2935/pisciculture/commit/868d3af)
  - [Dashboard](https://github.com/AnneCecile2935/pisciculture/commit/)

### **2. Captures d’Écran**
- [DataTables](lien_vers_capture_datatables.png)
- [Dashboard](lien_vers_capture_dashboard.png)
- [Formulaire global](lien_vers_capture_formulaire.png)


---

## **💡 Recommandations pour la Suite**
1. **Améliorations Techniques** :
   - **Cache** : Utiliser `django-redis` pour mettre en cache les requêtes fréquentes (ex: listes DataTables).
   - **Sécurité** : Ajouter des tests de sécurité (ex: `django-security`).

2. **Déploiement** :
   - **Conteneurisation** : Utiliser `docker-compose.prod.yml` pour la production.
   - **CI/CD** : Configurer un pipeline de déploiement automatique (ex: GitHub Actions + Heroku).

3. **Fonctionnalités Futures** :
   - **Mobile** : Adapter l’interface pour les appareils mobiles (Bootstrap 5).
   - **Météo** : Appeler une API météo pour avoir les prévisions directement sur l'application
   - **Prévisions** : Intégrer des modèles de ML pour prédire la croissance des poissons.

---
