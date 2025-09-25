## 6. **Gestion du Code Source (SCM) et Qualité (QA)**

## 	6.1. Stratégie SCM (Software Configuration Management)

### 		6.1.1. Outils et Branching

- **Outil de versioning** : Git + GitHub.
- **Branches** :
  - `main` : Branche de production (stable).
  - `develop` : Branche d’intégration des fonctionnalités.
  - `feature/[nom]` : Branches de développement pour chaque fonctionnalité.
  - `release/[version]` : Préparation des versions.
  - `hotfix/[nom]` : Corrections urgentes en production.

### 		6.1.2. Workflow

1. Créer une branche `feature/[nom]` depuis `develop`.
2. Développer et commiter régulièrement (messages clairs et atomiques).
3. Ouvrir une **Pull Request (PR)** vers `develop` avec :
   - Une description détaillée (template GitHub).
   - Une auto-revue via checklist (voir section 3).
4. Fusionner après validation des tests et du linting.

### 		6.1.3. Outils d’Automatisation

- **Hooks Git** : `pre-commit` pour exécuter `flake8`, `black`, et `pytest` avant chaque commit.

- **CI/CD** : GitHub Actions pour valider les PR avant fusion.

  ## 6.2. Stratégie QA (Assurance Qualité)

  ### 	6.2.1. Types de Tests

  | Partie   | Type                | Outil                 | Couverture                        |
  | -------- | ------------------- | --------------------- | --------------------------------- |
  | Backend  | Tests unitaires     | `pytest`              | Modèles, vues, utilitaires Django |
  | Backend  | Tests d’intégration | `pytest`              | Endpoints API, interactions       |
  | Frontend | Tests unitaires     | `Jest`                | Fonctions JS pures                |
  | Frontend | Tests d’intégration | `Jest` + `fetch-mock` | Appels API, logique métier        |

### 	6.2.2. Outils de Linting

- **Backend** : `flake8`, `black`, `isort`.

- **Frontend** : `ESLint`, `Prettier`.

  ### 6.2.3. Coverage

  - **Backend** : `pytest-cov` (≥ 85% visé).
  - **Frontend** : `Jest --coverage` (≥ 80% visé).

## 	6.3. Processus de Revue de Code

### 		6.3.1. Checklist de Revue

- À appliquer avant chaque fusion :
  -  Le code est clair, commenté et respecte les conventions.
  -  Les tests unitaires et d’intégration passent.
  -  Le coverage est ≥ 80% (backend) / ≥ 80% (frontend).
  -  La documentation est mise à jour.
  -  Aucune duplication de code ou dépendance inutile.

### 		6.3.2. Template de Pull Request

```bash
 ## Description
**Contexte** : [Pourquoi cette modification ?]
**Modifications** : [Liste des changements]
**Tests** : [Tests ajoutés/modifiés et comment les exécuter]
**Points d’attention** : [Décisions techniques, risques]

## Checklist
- [ ] Auto-revue effectuée.
- [ ] Tests locaux passés.
- [ ] Coverage vérifié.
- [ ] Documentation mise à jour.

```

### 		6.3.3. Outils GitHub

- **Pull Requests** : Utilisées même en solo pour structurer les changements.
- **GitHub Actions** : Exécute automatiquement les tests et le linting.
- **Codecov** : Rapport de coverage intégré aux PR.



## 6.4. Configuration Technique

### 	6.4.1. Backend (Django)

#### 		a. Dépendances

```bash
pip install pytest pytest-django pytest-cov flake8 black isort
```

#### 		b. Fichiers de Configuration

- `.pre-commit-config.yaml` :

  ```yaml
  repos:
    - repo: https://github.com/psf/black
      rev: 23.12.1
      hooks:
        - id: black
    - repo: https://github.com/PyCQA/flake8
      rev: 6.1.0
      hooks:
        - id: flake8
  ```

- `pytest.ini` :

  ```ini
  [pytest]
  DJANGO_SETTINGS_MODULE = core.settings
  python_files = tests.py test_*.py *_tests.py
  ```

#### 		c. Exemple de Test d’Intégration

```bash
# apps/sites/tests/test_integration.py
@pytest.mark.django_db
def test_bassin_creation(client, user):
    client.force_login(user)
    response = client.post(reverse("bassins:create"), {"nom": "Bassin 1", "site": 1})
    assert response.status_code == 302
    assert Bassin.objects.filter(nom="Bassin 1").exists()
```

#### 		d. Commandes Clés

```bash
# Lancer les tests avec coverage
pytest --cov=apps/sites --cov-report=xml
```

### 6.4.2. Frontend (JS Vanilla)

#### a. Dépendances

```bash
npm install --save-dev jest eslint eslint-config-prettier eslint-plugin-jest fetch-mock
```

#### b. Configuration de Jest

- `jest.config.js` :

  ```js
  module.exports = {
    testEnvironment: "jsdom",
    setupFilesAfterEnv: ["./tests/setup.js"],
    coverageReporters: ["text", "lcov"],
  };
  ```

- `tests/setup.js` :

  ```js
  require("fetch-mock").mock();
  ```

#### c. Exemple de Test Unitaire

```js
// tests/calculs.test.js
const { calculerQuantiteNourriture } = require("../src/calculs");

test("calcule la quantité de nourriture pour 100 poissons", () => {
  expect(calculerQuantiteNourriture(100)).toBe(2.5);
});
```

#### d. Exemple de Test d’Intégration

```js
// tests/api.test.js
const { chargerBassins } = require("../src/api");

test("charge la liste des bassins", async () => {
  fetch.mockResponseOnce(JSON.stringify([{ id: 1, nom: "Bassin 1" }]));
  const bassins = await chargerBassins();
  expect(bassins).toEqual([{ id: 1, nom: "Bassin 1" }]);
});
```

#### e. Configuration d’ESLint

- `.eslintrc.js` :

  ```js
  module.exports = {
    env: { browser: true, jest: true },
    extends: ["eslint:recommended", "plugin:prettier/recommended"],
    rules: { "no-console": "warn" },
  };
  ```

#### f. Commandes Clés

```bash
# Lancer les tests avec coverage
npx jest --coverage
```

### 6.4.3. GitHub Actions

- **Fichier** : `.github/workflows/test_and_lint.yml`

  ```yaml
  name: Test and Lint
  on: [pull_request]

  jobs:
    test_backend:
      runs-on: ubuntu-latest
      services:
        postgres:
          image: postgres:15
          env:
            POSTGRES_PASSWORD: postgres
          ports: ["5432:5432"]
      steps:
        - uses: actions/checkout@v4
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: "3.11"
        - name: Install dependencies
          run: pip install -r requirements.txt
        - name: Run linting
          run: |
            pip install flake8 black
            flake8 .
            black --check .
        - name: Run tests with coverage
          env:
            DATABASE_URL: postgres://postgres:postgres@localhost:5432/pisciculture_test
          run: pytest --cov=apps/sites --cov-report=xml
        - name: Upload coverage
          uses: codecov/codecov-action@v4
          with:
            token: ${{ secrets.CODECOV_TOKEN }}
            file: ./coverage.xml

    test_frontend:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Set up Node.js
          uses: actions/setup-node@v4
          with:
            node-version: 20
        - name: Install dependencies
          run: npm ci
        - name: Run linting
          run: npx eslint . --fix
        - name: Run frontend tests
          run: npx jest --coverage
        - name: Upload frontend coverage
          uses: codecov/codecov-action@v4
          with:
            token: ${{ secrets.CODECOV_TOKEN }}
            file: ./coverage/lcov.info
  ```

------

## 6.5. Coverage et Rapports

- **Outil** : [Codecov](https://codecov.io/gh/ton-org/pisciculture).

- **Badge** :

  ```bash
  [![codecov](https://codecov.io/gh/Annececile2935/pisciculture/branch/develop/graph/badge.svg)](https://codecov.io/gh/Annececile2935/pisciculture)
  ```

- **Seuils** :

  - Backend : ≥ 85% (visé), ≥ 80% (minimum).
  - Frontend : ≥ 80% (visé), ≥ 75% (minimum).

------

## 6.6. Déploiement

- **Staging** : Déploiement automatique après validation des tests sur `develop`.
- **Production** : Déploiement manuel après validation en staging.
