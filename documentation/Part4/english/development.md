# Development Log - Pisciculture

---

## **Sprint 1: Core Functionality (2025-09-01 → 2025-09-14)**

### **Base Models (Site, Bassin, Espece)**
- **Commit**: [30b8c63](https://github.com/AnneCecile2935/pisciculture/commit/30b8c63)
- **Modified Files**:
  - `apps/sites/models.py` (Site, Bassin)
- **Description**:
  - Created models `Site`, `Bassin`, `Espece`, and established ForeignKey relationships.
  - Basic admin configuration for `Site` and `Bassin`.
- **Blocker**: Initial migration conflicts.
  **Solution**: Reset migrations and fixed fields (`python manage.py makemigrations --merge`).
  **Proof**: [f4849cc](https://github.com/AnneCecile2935/pisciculture/commit/f4849cc).

### **LotDePoisson Model**
- **Commit**: [b5c8cc2](https://github.com/AnneCecile2935/pisciculture/commit/b5c8cc2)
- **Modified Files**:
  - `apps/stocks/models.py` (LotDePoisson)
- **Description**:
  - Added model with automatic average weight calculation.
  - Relationship to `Bassin` and `Espece`.

### **Aliment and Fournisseur Models**
- **Commit**: [c693e75](https://github.com/AnneCecile2935/pisciculture/commit/c693e75)
- **Modified Files**:
  - `apps/stocks/models.py` (Aliment, StockAliment)
  - `apps/fournisseurs/models.py` (Fournisseur)
- **Description**:
  - `Aliment` model with quantity validation.
  - Relationship to `Fournisseur`.

---

## **Sprint 2: Feeding and User Interface (2025-09-15 → 2025-09-28)**

### **Nourrissage Model and Form**
- **Commit**: [8b4678e](https://github.com/AnneCecile2935/pisciculture/commit/8b4678e)
- **Modified Files**:
  - `apps/activite_quotidien/models.py` (Nourrissage)
  - `apps/activite_quotidien/forms.py` (NourrissageForm)
- **Description**:
  - Model to record meals per basin.
  - Basic form for data entry.
- **Screenshot**:
  ![Feeding Form V1](images/sprint2_nourrissage_form_v1.png)

### **DataTables Integration**
- **Commit**: [868d3af](https://github.com/AnneCecile2935/pisciculture/commit/868d3af)
- **Modified Files**:
  - `templates/activite_quotidien/nourrissage_list.html`
  - `static/js/datatables_init.js`
- **Description**:
  - Migrated static lists to DataTables (AJAX, pagination, sorting).
  - Fixed templates to display data dynamically.
- **Blocker**: Incorrect data display.
  **Solution**: Corrected columns and AJAX calls.
  **Proof**: [260e0cf](https://github.com/AnneCecile2935/pisciculture/commit/260e0cf).

---

## **Sprint 3: Improvements and Testing (2025-09-29 → 2025-10-12)**

### **Global Form per Site**
- **Commit**: [93a9eb9](https://github.com/AnneCecile2935/pisciculture/commit/93a9eb9)
- **Modified Files**:
  - `apps/activite_quotidien/forms.py` (GlobalNourrissageForm)
  - `templates/activite_quotidien/nourrissage_global_form.html`
- **Description**:
  - Form to enter meals **for all basins of a site** at once.
  - JavaScript logic to calculate totals.
- **Screenshot**:
  ![Global Form](images/sprint3_global_form.png)

### **Unit and Integration Tests**
- **Commit**: [0f2fa07](https://github.com/AnneCecile2935/pisciculture/commit/0f2fa07)
- **Modified Files**:
  - `tests/activite_quotidien/test_nourrissage.py`
- **Description**:
  - Tests for creation, validation, and display of feeding records.
  - 100% coverage with `pytest --cov`.
- **Test Results**:
  ```bash
  === 8 tests passed in 1.2s (100% coverage) ===
