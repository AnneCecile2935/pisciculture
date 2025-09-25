## 9. **Source Code Management (SCM) and Quality Assurance (QA)**
## 9.1. SCM Strategy (Software Configuration Management)
### 9.1.1. Tools and Branching
- **Version Control**: Git + GitHub.
- **Branches**:
  - `main`: Production branch (stable).
  - `develop`: Integration branch for features.
  - `feature/[name]`: Development branches for each feature.
  - `release/[version]`: Version preparation.
  - `hotfix/[name]`: Urgent production fixes.

### 9.1.2. Workflow
1. Create a `feature/[name]` branch from `develop`.
2. Develop and commit regularly (clear, atomic commit messages).
3. Open a **Pull Request (PR)** to `develop` with:
   - A detailed description (GitHub template).
   - Self-review via checklist (see section 3).
4. Merge after passing tests and linting.

### 9.1.3. Automation Tools
- **Git Hooks**: `pre-commit` to run `flake8`, `black`, and `pytest` before each commit.
- **CI/CD**: GitHub Actions to validate PRs before merging.

## 9.2. QA Strategy (Quality Assurance)
### 9.2.1. Test Types
| Part     | Type               | Tool                 | Coverage                        |
|----------|--------------------|----------------------|---------------------------------|
| Backend  | Unit tests         | `pytest`             | Django models, views, utilities |
| Backend  | Integration tests  | `pytest`             | API endpoints, interactions     |
| Frontend | Unit tests         | `Jest`               | Pure JS functions               |
| Frontend | Integration tests  | `Jest` + `fetch-mock`| API calls, business logic       |

### 9.2.2. Linting Tools
- **Backend**: `flake8`, `black`, `isort`.
- **Frontend**: `ESLint`, `Prettier`.

### 9.2.3. Coverage
- **Backend**: `pytest-cov` (≥ 85% target).
- **Frontend**: `Jest --coverage` (≥ 80% target).

## 9.3. Code Review Process
### 9.3.1. Review Checklist
- Apply before each merge:
  - Code is clear, commented, and follows conventions.
  - Unit and integration tests pass.
  - Coverage is ≥ 80% (backend/frontend).
  - Documentation is updated.
  - No code duplication or unnecessary dependencies.

### 9.3.2. Pull Request Template
```bash
## Description
**Context**: [Why this change?]
**Changes**: [List of modifications]
**Tests**: [Added/modified tests and how to run them]
**Notes**: [Technical decisions, risks]

## Checklist
- [ ] Self-review completed.
- [ ] Local tests passed.
- [ ] Coverage verified.
- [ ] Documentation updated.

```

### 9.3.3. GitHub Tools

Pull Requests: Used even solo to structure changes.
GitHub Actions: Automatically runs tests and linting.
Codecov: Coverage reports integrated into PRs.

## 9.4. Technical Configuration
### 9.4.1. Backend (Django)
#### 		a. Dependencies
```bash
pip install pytest pytest-django pytest-cov flake8 black isort
```
#### 		b. Configuration Files


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

#### 		c. Integration Test Example

```bash
# apps/sites/tests/test_integration.py
@pytest.mark.django_db
def test_bassin_creation(client, user):
    client.force_login(user)
    response = client.post(reverse("bassins:create"), {"nom": "Bassin 1", "site": 1})
    assert response.status_code == 302
    assert Bassin.objects.filter(nom="Bassin 1").exists()
```

#### 		d.  Key Commands

```bash
# Lancer les tests avec coverage
pytest --cov=apps/sites --cov-report=xml
```

### 9.4.2. Frontend (JS Vanilla)

#### a. Dependencies

```bash
npm install --save-dev jest eslint eslint-config-prettier eslint-plugin-jest fetch-mock
```

#### b. Jest Configuration

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

#### c. Unit Test Example

```js
// tests/calculs.test.js
const { calculerQuantiteNourriture } = require("../src/calculs");

test("calcule la quantité de nourriture pour 100 poissons", () => {
  expect(calculerQuantiteNourriture(100)).toBe(2.5);
});
```

#### d.  Integration Test Example

```js
// tests/api.test.js
const { chargerBassins } = require("../src/api");

test("charge la liste des bassins", async () => {
  fetch.mockResponseOnce(JSON.stringify([{ id: 1, nom: "Bassin 1" }]));
  const bassins = await chargerBassins();
  expect(bassins).toEqual([{ id: 1, nom: "Bassin 1" }]);
});
```

#### e. ESLint Configuration

- `.eslintrc.js` :

  ```js
  module.exports = {
    env: { browser: true, jest: true },
    extends: ["eslint:recommended", "plugin:prettier/recommended"],
    rules: { "no-console": "warn" },
  };
  ```

#### f. Key Commands

```bash
# Lancer les tests avec coverage
npx jest --coverage
```

### 9.4.3. GitHub Actions

- **FiLE** : `.github/workflows/test_and_lint.yml`

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

## 9.5. Coverage and Reports

- **tOOLS** : [Codecov](https://codecov.io/gh/ton-org/pisciculture).

- **Badge** :

  ```bash
  [![codecov](https://codecov.io/gh/Annececile2935/pisciculture/branch/develop/graph/badge.svg)](https://codecov.io/gh/Annececile2935/pisciculture)
  ```

- **Thresholds** :

  - Backend : ≥ 85% (target), ≥ 80% (minimum).
  - Frontend : ≥ 80% (target, ≥ 75% (minimum).

------

## 9.6. Deployment

- Staging: Automatic deployment after test validation on develop.
- Production: Manual deployment after staging validation.

