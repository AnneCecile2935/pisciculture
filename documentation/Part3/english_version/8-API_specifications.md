### 8. **API Specifications**
#### 8.1. **Authentication**
##### 8.1.1 **API Routes**
| Endpoint            | Method | Input Format (JSON)                           | Output Format (JSON)                                    | Description                                      | Authorized Roles  |
|---------------------|--------|-----------------------------------------------|--------------------------------------------------------|--------------------------------------------------|-------------------|
| `/api/auth/login/`  | POST   | `{ "email": "string", "password": "string" }` | `{ "token": "string" }`                                 | Authenticates a user and returns a token.       | Public            |
| `/api/auth/logout/` | POST   | `{ "token": "string" }`                       | `{ "success": true }`                                   | Logs out the user (invalidates the token).       | User              |
| `/api/auth/me/`     | GET    | None                                          | `{ "id": "uuid", "email": "string", "role": "string" }` | Returns the connected user's information.       | User              |

##### 8.1.2 **Error Codes**
| Endpoint            | Method | Possible Error Codes                                      |
|---------------------|--------|-----------------------------------------------------------|
| `/api/auth/login/`  | POST   | **400**: Missing email or password. **401**: Invalid credentials. |
| `/api/auth/logout/` | POST   | **400**: Missing token. **401**: Invalid or expired token. |
| `/api/auth/me/`     | GET    | **401**: Unauthenticated (missing or invalid token).      |

---
#### 8.2. **Sites**
##### 8.2.1 **API Routes**
| Endpoint           | Method | Input Format (JSON)                         | Output Format (JSON)                                         | Description               | Authorized Roles   |
|--------------------|--------|---------------------------------------------|-------------------------------------------------------------|---------------------------|--------------------|
| `/api/sites/`      | GET    | None                                        | `[{ "id": "uuid", "name": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }]` | Lists all sites.          | Admin, User        |
| `/api/sites/`      | POST   | `{ "name": "string", "address": "string" }` | `{ "id": "uuid", "name": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }` | Creates a new site.       | Admin              |
| `/api/sites/{id}/` | GET    | None                                        | `{ "id": "uuid", "name": "string", "address": "string", "bassins": ["uuid"], "created_at": "datetime", "updated_at": "datetime" }` | Site details.             | Admin, User        |
| `/api/sites/{id}/` | PUT    | `{ "name": "string", "address": "string" }` | `{ "id": "uuid", "name": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }` | Updates a site.           | Admin              |
| `/api/sites/{id}/` | DELETE | None                                        | `{ "success": true }`                                        | Deletes a site.           | Admin              |

##### 8.2.2 **Error Codes**
| Endpoint           | Method | Possible Error Codes                                                                 |
|--------------------|--------|-------------------------------------------------------------------------------------|
| `/api/sites/`      | GET    | **401**: Unauthenticated. **403**: Unauthorized (e.g., non-admin user accessing full list). |
| `/api/sites/`      | POST   | **400**: Missing `name` or `address`. **401**: Unauthenticated. **403**: Insufficient role (non-admin). **409**: A site with the same name already exists. |
| `/api/sites/{id}/` | GET    | **401**: Unauthenticated. **403**: Unauthorized. **404**: Site not found.            |
| `/api/sites/{id}/` | PUT    | **400**: Invalid data. **401**: Unauthenticated. **403**: Insufficient role. **404**: Site not found. |
| `/api/sites/{id}/` | DELETE | **401**: Unauthenticated. **403**: Insufficient role. **404**: Site not found. **409**: Site cannot be deleted (referenced by ponds). |

---
#### 8.3. **Ponds**
##### 8.3.1 **API Routes**
| Endpoint             | Method | Input Format (JSON)                                         | Output Format (JSON)                                         | Description               | Authorized Roles   |
|----------------------|--------|-------------------------------------------------------------|-------------------------------------------------------------|---------------------------|--------------------|
| `/api/bassins/`      | GET    | None                                                        | `[{ "id": "uuid", "name": "string", "site": "uuid", "capacity": "float", "created_at": "datetime", "updated_at": "datetime" }]` | Lists all ponds.          | Admin, User        |
| `/api/bassins/`      | POST   | `{ "name": "string", "site": "uuid", "capacity": "float" }` | `{ "id": "uuid", "name": "string", "site": "uuid", "capacity": "float", "created_at": "datetime", "updated_at": "datetime" }` | Creates a new pond.       | Admin              |
| `/api/bassins/{id}/` | GET    | None                                                        | `{ "id": "uuid", "name": "string", "site": { "id": "uuid", "name": "string" }, "capacity": "float", "lots": ["uuid"], "created_at": "datetime", "updated_at": "datetime" }` | Pond details.             | Admin, User        |
| `/api/bassins/{id}/` | PUT    | `{ "name": "string", "capacity": "float" }`                 | `{ "id": "uuid", "name": "string", "site": "uuid", "capacity": "float", "created_at": "datetime", "updated_at": "datetime" }` | Updates a pond.           | Admin              |
| `/api/bassins/{id}/` | DELETE | None                                                        | `{ "success": true }`                                        | Deletes a pond.           | Admin              |

##### 8.3.2 **Error Codes**
| Endpoint             | Method | Possible Error Codes                                                                 |
|----------------------|--------|-------------------------------------------------------------------------------------|
| `/api/bassins/`      | GET    | **401**: Unauthenticated.                                                           |
| `/api/bassins/`      | POST   | **400**: Missing or invalid `name`, `site`, or `capacity`. **401**: Unauthenticated. **403**: Insufficient role. **404**: Parent site not found. |
| `/api/bassins/{id}/` | GET    | **401**: Unauthenticated. **404**: Pond not found.                                  |
| `/api/bassins/{id}/` | PUT    | **400**: Invalid data. **401**: Unauthenticated. **403**: Insufficient role. **404**: Pond not found. |
| `/api/bassins/{id}/` | DELETE | **401**: Unauthenticated. **403**: Insufficient role. **404**: Pond not found. **409**: Pond cannot be deleted (referenced by lots or feedings). |

---
#### 8.4. **Species**
##### 8.4.1 **API Routes**
| Endpoint             | Method | Input Format (JSON)                                          | Output Format (JSON)                                         | Description               | Authorized Roles   |
|----------------------|--------|-------------------------------------------------------------|-------------------------------------------------------------|---------------------------|--------------------|
| `/api/especes/`      | GET    | None                                                         | `[{ "id": "uuid", "name": "string", "scientific_name": "string", "characteristics": "string", "created_at": "datetime", "updated_at": "datetime" }]` | Lists all species.        | Admin, User        |
| `/api/especes/`      | POST   | `{ "name": "string", "scientific_name": "string", "characteristics": "string" }` | `{ "id": "uuid", "name": "string", "scientific_name": "string", "characteristics": "string", "created_at": "datetime", "updated_at": "datetime" }` | Creates a new species.    | Admin              |
| `/api/especes/{id}/` | GET    | None                                                         | `{ "id": "uuid", "name": "string", "scientific_name": "string", "characteristics": "string", "created_at": "datetime", "updated_at": "datetime" }` | Species details.          | Admin, User        |
| `/api/especes/{id}/` | PUT    | `{ "name": "string", "scientific_name": "string", "characteristics": "string" }` | `{ "id": "uuid", "name": "string", "scientific_name": "string", "characteristics": "string", "created_at": "datetime", "updated_at": "datetime" }` | Updates a species.        | Admin              |
| `/api/especes/{id}/` | DELETE | None                                                         | `{ "success": true }`                                        | Deletes a species.        | Admin              |

##### 8.4.3 **Error Codes**
| Endpoint             | Method | Possible Error Codes                                                                 |
|----------------------|--------|-------------------------------------------------------------------------------------|
| `/api/especes/`      | GET    | **401**: Unauthenticated.                                                           |
| `/api/especes/`      | POST   | **400**: Missing `name`. **401**: Unauthenticated. **403**: Insufficient role. **409**: A species with the same name already exists. |
| `/api/especes/{id}/` | GET    | **401**: Unauthenticated. **404**: Species not found.                               |
| `/api/especes/{id}/` | PUT    | **400**: Invalid data. **401**: Unauthenticated. **403**: Insufficient role. **404**: Species not found. |
| `/api/especes/{id}/` | DELETE | **401**: Unauthenticated. **403**: Insufficient role. **404**: Species not found. **409**: Species cannot be deleted (referenced by lots). |

---
#### 8.5. **Fish Lots**
##### 8.5.1 **API Routes**
| Endpoint          | Method | Input Format (JSON)                                          | Output Format (JSON)                                         | Description                              | Authorized Roles   |
|-------------------|--------|-------------------------------------------------------------|-------------------------------------------------------------|------------------------------------------|--------------------|
| `/api/lots/`      | GET    | None                                                         | `[{ "id": "uuid", "species": { "id": "uuid", "name": "string" }, "quantity": "int", "pond": { "id": "uuid", "name": "string" }, "arrival_date": "date", "created_at": "datetime", "updated_at": "datetime" }]` | Lists all lots.                     | Admin, User        |
| `/api/lots/`      | POST   | `{ "species": "uuid", "quantity": "int", "pond": "uuid", "arrival_date": "date" }` | `{ "id": "uuid", "species": "uuid", "quantity": "int", "pond": "uuid", "arrival_date": "date", "created_at": "datetime", "updated_at": "datetime" }` | Creates a new lot.                     | Admin, User        |
| `/api/lots/{id}/` | GET    | None                                                         | `{ "id": "uuid", "species": { "id": "uuid", "name": "string", "scientific_name": "string" }, "quantity": "int", "pond": { "id": "uuid", "name": "string", "site": { "id": "uuid", "name": "string" } }, "arrival_date": "date", "created_at": "datetime", "updated_at": "datetime" }` | Lot details.                         | Admin, User        |
| `/api/lots/{id}/` | PUT    | `{ "quantity": "int" }`                                      | `{ "id": "uuid", "species": "uuid", "quantity": "int", "pond": "uuid", "arrival_date": "date", "created_at": "datetime", "updated_at": "datetime" }` | Updates a lot (quantity only).         | Admin, User        |
| `/api/lots/{id}/` | DELETE | None                                                         | `{ "success": true }`                                        | Deletes a lot.                           | Admin              |

##### 8.5.2 **Error Codes**
| Endpoint          | Method | Possible Error Codes                                                                 |
|-------------------|--------|-------------------------------------------------------------------------------------|
| `/api/lots/`      | GET    | **401**: Unauthenticated.                                                           |
| `/api/lots/`      | POST   | **400**: Missing or invalid `species`, `quantity`, `pond`, or `arrival_date`. **401**: Unauthenticated. **404**: Species or pond not found. |
| `/api/lots/{id}/` | GET    | **401**: Unauthenticated. **404**: Lot not found.                                   |
| `/api/lots/{id}/` | PUT    | **400**: Invalid `quantity` (e.g., negative). **401**: Unauthenticated. **404**: Lot not found. |
| `/api/lots/{id}/` | DELETE | **401**: Unauthenticated. **403**: Insufficient role. **404**: Lot not found.         |

---
#### 8.6. **Suppliers**
##### 8.6.1 **API Routes**
| Endpoint                  | Method | Input Format (JSON)                                          | Output Format (JSON)                                         | Description                  | Authorized Roles   |
|---------------------------|--------|-------------------------------------------------------------|-------------------------------------------------------------|------------------------------|--------------------|
| `/api/fournisseurs/`      | GET    | None                                                         | `[{ "id": "uuid", "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }]` | Lists all suppliers.         | Admin, User        |
| `/api/fournisseurs/`      | POST   | `{ "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string" }` | `{ "id": "uuid", "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }` | Creates a new supplier.     | Admin              |
| `/api/fournisseurs/{id}/` | GET    | None                                                         | `{ "id": "uuid", "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string", "aliments": ["uuid"], "created_at": "datetime", "updated_at": "datetime" }` | Supplier details.            | Admin, User        |
| `/api/fournisseurs/{id}/` | PUT    | `{ "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string" }` | `{ "id": "uuid", "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }` | Updates a supplier.         | Admin              |
| `/api/fournisseurs/{id}/` | DELETE | None                                                         | `{ "success": true }`                                        | Deletes a supplier.          | Admin              |

##### 8.6.2 **Error Codes**
| Endpoint                  | Method | Possible Error Codes                                                                 |
|---------------------------|--------|-------------------------------------------------------------------------------------|
| `/api/fournisseurs/`      | GET    | **401**: Unauthenticated.                                                           |
| `/api/fournisseurs/`      | POST   | **400**: Missing or invalid data (e.g., `name`, `email`). **401**: Unauthenticated. **403**: Insufficient role. **409**: A supplier with the same email already exists. |
| `/api/fournisseurs/{id}/` | GET    | **401**: Unauthenticated. **404**: Supplier not found.                              |
| `/api/fournisseurs/{id}/` | PUT    | **400**: Invalid data. **401**: Unauthenticated. **403**: Insufficient role. **404**: Supplier not found. |
| `/api/fournisseurs/{id}/` | DELETE | **401**: Unauthenticated. **403**: Insufficient role. **404**: Supplier not found. **409**: Supplier cannot be deleted (referenced by foods). |

---
#### 8.7. **Foods**
##### 8.7.1 **API Routes**
| Endpoint              | Method | Input Format (JSON)                                          | Output Format (JSON)                                         | Description              | Authorized Roles   |
|-----------------------|--------|-------------------------------------------------------------|-------------------------------------------------------------|--------------------------|--------------------|
| `/api/aliments/`      | GET    | None                                                         | `[{ "id": "uuid", "name": "string", "description": "string", "supplier": { "id": "uuid", "name": "string" }, "created_at": "datetime", "updated_at": "datetime" }]` | Lists all foods.           | Admin, User        |
| `/api/aliments/`      | POST   | `{ "name": "string", "description": "string", "supplier": "uuid" }` | `{ "id": "uuid", "name": "string", "description": "string", "supplier": "uuid", "created_at": "datetime", "updated_at": "datetime" }` | Creates a new food.        | Admin              |
| `/api/aliments/{id}/` | GET    | None                                                         | `{ "id": "uuid", "name": "string", "description": "string", "supplier": { "id": "uuid", "name": "string", "contact": "string" }, "created_at": "datetime", "updated_at": "datetime" }` | Food details.             | Admin, User        |
| `/api/aliments/{id}/` | PUT    | `{ "name": "string", "description": "string", "supplier": "uuid" }` | `{ "id": "uuid", "name": "string", "description": "string", "supplier": "uuid", "created_at": "datetime", "updated_at": "datetime" }` | Updates a food.            | Admin              |
| `/api/aliments/{id}/` | DELETE | None                                                         | `{ "success": true }`                                        | Deletes a food.           | Admin              |

##### 8.7.2 **Error Codes**
| Endpoint              | Method | Possible Error Codes                                                                 |
|-----------------------|--------|-------------------------------------------------------------------------------------|
| `/api/aliments/`      | GET    | **401**: Unauthenticated.                                                           |
| `/api/aliments/`      | POST   | **400**: Missing `name` or `supplier`. **401**: Unauthenticated. **403**: Insufficient role. **404**: Supplier not found. |
| `/api/aliments/{id}/` | GET    | **401**: Unauthenticated. **404**: Food not found.                                  |
| `/api/aliments/{id}/` | PUT    | **400**: Invalid data. **401**: Unauthenticated. **403**: Insufficient role. **404**: Food or supplier not found. |
| `/api/aliments/{id}/` | DELETE | **401**: Unauthenticated. **403**: Insufficient role. **404**: Food not found. **409**: Food cannot be deleted (referenced by feedings). |

---
#### 8.8. **Feedings**
##### 8.8.1 **API Routes**
| Endpoint                  | Method | Input Format (JSON)                                       | Output Format (JSON)                                         | Description                                                  | Authorized Roles   |
|---------------------------|--------|----------------------------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------|--------------------|
| `/api/nourrissages/`      | GET    | None                                                      | `[{ "id": "uuid", "pond": { "id": "uuid", "name": "string" }, "food": { "id": "uuid", "name": "string" }, "quantity": "float", "feeding_date": "datetime", "recorded_by": { "id": "uuid", "email": "string" }, "created_at": "datetime", "updated_at": "datetime" }]` | Lists all feedings (filtered by user if Manager). | Admin, User        |
| `/api/nourrissages/`      | POST   | `{ "pond": "uuid", "food": "uuid", "quantity": "float" }` | `{ "id": "uuid", "pond": "uuid", "food": "uuid", "quantity": "float", "feeding_date": "datetime", "recorded_by": "uuid", "created_at": "datetime", "updated_at": "datetime" }` | Creates a new feeding.                                 | Admin, User        |
| `/api/nourrissages/{id}/` | GET    | None                                                      | `{ "id": "uuid", "pond": { "id": "uuid", "name": "string", "site": { "id": "uuid", "name": "string" } }, "food": { "id": "uuid", "name": "string", "supplier": { "id": "uuid", "name": "string" } }, "quantity": "float", "feeding_date": "datetime", "recorded_by": { "id": "uuid", "email": "string", "role": "string" }, "created_at": "datetime", "updated_at": "datetime" }` | Feeding details.                                     | Admin, User        |
| `/api/nourrissages/{id}/` | PUT    | `{ "quantity": "float" }`                                 | `{ "id": "uuid", "pond": "uuid", "food": "uuid", "quantity": "float", "feeding_date": "datetime", "recorded_by": "uuid", "created_at": "datetime", "updated_at": "datetime" }` | Updates a feeding (quantity only).             | Admin, User        |
| `/api/nourrissages/{id}/` | DELETE | None                                                      | `{ "success": true }`                                        | Deletes a feeding.                                     | Admin              |

##### 8.8.2 **Error Codes**
| Endpoint                  | Method | Possible Error Codes                                                                 |
|---------------------------|--------|-------------------------------------------------------------------------------------|
| `/api/nourrissages/`      | GET    | **401**: Unauthenticated.                                                           |
| `/api/nourrissages/`      | POST   | **400**: Missing or invalid `pond`, `food`, or `quantity`. **401**: Unauthenticated. **404**: Pond or food not found. |
| `/api/nourrissages/{id}/` | GET    | **401**: Unauthenticated. **403**: Unauthorized (e.g., manager accessing a feeding they didn’t record). **404**: Feeding not found. |
| `/api/nourrissages/{id}/` | PUT    | **400**: Invalid `quantity`. **401**: Unauthenticated. **403**: Unauthorized. **404**: Feeding not found. |
| `/api/nourrissages/{id}/` | DELETE | **401**: Unauthenticated. **403**: Insufficient role or unauthorized. **404**: Feeding not found. |

---
#### 8.10. **POST/PUT Request Examples**
##### **Create a Feeding (`POST /api/nourrissages/`)**
###### **Request**:
```json
{
    "pond": "550e8400-e29b-41d4-a716-446655440000",
    "food": "e5f6g7h8-e89b-41d4-a716-446655440000",
    "quantity": 2.5
}
```


###### **Response (201 Created)** :

```json
{
    "id": "g7h8i9j0-e89b-41d4-a716-446655440000",
    "pond": "550e8400-e29b-41d4-a716-446655440000",
    "food": "e5f6g7h8-e89b-41d4-a716-446655440000",
    "quantity": 2.5,
    "feeding_date": "2025-09-20T08:30:00Z",
    "recorded_by": "a1b2c3d4-e89b-41d4-a716-446655441111",
    "created_at": "2025-09-20T08:30:00Z",
    "updated_at": "2025-09-20T08:30:00Z"
}
```

