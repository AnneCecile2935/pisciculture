# **Complete Retrospective – Pisciculture Project (MVP)**
*Context*: Development of a web application for fish farm management, including feeding tracking, site/pond management, and analytical dashboards. Project completed in **4 sprints** (2025-09-01 → 2025-11-01) using Django, PostgreSQL, and Docker.

---
## **📌 Project Overview**
   **Aspect**               | **Achievements**                                                                                     | **Evidence**                                                                                     |
 |--------------------------|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
 | **Features**             | 100% of models (Site, Pond, Feeding, etc.), dynamic forms, and analytical dashboard.                  |                                                                                                |
 | **Tests**                | 94% coverage (232/249 tests passed), unit and integration tests.                                   |                                                                                                |
 | **Infrastructure**       | Dockerized (services: `db`, `db_test`, `web`, `test`), ready for GitHub Actions CI/CD.             | [docker-compose.yml](link_to_file)                                                              |
 | **Documentation**        | Development log, sprint retrospectives, and technical documentation.                              |                                                                                                |

---
## **✅ Major Successes**
### **1. Modular and Scalable Architecture**
- **Achievements**:
  - Clear separation of Django apps (`sites`, `daily_activity`, `stocks`, etc.) with minimal dependencies.
  - Well-designed models (e.g., `Feeding` with ForeignKey relationships to `Pond` and `Feed`).
  - Use of `factory_boy` for generating realistic test data.
- **Evidence**:
  - [App structure](https://github.com/AnneCecile2935/pisciculture/tree/main/app_pisci/apps)
  - [Feeding model](https://github.com/AnneCecile2935/pisciculture/blob/main/app_pisci/apps/daily_activity/models.py)

### **2. DataTables Integration**
- **Achievements**:
  - All lists (feedings, feeds, species) are dynamic (sorting, pagination, search).
  - Query optimization with `select_related` to avoid N+1 queries.
- **Evidence**:
  - [DataTables commit](https://github.com/AnneCecile2935/pisciculture/commit/868d3af)

### **3. Analytical Dashboard**
- **Achievements**:
  - **3 charts** (Chart.js):
    - Feedings per site (bar chart).
    - Average temperature (line chart).
    - Mortality (pie chart).
  - Dedicated API (`/api/dashboard/data/`) to feed the charts.
- **Evidence**:
  - [Dashboard code](https://github.com/AnneCecile2935/pisciculture/blob/main/app_pisci/templates/dashboard.html)

---
## **⚠️ Challenges and Solutions**
 | **Challenge**                     | **Cause**                                  | **Solution**                                                                                     | **Lesson Learned**                                                                                     |
 |-----------------------------------|--------------------------------------------|------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
 | **Migration conflicts**           | Frequent model changes                     | Used `python manage.py makemigrations --merge` and migration reset.                            | Always version migrations and avoid changes after `makemigrations`.                                |
 | **Test database not created**     | Incorrect Docker/PostgreSQL configuration  | Added `healthcheck` and manually created `test_user`.                                           | Verify PostgreSQL permissions and `healthchecks` in `docker-compose.yml`.                           |
 | **17 failing tests**              | Missing form validations                   | Added `MinValueValidator` and fixed missing templates (`esp_confirm_delete.html`).              | Prioritize form tests early in the sprint.                                                            |
 | **Time underestimation**          | Dashboard complexity (Chart.js)             | Broke into subtasks (backend API → frontend).                                                   | Add 20% buffer for complex frontend tasks.                                                          |

---
## **🎯 Lessons Learned**
### **1. Testing**
- **Prioritize form tests**:
  - Validations (e.g., quantity > 0) should be tested first.
- **Automate tests**:
  - Set up GitHub Actions to run tests on every push.
  - *Example workflow*:
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

### **2. Docker and PostgreSQL**
- **Separate environments**:
  - Use distinct Docker services (`db` vs `db_test`).
  - Different database names (`pisciculture` vs `pisciculture_test`).
- **Healthchecks**:
  - Always add healthchecks for database services.
  - *Example*:
    ```yaml
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    ```

### **3. Frontend (Chart.js, DataTables)**
- **Break down tasks**:
  - Start with backend (API for data) before frontend.
  - *Example*:
    ```python
    # views.py
    def dashboard_data(request):
        data = {
            'feedings': list(Feeding.objects.values('site__name').annotate(total=Count('id')))
        }
        return JsonResponse(data)
    ```
- **Optimize performance**:
  - Use `select_related` to avoid N+1 queries.
  - *Example*:
    ```python
    Feeding.objects.select_related('pond', 'feed').all()
    ```

### **4. Project Management**
- **Realistic estimation**:
  - Add 20% buffer for complex frontend tasks.
  - *Example*:
 | Task               | Initial Estimate | Revised Estimate |
 |--------------------|-------------------|------------------|
 | Dashboard          | 1 day             | 1.2 days         |
- **Retrospectives**:
  - Always include:
    - 3 successes (with evidence).
    - 3 challenges (with solutions).
    - 3 SMART actions for the next sprint.

---
## **📊 Key Project Metrics**
 | **Metric**               | **Value**       | **Comment**                                                                 |
 |--------------------------|-----------------|-----------------------------------------------------------------------------|
 | **Average velocity**      | 10/10 tasks     | Progressive improvement (Sprint 1: 7/10 → Sprint 4: 10/10).                |
 | **Test coverage**        | 94%             | 17 tests remaining (form-related).                                          |
 | **Time vs. estimate**    | +12%            | Mainly due to dashboard and tests.                                         |
 | **Bugs resolved**        | 100% (4/4)      | All critical bugs fixed.                                                   |
 | **Deferred tasks**       | 2/7             | Only P2 tasks deferred (e.g., "Cancel" button).                           |

---
## **🎯 Next Steps (Post-MVP)**
 | **Action**                              | **Priority** | **Deadline**   | **Success Criteria**                          |
 |-----------------------------------------|--------------|----------------|-----------------------------------------------|
 | **Fix remaining 17 tests**              | High         | 2025-11-05     | 100% test passing (`pytest --cov`).           |
 | **Automate tests (CI/CD)**              | High         | 2025-11-10     | Functional GitHub Actions workflow.           |
 | **Modify and separate batch and stock creation** | Medium       | 2025-11-15     | Ability to create fish stock independently of batch creation. |
 | **Implement pond stock**                | Medium       | 2025-11-20     | Ability to manage and view pond stock.        |
 | **Implement mortality and average weight functionality** | Medium       | 2025-11-20     | Ability to record mortality and track fish growth. |

---
## **📎 Evidence and Links**
### **1. Source Code**
- [GitHub Repository](https://github.com/AnneCecile2935/pisciculture)
- **Key commits**:
  - [DataTables integration](https://github.com/AnneCecile2935/pisciculture/commit/868d3af)
  - [Dashboard implementation](https://github.com/AnneCecile2935/pisciculture/commit/)

### **2. Screenshots**
- [DataTables](link_to_datatables_screenshot.png)
- [Dashboard](link_to_dashboard_screenshot.png)
- [Global form](link_to_global_form_screenshot.png)

---
## **💡 Recommendations for Future Development**
1. **Technical Improvements**:
   - **Caching**: Use `django-redis` to cache frequent queries (e.g., DataTables lists).
   - **Security**: Add security tests (e.g., `django-security`).

2. **Deployment**:
   - **Containerization**: Use `docker-compose.prod.yml` for production.
   - **CI/CD**: Set up automatic deployment pipeline (e.g., GitHub Actions + Heroku).

3. **Future Features**:
   - **Mobile**: Adapt interface for mobile devices (Bootstrap 5).
   - **Weather**: Integrate weather API for direct forecasts in the application.
   - **Predictions**: Integrate ML models to predict fish growth.
