### 8. **Spécifications des APIs**

#### 	8.1.**Authentification**

##### 		8.1.1 **Routes API**

| Endpoint            | Method | Input Format (JSON)                           | Output Format (JSON)                                    | Description                                          | Roles Authorized |
| ------------------- | ------ | --------------------------------------------- | ------------------------------------------------------- | ---------------------------------------------------- | ---------------- |
| `/api/auth/login/`  | POST   | `{ "email": "string", "password": "string" }` | `{ "token": "string" }`                                 | Authentifie un utilisateur et retourne un token.     | Public           |
| `/api/auth/logout/` | POST   | `{ "token": "string" }`                       | `{ "success": true }`                                   | Déconnecte l'utilisateur (invalide le token).        | Utilisateur      |
| `/api/auth/me/`     | GET    | None                                          | `{ "id": "uuid", "email": "string", "role": "string" }` | Retourne les informations de l'utilisateur connecté. | Utilisateur      |

##### 	8.1.2 Codes erreurs:

| Endpoint            | Method | Codes d'Erreur Possibles                                     |
| ------------------- | ------ | ------------------------------------------------------------ |
| `/api/auth/login/`  | POST   | **400** : Email ou mot de passe manquant. **401** : Identifiants invalides. |
| `/api/auth/logout/` | POST   | **400** : Token manquant. **401** : Token invalide ou expiré. |
| `/api/auth/me/`     | GET    | **401** : Non authentifié (token manquant ou invalide).      |

---

#### 	8.2 **Sites**

##### 		8.2.1 **Routes API**

| Endpoint           | Method | Input Format (JSON)                         | Output Format (JSON)                                         | Description           | Roles Authorized   |
| ------------------ | ------ | ------------------------------------------- | ------------------------------------------------------------ | --------------------- | ------------------ |
| `/api/sites/`      | GET    | None                                        | `[{ "id": "uuid", "name": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }]` | Liste tous les sites. | Admin, Utilisateur |
| `/api/sites/`      | POST   | `{ "name": "string", "address": "string" }` | `{ "id": "uuid", "name": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }` | Crée un nouveau site. | Admin              |
| `/api/sites/{id}/` | GET    | None                                        | `{ "id": "uuid", "name": "string", "address": "string", "bassins": ["uuid"], "created_at": "datetime", "updated_at": "datetime" }` | Détail d'un site.     | Admin, Utilisateur |
| `/api/sites/{id}/` | PUT    | `{ "name": "string", "address": "string" }` | `{ "id": "uuid", "name": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }` | Met à jour un site.   | Admin              |
| `/api/sites/{id}/` | DELETE | None                                        | `{ "success": true }`                                        | Supprime un site.     | Admin              |

##### 		8.2.2 Codes erreurs:

| Endpoint           | Method | Codes d'Erreur Possibles                                     |
| ------------------ | ------ | ------------------------------------------------------------ |
| `/api/sites/`      | GET    | **401** : Non authentifié. **403** : Utilisateur non autorisé (ex: un utilisateur non-admin essaye d'accéder à une liste complète). |
| `/api/sites/`      | POST   | **400** : `name` ou `address` manquant. **401** : Non authentifié. **403** : Rôle insuffisant (non-admin). **409** : Un site avec le même nom existe déjà. |
| `/api/sites/{id}/` | GET    | **401** : Non authentifié. **403** : Utilisateur non autorisé. **404** : Site non trouvé. |
| `/api/sites/{id}/` | PUT    | **400** : Données invalides. **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Site non trouvé. |
| `/api/sites/{id}/` | DELETE | **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Site non trouvé. **409** : Le site ne peut pas être supprimé car il est référencé par des bassins. |

#### 	8.3.**Bassins**

##### 		8.3.1 **Routes API**

| Endpoint             | Method | Input Format (JSON)                                         | Output Format (JSON)                                         | Description             | Roles Authorized   |
| -------------------- | ------ | ----------------------------------------------------------- | ------------------------------------------------------------ | ----------------------- | ------------------ |
| `/api/bassins/`      | GET    | None                                                        | `[{ "id": "uuid", "name": "string", "site": "uuid", "capacity": "float", "created_at": "datetime", "updated_at": "datetime" }]` | Liste tous les bassins. | Admin, Utilisateur |
| `/api/bassins/`      | POST   | `{ "name": "string", "site": "uuid", "capacity": "float" }` | `{ "id": "uuid", "name": "string", "site": "uuid", "capacity": "float", "created_at": "datetime", "updated_at": "datetime" }` | Crée un nouveau bassin. | Admin              |
| `/api/bassins/{id}/` | GET    | None                                                        | `{ "id": "uuid", "name": "string", "site": { "id": "uuid", "name": "string" }, "capacity": "float", "lots": ["uuid"], "created_at": "datetime", "updated_at": "datetime" }` | Détail d'un bassin.     | Admin, Utilisateur |
| `/api/bassins/{id}/` | PUT    | `{ "name": "string", "capacity": "float" }`                 | `{ "id": "uuid", "name": "string", "site": "uuid", "capacity": "float", "created_at": "datetime", "updated_at": "datetime" }` | Met à jour un bassin.   | Admin              |
| `/api/bassins/{id}/` | DELETE | None                                                        | `{ "success": true }`                                        | Supprime un bassin.     | Admin              |

##### 		8.2.2 Codes erreurs

| Endpoint             | Method | Codes d'Erreur Possibles                                     |
| -------------------- | ------ | ------------------------------------------------------------ |
| `/api/bassins/`      | GET    | **401** : Non authentifié.                                   |
| `/api/bassins/`      | POST   | **400** : `name`, `site`, ou `capacity` manquant ou invalide. **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Site parent non trouvé. |
| `/api/bassins/{id}/` | GET    | **401** : Non authentifié. **404** : Bassin non trouvé.      |
| `/api/bassins/{id}/` | PUT    | **400** : Données invalides. **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Bassin non trouvé. |
| `/api/bassins/{id}/` | DELETE | **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Bassin non trouvé. **409** : Le bassin ne peut pas être supprimé car il est référencé par des lots ou des nourrissages. |

#### 	8.4.**Espèces**

##### 		8.4.1 **Routes API**

| Endpoint             | Method | Input Format (JSON)                                          | Output Format (JSON)                                         | Description               | Roles Authorized   |
| -------------------- | ------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------- | ------------------ |
| `/api/especes/`      | GET    | None                                                         | `[{ "id": "uuid", "name": "string", "scientific_name": "string", "characteristics": "string", "created_at": "datetime", "updated_at": "datetime" }]` | Liste toutes les espèces. | Admin, Utilisateur |
| `/api/especes/`      | POST   | `{ "name": "string", "scientific_name": "string", "characteristics": "string" }` | `{ "id": "uuid", "name": "string", "scientific_name": "string", "characteristics": "string", "created_at": "datetime", "updated_at": "datetime" }` | Crée une nouvelle espèce. | Admin              |
| `/api/especes/{id}/` | GET    | None                                                         | `{ "id": "uuid", "name": "string", "scientific_name": "string", "characteristics": "string", "created_at": "datetime", "updated_at": "datetime" }` | Détail d'une espèce.      | Admin, Utilisateur |
| `/api/especes/{id}/` | PUT    | `{ "name": "string", "scientific_name": "string", "characteristics": "string" }` | `{ "id": "uuid", "name": "string", "scientific_name": "string", "characteristics": "string", "created_at": "datetime", "updated_at": "datetime" }` | Met à jour une espèce.    | Admin              |
| `/api/especes/{id}/` | DELETE | None                                                         | `{ "success": true }`                                        | Supprime une espèce.      | Admin              |

##### 		8.4.3 Codes erreur:

| Endpoint             | Method | Codes d'Erreur Possibles                                     |
| -------------------- | ------ | ------------------------------------------------------------ |
| `/api/especes/`      | GET    | **401** : Non authentifié.                                   |
| `/api/especes/`      | POST   | **400** : `name` manquant. **401** : Non authentifié. **403** : Rôle insuffisant. **409** : Une espèce avec le même nom existe déjà. |
| `/api/especes/{id}/` | GET    | **401** : Non authentifié. **404** : Espèce non trouvée.     |
| `/api/especes/{id}/` | PUT    | **400** : Données invalides. **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Espèce non trouvée. |
| `/api/especes/{id}/` | DELETE | **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Espèce non trouvée. **409** : L'espèce ne peut pas être supprimée car elle est référencée par des lots. |

#### 	8.5.**Lot de Poisson**

##### 		.85.1 Routes API

| Endpoint          | Method | Input Format (JSON)                                          | Output Format (JSON)                                         | Description                              | Roles Authorized   |
| ----------------- | ------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------------------------- | ------------------ |
| `/api/lots/`      | GET    | None                                                         | `[{ "id": "uuid", "species": { "id": "uuid", "name": "string" }, "quantity": "int", "pond": { "id": "uuid", "name": "string" }, "arrival_date": "date", "created_at": "datetime", "updated_at": "datetime" }]` | Liste tous les lots.                     | Admin, Utilisateur |
| `/api/lots/`      | POST   | `{ "species": "uuid", "quantity": "int", "pond": "uuid", "arrival_date": "date" }` | `{ "id": "uuid", "species": "uuid", "quantity": "int", "pond": "uuid", "arrival_date": "date", "created_at": "datetime", "updated_at": "datetime" }` | Crée un nouveau lot.                     | Admin, Utilisateur |
| `/api/lots/{id}/` | GET    | None                                                         | `{ "id": "uuid", "species": { "id": "uuid", "name": "string", "scientific_name": "string" }, "quantity": "int", "pond": { "id": "uuid", "name": "string", "site": { "id": "uuid", "name": "string" } }, "arrival_date": "date", "created_at": "datetime", "updated_at": "datetime" }` | Détail d'un lot.                         | Admin, Utilisateur |
| `/api/lots/{id}/` | PUT    | `{ "quantity": "int" }`                                      | `{ "id": "uuid", "species": "uuid", "quantity": "int", "pond": "uuid", "arrival_date": "date", "created_at": "datetime", "updated_at": "datetime" }` | Met à jour un lot (quantité uniquement). | Admin, Utilisateur |
| `/api/lots/{id}/` | DELETE | None                                                         | `{ "success": true }`                                        | Supprime un lot.                         | Admin              |

##### 		8.5.2 Codes erreur:

| Endpoint          | Method | Codes d'Erreur Possibles                                     |
| ----------------- | ------ | ------------------------------------------------------------ |
| `/api/lots/`      | GET    | **401** : Non authentifié.                                   |
| `/api/lots/`      | POST   | **400** : `species`, `quantity`, `pond`, ou `arrival_date` manquant ou invalide. **401** : Non authentifié. **404** : Espèce ou bassin non trouvé. |
| `/api/lots/{id}/` | GET    | **401** : Non authentifié. **404** : Lot non trouvé.         |
| `/api/lots/{id}/` | PUT    | **400** : `quantity` invalide (ex: négatif). **401** : Non authentifié. **404** : Lot non trouvé. |
| `/api/lots/{id}/` | DELETE | **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Lot non trouvé. |

#### 	8.6 **Fournisseurs**

##### 		8.6.1 Routes API

| Endpoint                  | Method | Input Format (JSON)                                          | Output Format (JSON)                                         | Description                  | Roles Authorized   |
| ------------------------- | ------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------------- | ------------------ |
| `/api/fournisseurs/`      | GET    | None                                                         | `[{ "id": "uuid", "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }]` | Liste tous les fournisseurs. | Admin, Utilisateur |
| `/api/fournisseurs/`      | POST   | `{ "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string" }` | `{ "id": "uuid", "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }` | Crée un nouveau fournisseur. | Admin              |
| `/api/fournisseurs/{id}/` | GET    | None                                                         | `{ "id": "uuid", "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string", "aliments": ["uuid"], "created_at": "datetime", "updated_at": "datetime" }` | Détail d'un fournisseur.     | Admin, Utilisateur |
| `/api/fournisseurs/{id}/` | PUT    | `{ "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string" }` | `{ "id": "uuid", "name": "string", "contact": "string", "product_type": "string", "email": "string", "phone": "string", "address": "string", "created_at": "datetime", "updated_at": "datetime" }` | Met à jour un fournisseur.   | Admin              |
| `/api/fournisseurs/{id}/` | DELETE | None                                                         | `{ "success": true }`                                        | Supprime un fournisseur.     | Admin              |

##### 		8.6.2 Codes erreur

| Endpoint                  | Method | Codes d'Erreur Possibles                                     |
| ------------------------- | ------ | ------------------------------------------------------------ |
| `/api/fournisseurs/`      | GET    | **401** : Non authentifié.                                   |
| `/api/fournisseurs/`      | POST   | **400** : Données manquantes ou invalides (ex: `name`, `email`). **401** : Non authentifié. **403** : Rôle insuffisant. **409** : Un fournisseur avec le même email existe déjà. |
| `/api/fournisseurs/{id}/` | GET    | **401** : Non authentifié. **404** : Fournisseur non trouvé. |
| `/api/fournisseurs/{id}/` | PUT    | **400** : Données invalides. **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Fournisseur non trouvé. |
| `/api/fournisseurs/{id}/` | DELETE | **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Fournisseur non trouvé. **409** : Le fournisseur ne peut pas être supprimé car il est référencé par des aliments. |

#### 	**8.7. Aliments**

##### 		8.7.1 Routes API

| Endpoint              | Method | Input Format (JSON)                                          | Output Format (JSON)                                         | Description              | Roles Authorized   |
| --------------------- | ------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------ | ------------------ |
| `/api/aliments/`      | GET    | None                                                         | `[{ "id": "uuid", "name": "string", "description": "string", "supplier": { "id": "uuid", "name": "string" }, "created_at": "datetime", "updated_at": "datetime" }]` | Liste tous les aliments. | Admin, Utilisateur |
| `/api/aliments/`      | POST   | `{ "name": "string", "description": "string", "supplier": "uuid" }` | `{ "id": "uuid", "name": "string", "description": "string", "supplier": "uuid", "created_at": "datetime", "updated_at": "datetime" }` | Crée un nouvel aliment.  | Admin              |
| `/api/aliments/{id}/` | GET    | None                                                         | `{ "id": "uuid", "name": "string", "description": "string", "supplier": { "id": "uuid", "name": "string", "contact": "string" }, "created_at": "datetime", "updated_at": "datetime" }` | Détail d'un aliment.     | Admin, Utilisateur |
| `/api/aliments/{id}/` | PUT    | `{ "name": "string", "description": "string", "supplier": "uuid" }` | `{ "id": "uuid", "name": "string", "description": "string", "supplier": "uuid", "created_at": "datetime", "updated_at": "datetime" }` | Met à jour un aliment.   | Admin              |
| `/api/aliments/{id}/` | DELETE | None                                                         | `{ "success": true }`                                        | Supprime un aliment.     | Admin              |

##### 		8.7.2 Codes erreur

| Endpoint              | Method | Codes d'Erreur Possibles                                     |
| --------------------- | ------ | ------------------------------------------------------------ |
| `/api/aliments/`      | GET    | **401** : Non authentifié.                                   |
| `/api/aliments/`      | POST   | **400** : `name` ou `supplier` manquant. **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Fournisseur non trouvé. |
| `/api/aliments/{id}/` | GET    | **401** : Non authentifié. **404** : Aliment non trouvé.     |
| `/api/aliments/{id}/` | PUT    | **400** : Données invalides. **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Aliment ou fournisseur non trouvé. |
| `/api/aliments/{id}/` | DELETE | **401** : Non authentifié. **403** : Rôle insuffisant. **404** : Aliment non trouvé. **409** : L'aliment ne peut pas être supprimé car il est référencé par des nourrissages. |

#### 	8.8.**Nourrissages**

##### 		8.8.1 Routes API

| Endpoint                  | Method | Input Format (JSON)                                       | Output Format (JSON)                                         | Description                                                  | Roles Authorized   |
| ------------------------- | ------ | --------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------ |
| `/api/nourrissages/`      | GET    | None                                                      | `[{ "id": "uuid", "pond": { "id": "uuid", "name": "string" }, "food": { "id": "uuid", "name": "string" }, "quantity": "float", "feeding_date": "datetime", "recorded_by": { "id": "uuid", "email": "string" }, "created_at": "datetime", "updated_at": "datetime" }]` | Liste tous les nourrissages (filtrés par utilisateur si Gérant). | Admin, utilisateur |
| `/api/nourrissages/`      | POST   | `{ "pond": "uuid", "food": "uuid", "quantity": "float" }` | `{ "id": "uuid", "pond": "uuid", "food": "uuid", "quantity": "float", "feeding_date": "datetime", "recorded_by": "uuid", "created_at": "datetime", "updated_at": "datetime" }` | Crée un nouveau nourrissage.                                 | Admin, Utilisateur |
| `/api/nourrissages/{id}/` | GET    | None                                                      | `{ "id": "uuid", "pond": { "id": "uuid", "name": "string", "site": { "id": "uuid", "name": "string" } }, "food": { "id": "uuid", "name": "string", "supplier": { "id": "uuid", "name": "string" } }, "quantity": "float", "feeding_date": "datetime", "recorded_by": { "id": "uuid", "email": "string", "role": "string" }, "created_at": "datetime", "updated_at": "datetime" }` | Détail d'un nourrissage.                                     | Admin, Utilisateur |
| `/api/nourrissages/{id}/` | PUT    | `{ "quantity": "float" }`                                 | `{ "id": "uuid", "pond": "uuid", "food": "uuid", "quantity": "float", "feeding_date": "datetime", "recorded_by": "uuid", "created_at": "datetime", "updated_at": "datetime" }` | Met à jour un nourrissage (quantité uniquement).             | Admin, Utilisateur |
| `/api/nourrissages/{id}/` | DELETE | None                                                      | `{ "success": true }`                                        | Supprime un nourrissage.                                     | Admin              |

##### 		8.8.2 Codes erreur

| Endpoint                  | Method | Codes d'Erreur Possibles                                     |
| ------------------------- | ------ | ------------------------------------------------------------ |
| `/api/nourrissages/`      | GET    | **401** : Non authentifié.                                   |
| `/api/nourrissages/`      | POST   | **400** : `pond`, `food`, ou `quantity` manquant ou invalide. **401** : Non authentifié. **404** : Bassin ou aliment non trouvé. |
| `/api/nourrissages/{id}/` | GET    | **401** : Non authentifié. **403** : Utilisateur non autorisé à voir ce nourrissage (ex: un gérant essaie d'accéder à un nourrissage qu'il n'a pas enregistré). **404** : Nourrissage non trouvé. |
| `/api/nourrissages/{id}/` | PUT    | **400** : `quantity` invalide. **401** : Non authentifié. **403** : Utilisateur non autorisé. **404** : Nourrissage non trouvé. |
| `/api/nourrissages/{id}/` | DELETE | **401** : Non authentifié. **403** : Rôle insuffisant ou utilisateur non autorisé. **404** : Nourrissage non trouvé. |

#### 8.10  Exemples de Requêtes POST/PUT

##### **Créer un Nourrissage (`POST /api/nourrissages/`)**

###### **Requête** :

```json
{
    "pond": "550e8400-e29b-41d4-a716-446655440000",
    "food": "e5f6g7h8-e89b-41d4-a716-446655440000",
    "quantity": 2.5
}
```

###### **Réponse (201 Created)** :

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

