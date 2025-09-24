## 1. **User Stories**

### 1.1 **Droits utilisateurs**

| Priorité     | User story                                                   | Rôle concerné |
| ------------ | ------------------------------------------------------------ | ------------- |
| Must  Have   | En tant qu’admin,et uniquement en tant qu'admin  je veux créer/modifier/supprimer des comptes  utilisateurs afin de gérer les accès à  l’application. | Admin         |
| Must  Have   | En tant qu’admin, je veux modifier l’email et le mot de passe d’un utilisateur afin de maintenir la sécurité des comptes. | Admin         |
| Must  Have   | En tant qu’utilisateur, je veux me connecter avec mon email et mot de passe afin d’accéder à l’application. | Tous          |
| Must  Have   | En tant qu'utilisateur, je veux me déconnecter de mon compte utilisateur pour quitter l'application | Tous          |
| Should  Have | En tant qu’utilisateur, je veux réinitialiser mon mot de passe afin  de ne pas perdre l’accès à mon compte. | Tous          |
| Should  Have | En tant qu’admin, je veux attribuer des rôles (admin, gérant, utilisateur) afin de limiter les permissions. | Admin         |
| Could  Have  | En tant  qu’utilisateur, je veux recevoir un email de confirmation  après la réinitialisation de mon mot de passe. | Tous          |

### **1.2.** **Site/ Bassins **

| Priorité     | User story                                                   | Rôle concerné |
| ------------ | ------------------------------------------------------------ | ------------- |
| Must Have    | En tant  qu’admin, je veux créer/modifier/supprimer un site de production afin de structurer l’application. | Admin         |
| Must Have    | En tant  qu’admin, je veux créer/modifier/supprimer un bassin  afin de gérer les infrastructures. | Admin         |
| Must Have    | En tant  qu’utilisateur je veux voir la liste des bassins pour un  site donné afin de voir l'état de nourrissage | Tous          |
| Should  Have | En tant  qu’admin, je veux associer un bassin à un site spécifique afin d’organiser les données. | Admin         |
| Could Have   | En tant  qu’utilisateur, je veux filtrer les bassins par site pour  accéder rapidement à mes données. | Tous          |

### 1.3 **Gestion des stocks**

| Priorité     | User story                                                   | Rôle concerné |
| ------------ | ------------------------------------------------------------ | ------------- |
| Must Have    | En tant  qu’utilisateur, je veux créer un lot de poissons afin de  suivre leur croissance et leur alimentation. | Tous          |
| Must Have    | En tant  qu’utilisateur, je veux assigner un lot à un bassin afin de  localiser les poissons. | Tous          |
| Must Have    | En tant  qu’utilisateur, je veux créer/modifier/supprimer un type d’aliment afin de gérer les stocks. | Tous          |
| Should  Have | En tant  qu’utilisateur, je veux voir l’historique des lots par bassin  pour analyser la production. | Tous          |
| Could Have   | En tant  qu’utilisateur, je veux recevoir une alerte si le stock d’aliment est bas pour éviter les ruptures. | Tous          |

### 1.4 **Activité quotidienne**

| Priorité     | User story                                                   | Rôle concerné |
| ------------ | ------------------------------------------------------------ | ------------- |
| Must Have    | En tant  qu’utilisateur, je veux enregistrer un nourrissage (bassin,  aliment, quantité) afin de suivre l’alimentation. | Tous          |
| Should  Have | En tant  qu'utilisateur, je  veux visualiser l’historique des nourrissages par  bassin pour ajuster les quantités. | Tous          |

### 1.5 Fournisseurs

| Priorité   | User story                                                   | Rôle concerné |
| ---------- | ------------------------------------------------------------ | ------------- |
| Must  Have | En tant  qu’utilisateur, je veux créer/modifier/supprimer un fournisseur afin de lier l'aliment au fournisseur | Tous          |
| Must Have  | En tant  qu'utilisateur, je veux associer un aliment à un fournisseur  pour suivre les approvisionnements. | Tous          |



### 1.6  Transverse

| Priorité     | User story                                                   | Rôle concerné |
| ------------ | ------------------------------------------------------------ | ------------- |
| Should Have  | En tant  qu’utilisateur, je veux exporter les données (nourrissages, relevés) en CSV pour les analyser hors ligne. | Tous          |
| Should  Have | En tant  qu’utilisateur, je veux voir un tableau de bord avec les données clés (ex : mortalités, nourrissages). | Tous          |
| Could Have   | En tant  qu’utilisateur, je veux accéder à l’application sur mobile  pour enregistrer des données sur le terrain. | Tous          |

