## **Rapport de Sprints – Projet Pisciculture (MVP)**
**Contexte** : Développement d’une application de gestion piscicole avec Django, PostgreSQL et Bootstrap.
**Méthodologie** : Approche agile en sprints de 1 à 2 semaines, avec priorisation P0/P1/P2 et traçabilité via GitHub.
**Objectif global** : Livrer un MVP fonctionnel pour enregistrer les nourrissages, gérer les sites/bassins, et fournir une interface utilisateur intuitive.

**Livrables clés** :
- Modèles Django pour Site, Bassin, Espèce, Aliment, Nourrissage, LotDePoisson.
- Interface utilisateur dynamique (DataTables, formulaires, sidebar).
- Tests unitaires et d’intégration (pytest, factory_boy).
- Documentation technique et utilisateur.

**Lien vers le dépôt** : [GitHub – Pisciculture](https://github.com/AnneCecile2935/pisciculture)
**Lien vers le GitHub Project** : [Tableau des sprints](https://github.com/users/AnneCecile2935/projects/3)

## **Sprint 1 : Core Functionality (Nourrissage, Sites, Bassins, Espèces)**

**Durée** : 2 semaines (ex : 2025-09-01 → 2025-09-14) **Objectif** : Mettre en place les modèles de base, les formulaires et les vues pour les fonctionnalités principales.

### **Tâches et Preuves**



# Sprint 1 - Détail

| Tâche                                  | Priorité | Durée | Statut  | Preuve                                              | Lien vers le code/test                                       |
| -------------------------------------- | -------- | ----- | ------- | --------------------------------------------------- | ------------------------------------------------------------ |
| Initialiser le projet Django           | P0       | 1j    | Terminé | Configuration de base, Docker, PostgreSQL.          | [e9339ff](https://github.com/AnneCecile2935/pisciculture/commit/e9339ffabc7c48d7ecea1c436e7281434bf289e8)                 |
| Créer les modèles Site, Bassin, Espece | P0       | 2j    | Terminé | Modèles avec relations ForeignKey.                  | [30b8c63](https://github.com/AnneCecile2935/pisciculture/commit/30b8c63de54c02173677dd2cb1534772b0bbee63)                 |
| Configurer l'admin pour Site et Bassin | P1       | 1j    | Terminé | Personnalisation de l'interface admin.              | [fba60a9](https://github.com/AnneCecile2935/pisciculture/commit/fba60a963487abbaf740374efe489fc01531fbc3)                 |
| Implémenter le modèle LotDePoisson     | P1       | 1j    | Terminé | Modèle avec calcul automatique du poids moyen.      | [b5c8cc2](https://github.com/AnneCecile2935/pisciculture/commit/b5c8cc28f27786e2572e29d56748289d931ce548)                 |
| Ajouter le modèle Aliment              | P1       | 1j    | Terminé | Modèle avec relation vers Fournisseur.              | [c693e75](https://github.com/AnneCecile2935/pisciculture/commit/c693e75cb8f96019faa707135db698e8598047e0)                 |
| Configurer les permissions admin       | P1       | 0.5j  | Terminé | Permissions personnalisées pour les admins.         | [fba60a9](https://github.com/AnneCecile2935/pisciculture/commit/fba60a963487abbaf740374efe489fc01531fbc3)                 |
| Corriger les erreurs de migration      | P1       | 0.5j  | Terminé | Résolution des conflits de base de données.         | [f4849cc](https://github.com/AnneCecile2935/pisciculture/commit/f4849cc7596da7597080b01609e3970118ed8ce2)                 |
| Ajouter des tests pour les modèles     | P2       | 1j    | Terminé | Tests unitaires pour Site, Bassin, Espece, Aliment. | [617edf4](https://github.com/AnneCecile2935/pisciculture/commit/617edf4d00e3d584fee32ae6443dc88cef8a887d), [6ee50ec](https://github.com/AnneCecile2935/pisciculture/commit/6ee50ec599544683bcda9809ee593f18fe13cfba) |

### **Blocages et Solutions**

- **Problème** : Conflits de migration pour les modèles Site et Bassin. **Solution** : Réinitialisation des migrations et correction des champs. **Preuve** : [f4849cc](lien).
- **Problème** : Erreurs de syntaxe dans les modèles. **Solution** : Correction des champs et relations. **Preuve** : [a0cb881](lien).

------

## **Sprint 2 : Nourrissage et Interface Utilisateur**

**Durée** : 2 semaines (ex : 2025-09-15 → 2025-09-28) **Objectif** : Implémenter le module de nourrissage, améliorer l'interface utilisateur et ajouter des tests.

### **Tâches et Preuves**

# Sprint 2 - Détail

| Tâche                                    | Priorité | Durée | Statut  | Preuve                                                       | Lien vers le code/test                                       |
| ---------------------------------------- | -------- | ----- | ------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Ajouter le modèle Nourrissage            | P0       | 1j    | Terminé | Modèle pour enregistrer les repas des poissons.              | [8b4678e](https://github.com/AnneCecile2935/pisciculture/commit/8b4678e3a024ae371f1413a2fa13c8eea93e5d0c)                 |
| Configurer les URLs pour Nourrissage     | P0       | 0.5j  | Terminé | Ajout des routes pour le CRUD.                               | [430cd3c](https://github.com/AnneCecile2935/pisciculture/commit/430cd3c9c2c4fbc95d0154eca5210af6f311f2c8)                 |
| Créer les templates pour Nourrissage     | P0       | 1j    | Terminé | Templates pour l'affichage et la saisie des repas.           | [7746576](https://github.com/AnneCecile2935/pisciculture/commit/774657628c22738c7df9b5c653fc8b6f85d5f4a9)                 |
| Implémenter le formulaire de nourrissage | P0       | 2j    | Terminé | Formulaire pour enregistrer les repas par bassin.            | [0f2fa07](https://github.com/AnneCecile2935/pisciculture/commit/0f2fa0766c3828d3b556923071da46271df23647)                 |
| Ajouter DataTables pour les listes       | P1       | 2j    | Terminé | Intégration de DataTables pour les listes dynamiques.        | [868d3af](https://github.com/AnneCecile2935/pisciculture/commit/868d3af9346c32602c1203cda334ff3100ce612b), [260e0cf](https://github.com/AnneCecile2935/pisciculture/commit/260e0cf4e53c512b3ef5cb372199c1bfb40e1ccd) |
| Améliorer le layout et le sidebar        | P1       | 1j    | Terminé | Ajout de sous-menus et de styles pour le sidebar.            | [d4f2de2](https://github.com/AnneCecile2935/pisciculture/commit/d4f2de2e453c73c6c463ff74d8df8f1335fc96b9)                 |
| Ajouter des tests pour Nourrissage       | P1       | 1j    | Terminé | Tests unitaires et d'intégration pour le module Nourrissage. | [0f2fa07](https://github.com/AnneCecile2935/pisciculture/commit/0f2fa0766c3828d3b556923071da46271df23647)                 |
| Corriger les widgets de formulaire       | P2       | 0.5j  | Terminé | Correction des messages d'erreur et des widgets.             | [5fd6ff2](https://github.com/AnneCecile2935/pisciculture/commit/5fd6ff282bce3899015cfd4d1415c5346ab1f90fn)                 |

### **Blocages et Solutions**

- **Problème** : Affichage incorrect des DataTables. **Solution** : Correction des templates et des appels AJAX. **Preuve** : [868d3af](lien).
- **Problème** : Messages d'erreur non clairs dans les formulaires. **Solution** : Standardisation des messages et des classes CSS. **Preuve** : [5fd6ff2](lien).

------

## **Sprint 3 : Améliorations et Tests Complets**

**Durée** : 2 semaines (ex : 2025-09-29 → 2025-10-12) **Objectif** : Finaliser les fonctionnalités, ajouter des tests complets et améliorer l'interface.

### **Tâches et Preuves**

# Sprint 3 - Détail

| Tâche                                     | Priorité | Durée | Statut  | Preuve                                                       | Lien vers le code/test                                       |
| ----------------------------------------- | -------- | ----- | ------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Ajouter un formulaire global par site     | P0       | 2j    | Terminé | Formulaire pour enregistrer les repas pour tous les bassins d'un site. | [93a9eb9](https://github.com/AnneCecile2935/pisciculture/commit/93a9eb9582d93999c7eb56faa31a6d6550955b27)                 |
| Standardiser les messages de confirmation | P0       | 0.5j  | Terminé | Messages cohérents pour la suppression et les actions.       | [626780e](https://github.com/AnneCecile2935/pisciculture/commit/626780e48d43064277872e6b41756e8a7c52f51f)                 |
| Améliorer les styles des formulaires      | P1       | 1j    | Terminé | Ajout de `form_style.css` pour une cohérence visuelle.       | [f9fc1f4](https://github.com/AnneCecile2935/pisciculture/commit/f9fc1f406a49e56c85981df390f8131fa826e161)                 |
| Intégrer DataTables pour tous les modules | P1       | 2j    | Terminé | Migration des listes statiques vers DataTables (Aliments, Fournisseurs, etc.). | [c8956b9](https://github.com/AnneCecile2935/pisciculture/commit/c8956b930ca6c141b55ca7389bf6d4a5ea84cee4), [f1b3101](https://github.com/AnneCecile2935/pisciculture/commit/f1b31016badd03ac64910a1df930790165769d67) |
| Ajouter des tests pour les vues           | P1       | 2j    | Terminé | Tests pour les vues d'authentification, utilisateurs, et nourrissage. | [edd4f21](https://github.com/AnneCecile2935/pisciculture/commit/edd4f2127cf3f867568d4cc1a160ab11edf1315c), [7813942](https://github.com/AnneCecile2935/pisciculture/commit/78139429a70030685f11ea07ffad93dcfb02b18f) |
| Configurer pytest et factory_boy          | P1       | 1j    | Terminé | Configuration des outils de test.                            | [7a23d96](https://github.com/AnneCecile2935/pisciculture/commit/7a23d96f30b5285790184ff6748623fc94a0f15f)                 |
| Corriger les bugs mineurs                 | P2       | 1j    | Terminé | Résolution des problèmes de permissions et d'affichage.      | [417a8e3](https://github.com/AnneCecile2935/pisciculture/commit/417a8e3f8331d7e706f79cdc8979c42fe702abb1)                 |

### **Blocages et Solutions**

- **Problème** : Incompatibilité des tests avec les nouvelles migrations. **Solution** : Mise à jour des factories et des fixtures de test. **Preuve** : [8cc09f9](lien).
- **Problème** : Conflits de permissions pour les utilisateurs standards. **Solution** : Utilisation de `UserPassesTestMixin` pour les vues. **Preuve** : [3a3a5de](lien).

------

## **Sprint 4 : Finalisation et Documentation**

**Durée** : 1 semaine (ex : 2025-10-13 → 2025-10-20) **Objectif** : Finaliser les dernières fonctionnalités, compléter la documentation et préparer la livraison.

### **Tâches et Preuves**

# Sprint 4 - Détail

| Tâche                                        | Priorité | Durée | Statut  | Preuve                                                       | Lien vers le code/test                                       |
| -------------------------------------------- | -------- | ----- | ------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Compléter la documentation                   | P0       | 2j    | Terminé | Ajout de diagrammes, de la documentation technique et des user stories. | [d2373e3](https://github.com/AnneCecile2935/pisciculture/commit/d2373e358f297c72a5a00a71fa4dfcb7098d0297), [14b35e7](https://github.com/AnneCecile2935/pisciculture/commit/14b35e7063765ae1fdd69fbd33f713b9f7a7170d) |
| Ajouter des tests pour les modèles manquants | P0       | 1j    | Terminé | Tests pour Fournisseurs, Stocks, Espèces.                    | [ad02410](https://github.com/AnneCecile2935/pisciculture/commit/ad024105c18808c06525fc2edf70e29e6e7cdc1d), [617edf4](https://github.com/AnneCecile2935/pisciculture/commit/617edf4d00e3d584fee32ae6443dc88cef8a887d) |
| Finaliser les graphiques DataTables          | P1       | 1j    | Terminé | Intégration de Chart.js pour les graphiques de température et d'oxygène. | [868d3af](https://github.com/AnneCecile2935/pisciculture/commit/868d3af9346c32602c1203cda334ff3100ce612b)                 |
| Corriger les bugs restants                   | P1       | 1j    | Terminé | Résolution des problèmes mineurs d'affichage et de validation. | [5fd6ff2](https://github.com/AnneCecile2935/pisciculture/commit/5fd6ff282bce3899015cfd4d1415c5346ab1f90f)                 |
| Préparer la démonstration                    | P2       | 0.5j  | Terminé | Captures d'écran et vidéo de démonstration.                  | [Lien vers captures](https://chat.mistral.ai/chat/lien)      |

### Tâches restantes :

- Implémenter le dashboard
- Ajouter catégorie de bassin (bassin ou labo)
- Pop up Aliment de suppression différente des autres
- Changement d'autorisation d'accès aux users finalement
- Ajout bouton annuler au formulaire repas par site
- Ajout * aux champs obligatoires
- Refaire les tests pour activité quotidien (depuis formulaire de saisie de repas par site fonctionnel)
- Corriger la DB de test
------

## **Rétrospective Globale**
**Ce qui a bien fonctionné** :
- Découpage des tâches en sous-tâches techniques (ex: modèle → vue → tests).
- Utilisation de DataTables pour dynamiser l’interface sans surcharge de développement.


**Axes d’amélioration** :
- **Estimation des durées** : Certaines tâches front-end (ex: styles) ont été sous-estimées. Pour le Sprint 5, j’ajouterai une marge de 20% sur les tâches UI.
- **Tests** : Automatiser davantage les tests d’intégration avec GitHub Actions.
- **Revue de code** : Intégrer des revues systématiques avant merge (même en solo, via des checklists).
