## 1. **User Stories**

### 1.1 **User Rights**
| Priority     | User Story                                                                 | Role Concerned |
|--------------|----------------------------------------------------------------------------|----------------|
| Must Have    | As an **admin**, and **only as an admin**, I want to create/modify/delete user accounts to manage application access. | Admin          |
| Must Have    | As an **admin**, I want to modify a user’s email and password to maintain account security. | Admin          |
| Must Have    | As a **user**, I want to log in with my email and password to access the application. | All            |
| Must Have    | As a **user**, I want to log out of my account to exit the application.       | All            |
| Should Have  | As a **user**, I want to reset my password to avoid losing access to my account. | All            |
| Should Have  | As an **admin**, I want to assign roles (admin, manager, user) to limit permissions. | Admin          |
| Could Have   | As a **user**, I want to receive a confirmation email after password reset. | All            |

### 1.2 **Sites/Ponds**
| Priority     | User Story                                                                 | Role Concerned |
|--------------|----------------------------------------------------------------------------|----------------|
| Must Have    | As an **admin**, I want to create/modify/delete a production site to structure the application. | Admin          |
| Must Have    | As an **admin**, I want to create/modify/delete a pond to manage infrastructure. | Admin          |
| Must Have    | As a **user**, I want to see the list of ponds for a given site to check feeding status. | All            |
| Should Have  | As an **admin**, I want to associate a pond with a specific site to organize data. | Admin          |
| Could Have   | As a **user**, I want to filter ponds by site for quick data access.         | All            |

### 1.3 **Stock Management**
| Priority     | User Story                                                                 | Role Concerned |
|--------------|----------------------------------------------------------------------------|----------------|
| Must Have    | As a **user**, I want to create a fish batch to track growth and feeding.   | All            |
| Must Have    | As a **user**, I want to assign a batch to a pond to locate fish.           | All            |
| Must Have    | As a **user**, I want to create/modify/delete a feed type to manage stock.  | All            |
| Should Have  | As a **user**, I want to view batch history per pond to analyze production. | All            |
| Could Have   | As a **user**, I want to receive a low-stock alert for feed to avoid shortages. | All        |

### 1.4 **Daily Activity**
| Priority     | User Story                                                                 | Role Concerned |
|--------------|----------------------------------------------------------------------------|----------------|
| Must Have    | As a **user**, I want to record feeding (pond, feed, quantity) to track nutrition. | All            |
| Should Have  | As a **user**, I want to view feeding history per pond to adjust quantities. | All            |

### 1.5 **Suppliers**
| Priority     | User Story                                                                 | Role Concerned |
|--------------|----------------------------------------------------------------------------|----------------|
| Must Have    | As a **user**, I want to create/modify/delete a supplier to link feed to suppliers. | All            |
| Must Have    | As a **user**, I want to associate feed with a supplier to track procurement. | All            |

### 1.6 **Transverse Features**
| Priority     | User Story                                                                 | Role Concerned |
|--------------|----------------------------------------------------------------------------|----------------|
| Should Have  | As a **user**, I want to export data (feeding logs, records) as CSV for offline analysis. | All            |
| Should Have  | As a **user**, I want a dashboard with key metrics (e.g., mortality, feeding). | All            |
| Could Have   | As a **user**, I want mobile access to the app to record data in the field. | All            |
