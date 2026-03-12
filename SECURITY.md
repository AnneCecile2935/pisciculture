# Politique de Sécurité

## 📌 Versions supportées

Ce projet est actuellement en phase de **développement actif** (MVP). Seule la version en cours de développement est supportée pour les mises à jour de sécurité.
   Version       | Supportée          | Notes                                  |
 |---------------|--------------------|----------------------------------------|
 | `main` (dev)  | :white_check_mark: | Version en développement (2025-2026). |
 | `< 1.0.0`     | :x:                | Versions antérieures non supportées.  |

*À partir de la version 1.0.0 (prévue pour avril 2026), une table détaillée des versions supportées sera mise à jour ici.*

---

## 🚨 Signaler une vulnérabilité

Si tu découvres une faille de sécurité dans **Dluzh Breizh Edith**, merci de suivre ces étapes :

1. **Ne pas créer d’issue publique** (pour éviter d’exposer la faille avant sa correction).
2. **Contacter l’équipe** :
   - Par email : [anne-cecile.colleter@live.fr](mailto:anne-cecile.colleter@live.fr)

3. **Inclure dans ton rapport** :
   - Une description claire de la vulnérabilité.
   - Les étapes pour la reproduire (si possible).
   - Ton nom ou pseudonyme (pour les crédits après correction).

### ⏳ Délai de réponse
- **Accusé de réception** sous 48h.
- **Correctif publié** sous 7 jours (selon la criticité).

### 🔍 Portée
Ce document couvre :
- Le code source du projet ([lien vers le dépôt](#)).
- Les dépendances directes (Django, PostgreSQL, etc.).
- Les données sensibles gérées par l’application (lots de poissons, utilisateurs).

---

## 🛡️ Bonnes pratiques de sécurité
- **Ne jamais commiter** de secrets (mots de passe, clés API) dans le dépôt. Utilise un fichier `.env` et ajoute-le à `.gitignore`.
- **Mettre à jour régulièrement** les dépendances via [Dependabot](https://docs.github.com/en/code-security/dependabot).
- **Vérifier les alertes de sécurité** dans l’onglet **Security** de ton dépôt GitHub.

---

## 📜 Licence
Copyright (c) [2025-2026] Anne-Cécile Colléter et Dluzh Breizh Edith.

Tous droits réservés. Aucune partie de ce projet ne peut être utilisée, modifiée ou distribuée
sans l'autorisation écrite explicite des auteurs.
