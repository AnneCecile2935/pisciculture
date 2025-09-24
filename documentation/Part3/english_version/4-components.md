## 4. **Component, Class, and Database Design**

### 4.1 **Components**
#### **A. Main Pages**
| Page                     | Description                                                  | Associated UI Components                                     |
|--------------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| **Login Page**           | User authentication (Admin/User).                            | Login form, error messages.                                  |
| **Site Management**      | List, create, and edit production sites.                     | Sites table, edit form, action buttons.                      |
| **Pond Management**      | List of ponds per site.                                      | Ponds table, edit form, site filters.                        |
| **Batch Management**     | List of fish batches with details (species, quantity, pond). | Batches table, create/edit form, species/pond filters.       |
| **Species Management**   | List and manage fish species.                                | Species table, edit form.                                    |
| **Supplier Management**  | List and manage feed suppliers.                              | Suppliers table, edit form.                                  |
| **Feed Management**      | List of feeds (linked to suppliers).                         | Feeds table, edit form.                                       |
| **Feeding Logs**         | Record and view feeding history.                             | Feedings table, recording form, date/pond filters.           |

---
#### **B. Reusable Components**
| Component            | Description                                                  | Usage                                                          |
|----------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| **Sidebar**          | Main navigation bar (links to pages).                        | Included in `base.html` (Django template inheritance).        |
| **Data Table**       | Tabular display (with pagination, sorting).                  | Used in list pages (sites, ponds, batches, etc.).            |
| **Form**             | Generic form for creating/editing entities.                  | Reused for sites, ponds, batches, etc.                       |
| **Modal**            | Modal window for confirmations or quick forms.               | Deleting a site, confirming an action.                       |
| **Flash Messages**   | Display success/error messages (e.g., "Batch created successfully"). | Included in `base.html` via `{% if messages %}`.             |
| **Filters**          | Filter bar for tables (by date, site, species, etc.).        | Used in list pages (batches, feedings).                      |
| **Breadcrumbs**      | Navigation trail (e.g., Home > Sites > Pond X).              | Included in `base.html`.                                      |

---
## **2. Component Interactions**
Each page’s components interact with each other and the backend (Django/DRF). Here’s a concrete example:

### **A. Login Page (`login.html`)**
- **Components**:
  - Login form (`<form>` with `email`/`password` fields).
  - "Forgot Password" link (optional for MVP).
  - Error messages (e.g., "Invalid email or password").
- **Interactions**:
  1. User fills the form and clicks "Login."
  2. **Vanilla JS**:
     - Validates fields (non-empty, email format).
     - Sends a `POST` request to `/api/auth/login/` using `fetch()`.
  3. **Backend (Django)**:
     - Returns a **token** on success (stored in `localStorage`).
     - Returns a **401 error** if credentials are invalid.
  4. **Frontend**:
     - Redirects to the dashboard on success.
     - Displays an error message otherwise.

### **B. Feeding Management (`repas.html`)**
- **Components**:
  - **Feedings Table**: With filters (date, pond, feed).
  - **Recording Form**: Pond, feed, and quantity selection.
  - **Export Button**: Optional CSV export (MVP).
- **Interactions**:
  1. **Initial Load**:
     - Fetches feedings via `GET /api/nourrissages/`.
     - Fetches ponds and feeds for filters/dropdowns.
  2. **Recording**:
     - Submits the form via `POST /api/nourrissages/`.
     - Refreshes the table on success.
  3. **Filtering**:
     - Sends filtered requests (e.g., `GET /api/nourrissages/?pond_id=XXX`).
