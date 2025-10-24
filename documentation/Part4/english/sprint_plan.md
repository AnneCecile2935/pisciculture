## **Sprint 1: Core Functionality (Feeding, Sites, Basins, Species)**
**Duration**: 2 weeks (e.g., 2025-09-01 → 2025-09-14)
**Objective**: Set up base models, forms, and views for core features.

### **Tasks and Evidence**
# Sprint 1 - Details
   Task                                      | Priority | Duration | Status  | Evidence                                             | Link to code/test                                           |
 |-------------------------------------------|----------|----------|---------|------------------------------------------------------|-------------------------------------------------------------|
 | Initialize Django project                 | P0       | 1 day    | Done    | Basic configuration, Docker, PostgreSQL.             | [e9339ff](https://github.com/AnneCecile2935/pisciculture/commit/e9339ffabc7c48d7ecea1c436e7281434bf289e8) |
 | Create Site, Bassin, Espece models         | P0       | 2 days   | Done    | Models with ForeignKey relationships.                | [30b8c63](https://github.com/AnneCecile2935/pisciculture/commit/30b8c63de54c02173677dd2cb1534772b0bbee63) |
 | Configure admin for Site and Bassin        | P1       | 1 day    | Done    | Customization of admin interface.                    | [fba60a9](https://github.com/AnneCecile2935/pisciculture/commit/fba60a963487abbaf740374efe489fc01531fbc3) |
 | Implement LotDePoisson model               | P1       | 1 day    | Done    | Model with automatic average weight calculation.     | [b5c8cc2](https://github.com/AnneCecile2935/pisciculture/commit/b5c8cc28f27786e2572e29d56748289d931ce548) |
 | Add Aliment model                          | P1       | 1 day    | Done    | Model with relationship to Fournisseur.              | [c693e75](https://github.com/AnneCecile2935/pisciculture/commit/c693e75cb8f96019faa707135db698e8598047e0) |
 | Configure admin permissions                | P1       | 0.5 day  | Done    | Custom permissions for admins.                       | [fba60a9](https://github.com/AnneCecile2935/pisciculture/commit/fba60a963487abbaf740374efe489fc01531fbc3) |
 | Fix migration errors                       | P1       | 0.5 day  | Done    | Resolution of database conflicts.                    | [f4849cc](https://github.com/AnneCecile2935/pisciculture/commit/f4849cc7596da7597080b01609e3970118ed8ce2) |
 | Add tests for models                       | P2       | 1 day    | Done    | Unit tests for Site, Bassin, Espece, Aliment.         | [617edf4](https://github.com/AnneCecile2935/pisciculture/commit/617edf4d00e3d584fee32ae6443dc88cef8a887d), [6ee50ec](https://github.com/AnneCecile2935/pisciculture/commit/6ee50ec599544683bcda9809ee593f18fe13cfba) |

### **Blockers and Solutions**
- **Issue**: Migration conflicts for Site and Bassin models.
  **Solution**: Reset migrations and fixed fields.
  **Evidence**: [f4849cc](link).
- **Issue**: Syntax errors in models.
  **Solution**: Corrected fields and relationships.
  **Evidence**: [a0cb881](link).

------
## **Sprint 2: Feeding and User Interface**
**Duration**: 2 weeks (e.g., 2025-09-15 → 2025-09-28)
**Objective**: Implement feeding module, improve user interface, and add tests.

### **Tasks and Evidence**
# Sprint 2 - Details
 | Task                                      | Priority | Duration | Status  | Evidence                                             | Link to code/test                                           |
 |-------------------------------------------|----------|----------|---------|------------------------------------------------------|-------------------------------------------------------------|
 | Add Nourrissage model                     | P0       | 1 day    | Done    | Model to record fish meals.                          | [8b4678e](https://github.com/AnneCecile2935/pisciculture/commit/8b4678e3a024ae371f1413a2fa13c8eea93e5d0c) |
 | Configure URLs for Nourrissage            | P0       | 0.5 day  | Done    | Added routes for CRUD operations.                    | [430cd3c](https://github.com/AnneCecile2935/pisciculture/commit/430cd3c9c2c4fbc95d0154eca5210af6f311f2c8) |
 | Create templates for Nourrissage          | P0       | 1 day    | Done    | Templates for displaying and entering meals.         | [7746576](https://github.com/AnneCecile2935/pisciculture/commit/774657628c22738c7df9b5c653fc8b6f85d5f4a9) |
 | Implement feeding form                    | P0       | 2 days   | Done    | Form to record meals per basin.                      | [0f2fa07](https://github.com/AnneCecile2935/pisciculture/commit/0f2fa0766c3828d3b556923071da46271df23647) |
 | Add DataTables for lists                   | P1       | 2 days   | Done    | Integration of DataTables for dynamic lists.         | [868d3af](https://github.com/AnneCecile2935/pisciculture/commit/868d3af9346c32602c1203cda334ff3100ce612b), [260e0cf](https://github.com/AnneCecile2935/pisciculture/commit/260e0cf4e53c512b3ef5cb372199c1bfb40e1ccd) |
 | Improve layout and sidebar                 | P1       | 1 day    | Done    | Added sub-menus and styles for the sidebar.           | [d4f2de2](https://github.com/AnneCecile2935/pisciculture/commit/d4f2de2e453c73c6c463ff74d8df8f1335fc96b9) |
 | Add tests for Nourrissage                 | P1       | 1 day    | Done    | Unit and integration tests for the Nourrissage module. | [0f2fa07](https://github.com/AnneCecile2935/pisciculture/commit/0f2fa0766c3828d3b556923071da46271df23647) |
 | Fix form widgets                           | P2       | 0.5 day  | Done    | Corrected error messages and widgets.                | [5fd6ff2](https://github.com/AnneCecile2935/pisciculture/commit/5fd6ff282bce3899015cfd4d1415c5346ab1f90f) |

### **Blockers and Solutions**
- **Issue**: Incorrect display of DataTables.
  **Solution**: Fixed templates and AJAX calls.
  **Evidence**: [868d3af](link).
- **Issue**: Unclear error messages in forms.
  **Solution**: Standardized messages and CSS classes.
  **Evidence**: [5fd6ff2](link).

------
## **Sprint 3: Improvements and Full Testing**
**Duration**: 2 weeks (e.g., 2025-09-29 → 2025-10-12)
**Objective**: Finalize features, add comprehensive tests, and improve the interface.

### **Tasks and Evidence**
# Sprint 3 - Details
 | Task                                      | Priority | Duration | Status  | Evidence                                             | Link to code/test                                           |
 |-------------------------------------------|----------|----------|---------|------------------------------------------------------|-------------------------------------------------------------|
 | Add global form per site                  | P0       | 2 days   | Done    | Form to record meals for all basins of a site.       | [93a9eb9](https://github.com/AnneCecile2935/pisciculture/commit/93a9eb9582d93999c7eb56faa31a6d6550955b27) |
 | Standardize confirmation messages         | P0       | 0.5 day  | Done    | Consistent messages for deletion and actions.       | [626780e](https://github.com/AnneCecile2935/pisciculture/commit/626780e48d43064277872e6b41756e8a7c52f51f) |
 | Improve form styles                       | P1       | 1 day    | Done    | Added `form_style.css` for visual consistency.        | [f9fc1f4](https://github.com/AnneCecile2935/pisciculture/commit/f9fc1f406a49e56c85981df390f8131fa826e161) |
 | Integrate DataTables for all modules      | P1       | 2 days   | Done    | Migrated static lists to DataTables (Aliments, Fournisseurs, etc.). | [c8956b9](https://github.com/AnneCecile2935/pisciculture/commit/c8956b930ca6c141b55ca7389bf6d4a5ea84cee4), [f1b3101](https://github.com/AnneCecile2935/pisciculture/commit/f1b31016badd03ac64910a1df930790165769d67) |
 | Add tests for views                        | P1       | 2 days   | Done    | Tests for authentication, user, and feeding views.   | [edd4f21](https://github.com/AnneCecile2935/pisciculture/commit/edd4f2127cf3f867568d4cc1a160ab11edf1315c), [7813942](https://github.com/AnneCecile2935/pisciculture/commit/78139429a70030685f11ea07ffad93dcfb02b18f) |
 | Configure pytest and factory_boy          | P1       | 1 day    | Done    | Set up testing tools.                                | [7a23d96](https://github.com/AnneCecile2935/pisciculture/commit/7a23d96f30b5285790184ff6748623fc94a0f15f) |
 | Fix minor bugs                             | P2       | 1 day    | Done    | Resolved permission and display issues.              | [417a8e3](https://github.com/AnneCecile2935/pisciculture/commit/417a8e3f8331d7e706f79cdc8979c42fe702abb1) |

### **Blockers and Solutions**
- **Issue**: Test incompatibility with new migrations.
  **Solution**: Updated test factories and fixtures.
  **Evidence**: [8cc09f9](link).
- **Issue**: Permission conflicts for standard users.
  **Solution**: Used `UserPassesTestMixin` for views.
  **Evidence**: [3a3a5de](link).

------
## **Sprint 4: Finalization and Documentation**
**Duration**: 1 week (e.g., 2025-10-13 → 2025-10-20)
**Objective**: Finalize remaining features, complete documentation, and prepare for delivery.

### **Tasks and Evidence**
# Sprint 4 - Details
 | Task                                      | Priority | Duration | Status  | Evidence                                             | Link to code/test                                           |
 |-------------------------------------------|----------|----------|---------|------------------------------------------------------|-------------------------------------------------------------|
 | Complete documentation                    | P0       | 2 days   | Done    | Added diagrams, technical documentation, and user stories. | [d2373e3](https://github.com/AnneCecile2935/pisciculture/commit/d2373e358f297c72a5a00a71fa4dfcb7098d0297), [14b35e7](https://github.com/AnneCecile2935/pisciculture/commit/14b35e7063765ae1fdd69fbd33f713b9f7a7170d) |
 | Add tests for missing models              | P0       | 1 day    | Done    | Tests for Fournisseurs, Stocks, Espèces.             | [ad02410](https://github.com/AnneCecile2935/pisciculture/commit/ad024105c18808c06525fc2edf70e29e6e7cdc1d), [617edf4](https://github.com/AnneCecile2935/pisciculture/commit/617edf4d00e3d584fee32ae6443dc88cef8a887d) |
 | Finalize DataTables charts                 | P1       | 1 day    | Done    | Integrated Chart.js for temperature and oxygen graphs. | [868d3af](https://github.com/AnneCecile2935/pisciculture/commit/868d3af9346c32602c1203cda334ff3100ce612b) |
 | Fix remaining bugs                        | P1       | 1 day    | Done    | Resolved minor display and validation issues.        | [5fd6ff2](https://github.com/AnneCecile2935/pisciculture/commit/5fd6ff282bce3899015cfd4d1415c5346ab1f90f) |
 | Prepare demonstration                      | P2       | 0.5 day  | Done    | Screenshots and demo video.                          | [Link to screenshots](https://chat.mistral.ai/chat/link)    |

### **Remaining Tasks:**
- Implement the dashboard
- Add basin category (basin or lab)
- Different deletion popup for Aliment
- Change user access permissions
- Add cancel button to site meal form
- Add * to required fields
- Redo tests for daily activity (since site meal form is functional)
- Fix test database
