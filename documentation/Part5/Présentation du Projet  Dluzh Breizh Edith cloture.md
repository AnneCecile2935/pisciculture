# Présentation du Projet : Dluzh Breizh Edith
*Outil de gestion centralisée pour les petites entreprises piscicoles – Version 0.1.0*

---

## **1. Introduction**
### **Contexte et Équipe**
- **Porté par** : Anne-Cécile Colleter (développeuse full-stack, spécialisation en solutions techniques pour la pisciculture).
- **Problématique** :
  - Les pisciculteurs bretons utilisent encore des **classeurs papier ou tableaux velleda** pour suivre leurs lots, avec des risques d’erreurs et une perte de temps estimée à **15-20%**.
  - Besoin criant de **traçabilité sur 3 ans** (obligations réglementaires) et d’outils adaptés aux petites structures.
- **Objectifs du MVP** :
  - Remplacer les méthodes manuelles par une **solution numérique centralisée**.
  - Automatiser le suivi des **bassins, lots de poissons, et actions quotidiennes** (alimentation, mortalités, traitements).
  - **Cible** : Piscicultures de moins de 5 salariés, avec un focus sur la simplicité d’utilisation.

### **Solution proposée**
Une application web (Django + Bootstrap) permettant :
- La **création et le suivi des lots** (espèces, quantité, croissance).
- Un **tableau de bord interactif** pour visualiser l’état des bassins et les actions récentes.
- Une **gestion multi-utilisateurs** (rôles Admin/User) pour les équipes réduites.

> *"Un outil conçu par et pour les pisciculteurs, sans jargon superflu."*

---

## **2. Processus du Projet**
### **Étapes clés et Livrables**
| Étape        | Durée       | Livrables principaux                                    | Défis rencontrés                                             |
| ------------ | ----------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| **Idéation** | 13-29/08    | Charte projet, maquettes, interviews utilisateurs       | Définir un scope réaliste pour un MVP solo.                  |
| **Backend**  | 29/08-15/09 | Modèles Django (Bassin, Lot, Espèce, Action), APIs CRUD | Gestion des relations complexes (ex: Lot ↔ Bassin).          |
| **Frontend** | 16/09-03/11 | Tableau de bord, formulaires de saisie                  | Design responsive pour tablettes (utilisation en extérieur). |
| **Tests**    | 06/10-07/11 | Correction de bugs, optimisation UX                     | Priorisation des bugs avec la méthode P0/P1/P2.              |

### **Choix techniques**
- **Backend** : Django (Class-Based Views) pour une maintenance facile et une scalabilité future.
- **Frontend** : Bootstrap pour un design **intuitif et adaptatif** (utilisable en extérieur, sur tablette).
- **Base de données** : PostgreSQL pour gérer les **données historiques sur 3 ans**.
- **Fonctionnalité phare** :
  - **Tableau de bord** avec visualisation des actions par bassin (alimentation, mortalités).
  - **Historique des lots** : Suivi de la quantité initiale vs. actuelle, avec calcul automatique des pertes.

---

## **3. Démo Technique**
### **Architecture simplifiée**
```plaintext
Utilisateur → Frontend (Bootstrap) ↔ Backend (Django) ↔ Base de données (PostgreSQL)
```



- **Extraits de code à montrer** :
  - Vue `BassinDetail` (front) + API `LotListCreate` (back).
  - Modèle `Lot` avec champ `quantité_initial` et historique des actions.

### **Démonstration en direct** (10 min max)

1. **Création d’un lot** : Saisie des données (espèce, bassin, quantité).
2. **Suivi alimentaire** : Ajout d’une action + visualisation dans le tableau de bord.

### **3.1. Rôle Administrateur**
*Configuration initiale des données.*
- [Capture 1 : Création d’un utilisateur](#)
  > ![Admin - Utilisateur](images/admin_user.png)
  > *Légende : Formulaire de création avec sélection du rôle (Admin/User).*

### **3.2. Rôle Utilisateur**
*Workflow quotidien : création de lot → action → historique.*

1. **Tableau de bord**
   > ![User - Tableau de bord](images/user_dashboard.png)
   > *Légende : Vue d’ensemble avec alertes visuelles (couleurs).*

2. **Création d’un lot**
   > ![User - Nouveau lot](images/user_nouveau_lot.png)
   > *Légende : Sélection de l’espèce et du bassin. La quantité initiale est validée.*

3. **Ajout d’une action**
   > ![User - Action](images/user_action.png)
   > *Légende : Enregistrement d’une alimentation avec validation du `code_alim`.*

4. **Historique et calculs**
   > ![User - Historique](images/user_historique.png)
   > *Légende : Liste des actions et quantité actuelle recalculée.*

### **3.3. Validations Techniques**
*Exemples de code pour les fonctionnalités clés.*
```python
# Validation du code_alim (TODO ⭐⭐⭐)
def clean_code_alim(self):
    code_alim = self.cleaned_data.get("code_alim")
    if not code_alim.isalnum():
        raise forms.ValidationError("Format invalide.")
    return code_alim.upper()
```



------

## **4. Résultats & Métriques**

| Objectif initial             | Résultat obtenu                            | Écart/Explication                                        |
| ---------------------------- | ------------------------------------------ | -------------------------------------------------------- |
| 100% des fonctionnalités MVP | 90% (manque : export PDF des rapports)     | Priorisation des bugs critiques (ex: calcul des stocks). |
| Interface "intuitive"        | 8/10 en test utilisateur (3 pisciculteurs) | Feedback : Ajouter un tutoriel vidéo.                    |
| Réduction du temps de saisie | -30% (estimé via tests utilisateurs)       | Gain confirmé pour la traçabilité.                       |

**Témoignage utilisateur** :

*"Avec Dluzh Breizh Edith, je vois en un coup d’œil quel bassin nécessite une attention particulière. Plus besoin de recopier mes notes papier et mon tableau Velleda!"* 



## **5. Rétrospective et feuille de route

### **Succès**

✅ **Gestion de projet** :

- Utilisation de **GitHub Projects** pour suivre les issues/milestones → meilleure visibilité.
- **Méthode P0/P1/P2** efficace pour prioriser les bugs.

✅ **Technique** :

- Les **Class-Based Views** de Django ont accéléré le développement des APIs.
- Intégration de la météo : **valeur ajoutée majeure** pour les utilisateurs.

### **Défis & Améliorations**

⚠ **Défis** :

- **Base de données** : Problèmes de migrations avec `db_test` → solution : script de reset automatisé.
- **Anglais** : Difficulté à rédiger la documentation technique → utilisation de DeepL + relecture.
- **Solo** : Charge de travail sous-estimée pour les tests → prévoir +20% de temps dans les prochains projets.

🔧 **Améliorations futures** :

- Automatiser les tests unitaires (coverage < 50%).

- **Intégration de l’API météo** (prévue pour Q1 2026) : alertes température/précipitations.

- **Export PDF** des rapports pour les contrôles réglementaires.

- **Version 0.2.0** : Ajouter un système de notifications push pour les alertes.

  ##### **Exemple de TODO Technique (Extrait : Formulaire Aliment)**
  Pour illustrer la méthode de suivi des améliorations, voici un extrait du fichier `TODO.md` dédié aux **formulaires** (priorisé avec ⭐⭐⭐/⭐⭐/⭐) :

  | Priorité | Tâche                            | Description                                                  | Statut  | Code/Exemple                                                 |
  | -------- | -------------------------------- | ------------------------------------------------------------ | ------- | ------------------------------------------------------------ |
  | ⭐⭐⭐      | Validation serveur (`code_alim`) | Ajouter `RegexValidator` pour limiter à 6 caractères alphanumériques majuscules. | À faire | `python\nvalidators=[RegexValidator(regex='^[A-Z0-9]{6}$', message='Code invalide.')]` |
  | ⭐⭐⭐      | Normalisation automatique        | Convertir `code_alim` en majuscules via `clean_code_alim()`. | À faire | `python\ndef clean_code_alim(self):\n    return self.cleaned_data["code_alim"].upper()` |
  | ⭐⭐⭐      | Filtrage des fournisseurs actifs | Limiter le `queryset` aux fournisseurs `est_actif=True` dans `__init__`. | À faire | `python\nself.fields["fournisseur"].queryset = ...filter(est_actif=True)` |
  | ⭐⭐⭐      | Validation JS en temps réel      | Limiter à 6 caractères + conversion en majuscules.           | À faire | `javascript\ndocument.getElementById('id_code_alim').addEventListener('input', ...)` |
  | ⭐⭐       | Amélioration du template         | Afficher `help_text` et erreurs avec Bootstrap.              | À faire | `html\n...`                                                  |
  | ⭐        | Tests unitaires                  | Valider codes invalides, fournisseurs inactifs, champs obligatoires. | Backlog | `python\nclass AlimentFormTest(TestCase):\n    def test_code_alim_invalid(self):...` |

> 

------

## **6. Conclusion & Perspectives**

### **Bilan**

- **MVP fonctionnel** : Preuve de concept validée par les tests utilisateurs.
- **Prochaines étapes** :
  - Finaliser l’export PDF (priorité P0).
  - Rechercher des partenariats avec des stations météo locales.
  - **Objectif long terme** : Devenir la référence des outils piscicoles en Bretagne.

### **Remerciements**

- Holberton pour l’accompagnement technique.
- Les pisciculteurs testeurs (nommer les structures si accord).
- [Ton fils] pour sa patience pendant les weekends de dev 😉.



# **Annexes (pour le rapport final)**

## **Rétrospective détaillée**

### **Ce qui a bien fonctionné**

- **Outils** :
  - GitHub Projects + labels P0/P1/P2 → clarté totale.
  - Trello pour les idées "hors scope" (backlog).
- **Méthode** :
  - Développement par petites itérations (1 fonctionnalité = 1 commit).
  - Veilles techno hebdomadaires (ex: librairies Django pour la météo).

### **Ce à améliorer**

| Problème                 | Solution proposée                                    | Responsable |
| ------------------------ | ---------------------------------------------------- | ----------- |
| Tests insuffisants       | Intégrer GitHub Actions pour des tests automatiques. | Moi         |
| Documentation en anglais | Créer un glossaire technique FR/EN.                  | Moi         |
| Charge de travail solo   | Prévoir un·e contributeur·rice pour la V0.2.         | À recruter  |