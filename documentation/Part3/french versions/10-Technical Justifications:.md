## 10. **Justifications Techniques**

Ce projet utilise Django et JavaScript Vanilla pour offrir une solution légère mais robuste, avec des outils modernes (GitHub Actions, Codecov) pour garantir la qualité du code. L’architecture modulaire et les tests automatisés permettent une évolution sereine, tandis que les technologies choisies restent accessibles pour une débutante.

### **10.1. Backend : Django (Python)**

**Pourquoi Django ?**

- **Framework mature et complet** : Django fournit une structure prête à l’emploi pour les applications web (ORM, admin, sécurité, routage), ce qui accélère le développement et réduit les risques d’erreurs.
- **ORM intégré** : Permet de manipuler la base de données (PostgreSQL) en Python, sans écrire de SQL brut, tout en garantissant la sécurité contre les injections SQL.
- **Sécurité native** : Protection contre les failles courantes (CSRF, XSS, SQL injection) et gestion des utilisateurs/authentification intégrée.
- **Scalabilité** : Adapté aux applications évolutives grâce à son architecture modulaire (apps Django).
- **Écosystème riche** : Bibliothèques tierces pour étendre les fonctionnalités (ex. : `django-rest-framework` pour les APIs).

**Pourquoi PostgreSQL ?**

- **Base de données relationnelle** : Idéale pour les données structurées (sites, bassins, lots, nourrissages) avec des relations complexes.
- **Fiabilité et performances** : Support des transactions, requêtes avancées, et scalabilité.
- **Compatibilité** : Fonctionne parfaitement avec Django et Docker.

------

### 10.**2. Frontend : JavaScript Vanilla**

**Pourquoi pas de framework (React/Vue) ?**

- **Simplicité** : Le projet initial se concentre sur des fonctionnalités basiques (formulaires, affichage de données). Vanilla JS suffit pour éviter une surcharge inutile.
- **Légèreté** : Pas de dépendances lourdes à gérer, ce qui simplifie le déploiement et la maintenance.
- **Apprentissage** : Permet de maîtriser les fondamentaux (DOM, `fetch`, événements) avant d’adopter un framework si besoin.

**Évolutivité** :

- Si le projet grandit, migration possible vers React/Vue sans refactorisation majeure (grâce à une architecture modulaire en JS).

------

### 10.**3. Tests : Pytest (Backend) + Jest (Frontend)**

**Pourquoi Pytest ?**

- **Intégration native avec Django** : Fixtures pour les tests de base de données, plugins dédiés (`pytest-django`).
- **Syntax concise** : Plus lisible que `unittest`, avec des rapports de coverage intégrés (`pytest-cov`).

**Pourquoi Jest ?**

- **Standard pour le JS** : Outil le plus populaire pour tester du JavaScript, avec support des mocks (ex. : `fetch-mock`) et des environnements DOM simulés (`jsdom`).
- **Coverage intégré** : Génère des rapports détaillés pour identifier les parties non testées.

**Pourquoi séparer les tests backend/frontend ?**

- **Isolation des responsabilités** : Les tests backend vérifient la logique serveur (Python), tandis que les tests frontend valident l’interface utilisateur (JS).
- **Environnements différents** : Python s’exécute côté serveur, JS côté navigateur.

------

### **10.4. SCM : Git + GitHub**

**Pourquoi Git ?**

- **Standard industriel** : Outil de versioning le plus utilisé, avec un écosystème riche (GitHub, GitLab).
- **Branching flexible** : Permet de travailler sur des fonctionnalités en parallèle (`feature/*`) sans bloquer la branche principale.

**Pourquoi GitHub ?**

- **Intégration CI/CD** : GitHub Actions permet d’automatiser les tests et le déploiement sans serveur externe.
- **Collaboration** : Même en solo, les PR et les issues aident à structurer le travail.

**Branching strategy** :

- `main`/`develop` : Séparation claire entre code stable et en développement.
- `feature/*` : Isoler les nouvelles fonctionnalités pour éviter les conflits.

------

### **10.5. CI/CD : GitHub Actions**

**Pourquoi GitHub Actions ?**

- **Intégration native** : Pas besoin de configurer un outil externe (ex. : Jenkins, Travis CI).
- **Gratuit pour les dépôts publics** : Idéal pour un projet open-source ou académique.
- **Workflows simples** : Déclenchement automatique des tests à chaque PR, avec feedback visuel (✅/❌).

**Pourquoi Codecov ?**

- **Visualisation du coverage** : Badge dans le README pour suivre la qualité des tests en un coup d’œil.
- **Seuils configurables** : Oblige à maintenir un coverage minimum (ex. : 80%).

------

### 10.**6. Linting et Formatage**

**Backend : Flake8 + Black**

- **Flake8** : Détecte les erreurs de style (PEP 8) et les bugs potentiels.
- **Black** : Formatte automatiquement le code pour une cohérence d’équipe (même en solo).

**Frontend : ESLint + Prettier**

- **ESLint** : Applique des règles de qualité (ex. : éviter `console.log` en production).
- **Prettier** : Formatte le code JS de manière uniforme.

**Pourquoi automatiser le linting ?**

- **Qualité constante** : Évite les erreurs basiques et uniforme le style.
- **Gain de temps** : Exécuté automatiquement via `pre-commit` et GitHub Actions.

------

### **10.7. Docker

**Pourquoi Docker ?**

- **Environnement reproductible** : Évite les problèmes de "ça marche chez moi" en containerisant l’application (PostgreSQL, Django, dépendances).
- **Déploiement simplifié** : Un fichier `docker-compose.yml` suffit pour lancer l’app localement ou en production.

**Alternative** :

- Si Docker n’est pas utilisé, documenter clairement les dépendances (ex. : versions de Python, Node.js, PostgreSQL).

------

### 10.**8. Architecture Modulaire

**Pourquoi séparer en apps (`sites`, `stocks`, `activité_quotidien`) ?**

- **Séparation des concerns** : Chaque app gère un domaine métier spécifique (ex. : `sites` pour les bassins, `stocks` pour les poissons/aliments).
- **Réutilisabilité** : Une app peut être réutilisée dans d’autres projets.
- **Maintenabilité** : Plus facile à déboguer et à faire évoluer.

**Exemple** :

- `sites/` : Gère les sites et bassins.
- `activité_quotidien/` : Gère les nourrissages, relevés de température, etc.

Voici une section **"Technical Justifications"** claire et structurée pour ton projet, expliquant les choix technologiques et architecturaux. Tu peux l’ajouter directement à ta documentation.



### **10.9. Choix des Technologies par Rapport aux Exigences**

| Exigence                        | Technologie Choisie        | Justification                                                |
| ------------------------------- | -------------------------- | ------------------------------------------------------------ |
| Gestion des utilisateurs/rôles  | Django Auth                | Système d’authentification sécurisé et personnalisable (admin/utilisateur). |
| Enregistrement des nourrissages | Django Models + PostgreSQL | Stockage structuré des données avec historique et relations. |
| Responsivité                    | CSS Vanilla ou Bootstrap   | Bootstrap accélère le développement si besoin, sinon CSS pur pour plus de contrôle. |
| Accessibilité                   | HTML5 semantique + ARIA    | Respect des standards W3C pour les utilisateurs handicapés.  |

### 10.**10. Alternatives Envisagées et Écarts**

- **Frontend** :
  - **Alternative** : React/Vue pour une interface plus dynamique.
  - **Écart** : Vanilla JS choisi pour éviter la complexité initiale, avec possibilité de migration ultérieure.
- **Backend** :
  - **Alternative** : FastAPI pour une API plus légère.
  - **Écart** : Django préféré pour son admin intégré et sa maturité.
- **Base de données** :
  - **Alternative** : SQLite pour un prototype rapide.
  - **Écart** : PostgreSQL choisi pour sa robustesse et son support des requêtes complexes.

### **10.11. Justification des Outils de Tests**

| Outil        | Alternative | Pourquoi ce choix ?                                          |
| ------------ | ----------- | ------------------------------------------------------------ |
| `pytest`     | `unittest`  | Syntax plus concise et plugins dédiés à Django.              |
| `Jest`       | `Mocha`     | Intégration plus simple avec les mocks et le coverage.       |
| `fetch-mock` | `nock`      | Plus léger et adapté à `fetch` (utilisé en JS vanilla).      |
| Codecov      | Coveralls   | Intégration plus fluide avec GitHub et rapports plus clairs. |

### 10.**12. Perspectives d’Évolution**

- **Frontend** : Migration vers React si l’interface devient complexe (ex. : tableaux dynamiques, graphiques).
- **Backend** : Ajout de `django-rest-framework` pour une API plus puissante si besoin de mobile.
