## 10. **Technical Justifications**
This project uses Django and Vanilla JavaScript to provide a lightweight yet robust solution, with modern tools (GitHub Actions, Codecov) to ensure code quality. The modular architecture and automated tests enable smooth evolution while keeping the technologies accessible for a beginner.

### **10.1. Backend: Django (Python)**
**Why Django?**
- **Mature and complete framework**: Django provides a ready-to-use structure for web applications (ORM, admin, security, routing), accelerating development and reducing error risks.
- **Built-in ORM**: Allows database (PostgreSQL) manipulation in Python without raw SQL, while ensuring protection against SQL injections.
- **Native security**: Protection against common vulnerabilities (CSRF, XSS, SQL injection) with integrated user/authentication management.
- **Scalability**: Suitable for evolving applications thanks to its modular architecture (Django apps).
- **Rich ecosystem**: Third-party libraries to extend functionality (e.g., `django-rest-framework` for APIs).

**Why PostgreSQL?**
- **Relational database**: Ideal for structured data (sites, ponds, batches, feedings) with complex relationships.
- **Reliability and performance**: Supports transactions, advanced queries, and scalability.
- **Compatibility**: Works perfectly with Django and Docker.

------
### **10.2. Frontend: Vanilla JavaScript**
**Why no framework (React/Vue)?**
- **Simplicity**: The initial project focuses on basic features (forms, data display). Vanilla JS is sufficient to avoid unnecessary overhead.
- **Lightweight**: No heavy dependencies to manage, simplifying deployment and maintenance.
- **Learning curve**: Mastering fundamentals (DOM, `fetch`, events) before adopting a framework if needed.

**Scalability**:
- If the project grows, migration to React/Vue is possible without major refactoring (thanks to modular JS architecture).

------
### **10.3. Testing: Pytest (Backend) + Jest (Frontend)**
**Why Pytest?**
- **Native Django integration**: Fixtures for database testing, dedicated plugins (`pytest-django`).
- **Concise syntax**: More readable than `unittest`, with built-in coverage reports (`pytest-cov`).

**Why Jest?**
- **JS standard**: Most popular tool for testing JavaScript, with mock support (e.g., `fetch-mock`) and simulated DOM environments (`jsdom`).
- **Built-in coverage**: Generates detailed reports to identify untested parts.

**Why separate backend/frontend tests?**
- **Separation of concerns**: Backend tests verify server logic (Python), while frontend tests validate the user interface (JS).
- **Different environments**: Python runs server-side, JS runs in the browser.

------
### **10.4. SCM: Git + GitHub**
**Why Git?**
- **Industry standard**: Most widely used version control tool, with a rich ecosystem (GitHub, GitLab).
- **Flexible branching**: Allows parallel feature development (`feature/*`) without blocking the main branch.

**Why GitHub?**
- **CI/CD integration**: GitHub Actions automates tests and deployment without external servers.
- **Collaboration**: Even solo, PRs and issues help structure work.

**Branching strategy**:
- `main`/`develop`: Clear separation between stable and development code.
- `feature/*`: Isolates new features to avoid conflicts.

------
### **10.5. CI/CD: GitHub Actions**
**Why GitHub Actions?**
- **Native integration**: No need for external tools (e.g., Jenkins, Travis CI).
- **Free for public repos**: Ideal for open-source or academic projects.
- **Simple workflows**: Automatic test triggering on each PR, with visual feedback (✅/❌).

**Why Codecov?**
- **Coverage visualization**: Badge in README to track test quality at a glance.
- **Configurable thresholds**: Enforces minimum coverage (e.g., 80%).

------
### **10.6. Linting and Formatting**
**Backend: Flake8 + Black**
- **Flake8**: Detects style errors (PEP 8) and potential bugs.
- **Black**: Automatically formats code for team consistency (even solo).

**Frontend: ESLint + Prettier**
- **ESLint**: Enforces quality rules (e.g., avoid `console.log` in production).
- **Prettier**: Uniformly formats JS code.

**Why automate linting?**
- **Consistent quality**: Avoids basic errors and enforces style uniformity.
- **Time savings**: Executed automatically via `pre-commit` and GitHub Actions.

------
### **10.7. Docker**
**Why Docker?**
- **Reproducible environment**: Avoids "works on my machine" issues by containerizing the app (PostgreSQL, Django, dependencies).
- **Simplified deployment**: A single `docker-compose.yml` file suffices to run the app locally or in production.

**Alternative**:
- If Docker isn't used, clearly document dependencies (e.g., Python, Node.js, PostgreSQL versions).

------
### **10.8. Modular Architecture**
**Why separate into apps (`sites`, `stocks`, `daily_activity`)?**
- **Separation of concerns**: Each app handles a specific business domain (e.g., `sites` for ponds, `stocks` for fish/food).
- **Reusability**: An app can be reused in other projects.
- **Maintainability**: Easier to debug and evolve.

**Example**:
- `sites/`: Manages sites and ponds.
- `daily_activity/`: Manages feedings, temperature readings, etc.

------
### **10.9. Technology Choices vs. Requirements**

| Requirement                     | Chosen Technology       | Justification                                              |
|---------------------------------|--------------------------|------------------------------------------------------------|
| User/role management            | Django Auth              | Secure and customizable authentication system (admin/user). |
| Feeding records                 | Django Models + PostgreSQL | Structured data storage with history and relationships.    |
| Responsiveness                  | Vanilla CSS or Bootstrap | Bootstrap speeds development if needed; otherwise pure CSS for more control. |
| Accessibility                   | Semantic HTML5 + ARIA    | Compliance with W3C standards for disabled users.          |

### **10.10. Considered Alternatives and Deviations**

| Area       | Alternative       | Why this choice?                                           |
|------------|-------------------|------------------------------------------------------------|
| Frontend   | React/Vue         | Vanilla JS chosen to avoid initial complexity, with future migration possibility. |
| Backend    | FastAPI           | Django preferred for its built-in admin and maturity.      |
| Database   | SQLite            | PostgreSQL chosen for robustness and complex query support.|

### **10.11. Testing Tools Justification**

| Tool         | Alternative | Why this choice?                                          |
|--------------|--------------|-----------------------------------------------------------|
| `pytest`     | `unittest`   | More concise syntax and Django-specific plugins.          |
| `Jest`       | `Mocha`      | Simpler integration with mocks and coverage.              |
| `fetch-mock` | `nock`       | Lighter and better suited for `fetch` (used in vanilla JS).|
| Codecov      | Coveralls    | Smoother GitHub integration and clearer reports.          |

### **10.12. Evolution Perspectives**
- **Frontend**: Migration to React if the interface becomes complex (e.g., dynamic tables, charts).
- **Backend**: Add `django-rest-framework` for a more powerful API if mobile support is needed.
