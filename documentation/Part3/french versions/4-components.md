## 4. **Conception des Composants, Classes et Base de Données**

### 	4.1 **Composants**

#### 		**A. Pages Principales**

| Page                         | Description                                                  | Composants UI Associés                                       |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Page de Connexion**        | Authentification des utilisateurs (Admin/Utilisateur).       | Formulaire de connexion, messages d'erreur.                  |
| **Gestion des Sites**        | Liste, création, et modification des sites.                  | Tableau des sites, formulaire d’édition, boutons d’action.   |
| **Gestion des Bassins**      | Liste des bassins par site.                                  | Tableau des bassins, formulaire d’édition, filtres par site. |
| **Gestion des Lots**         | Liste des lots de poissons, avec détails (espèce, quantité, bassin). | Tableau des lots, formulaire de création/modification, filtres par espèce/bassin. |
| **Gestion des Espèces**      | Liste et gestion des espèces de poissons.                    | Tableau des espèces, formulaire d’édition.                   |
| **Gestion des Fournisseurs** | Liste et gestion des fournisseurs d’aliments.                | Tableau des fournisseurs, formulaire d’édition.              |
| **Gestion des Aliments**     | Liste des aliments (liés aux fournisseurs).                  | Tableau des aliments, formulaire d’édition.                  |
| **Nourrissages**             | Enregistrement et historique des nourrissages.               | Tableau des nourrissages, formulaire d’enregistrement, filtres par date/bassin. |

---

#### 		**B. Composants Réutilisables**

| Composant              | Description                                                  | Utilisation                                                  |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Sidebar**            | Barre de navigation principale (liens vers les pages).       | Inclus dans `base.html` (héritage Django).                   |
| **Tableau de Données** | Affichage sous forme de tableau (avec pagination, tri).      | Utilisé dans les pages de liste (sites, bassins, lots, etc.). |
| **Formulaire**         | Formulaire générique pour la création/modification d’entités. | Réutilisé pour les sites, bassins, lots, etc.                |
| **Modal**              | Fenêtre modale pour les confirmations ou formulaires rapides. | Suppression d’un site, confirmation d’une action.            |
| **Messages Flash**     | Affichage des messages de succès/erreur (ex: "Lot créé avec succès"). | Inclus dans `base.html` via `{% if messages %}`.             |
| **Filtres**            | Barre de filtres pour les tableaux (par date, site, espèce, etc.). | Utilisé dans les pages de liste (lots, nourrissages).        |
| **Breadcrumbs**        | Fil d’Ariane pour la navigation (ex: Accueil > Sites > Bassin X). | Inclus dans `base.html`.                                     |

## **2. Décrire les Interactions entre Composants**

Pour chaque page,  les composants interagissent entre eux et avec le back-end (Django/DRF). Voici un exemple concret :

------

### **A. Page de Connexion (`login.html`)**

- **Composants** :
  - Formulaire de connexion (`<form>` avec champs `email`/`password`).
  - Lien vers "Mot de passe oublié" (optionnel pour le MVP).
  - Messages d’erreur (ex: "Email ou mot de passe incorrect").
- **Interactions** :
  1. L’utilisateur remplit le formulaire et clique sur "Se connecter".
  2. **JS Vanilla** :
     - Valide les champs (non vides, format email).
     - Envoie une requête `POST` à `/api/auth/login/` avec `fetch()`.
  3. **Back-end (Django)** :
     - Retourne un **token** en cas de succès (stocké dans `localStorage`).
     - Retourne une **erreur 401** si les identifiants sont invalides.
  4. **Front-end** :
     - Redirige vers le tableau de bord en cas de succès.
     - Affiche un message d’erreur sinon.

### **B. Gestion des Nourrissages (`repas.html`)**

- **Composants** :
  - **Tableau des Nourrissages** : Avec filtres (date, bassin, aliment).
  - **Formulaire d’Enregistrement** : Sélection du bassin, de l’aliment, et quantité.
  - **Bouton "Exporter"** : Pour exporter en CSV (optionnel pour le MVP).
- **Interactions** :
  1. **Chargement initial** :
     - Récupère les nourrissages via `GET /api/nourrissages/`.
     - Récupère les bassins et aliments pour les filtres/dropdowns.
  2. **Enregistrement** :
     - Soumet le formulaire via `POST /api/nourrissages/`.
     - Recharge le tableau après succès.
  3. **Filtrage** :
     - Envoie une requête filtrée (ex: `GET /api/nourrissages/?pond_id=XXX`).
