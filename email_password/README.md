# Authentification étendue avec email & mot de passe (expansion V2 - cloud)

Ce projet a été développé pour fonctionner en environnement local, sans authentification par mot de passe ni envoi d’emails.

Ce dossier contient toutes les modifications et ajouts nécessaires pour intégrer une gestion complète des emails et mots de passe à l’application. Bien que cette fonctionnalité ne soit pas utilisée dans la configuration actuelle en local, elle a été intégrée de manière préparatoire pour une future configuration déployée sur le cloud (V2).

## Pourquoi ?

Dans un environnement local, la gestion complète des utilisateurs par email, mot de passe et réinitialisation n’est pas indispensable car :

- L’authentification par mot de passe n’est pas essentielle, car l’accès est restreint à une seule personne ou à un petit environnement de test.
- Il n’y a pas besoin de sécurité renforcée ou de processus de récupération.
- L’envoi d’emails nécessite une configuration SMTP, souvent fastidieuse à mettre en place localement et inutile si personne ne consulte les mails générés.

Mais, dans une version déployée sur le cloud, ces fonctionnalités sont essentielles :
- Sécurité renforcée par mot de passe hashé.
- Réinitialisation du mot de passe via email.
- Gestion complète des utilisateurs via API REST.
- Envoi d’emails sécurisé via SMTP.

C’est pourquoi toute la structure nécessaire a été mise en place dès maintenant, même si elle est désactivée ou inutilisée localement.

## Architecture

```bash
email_password/
├── crud/
│   ├── user.py                   # Ajout des variables email et password
│   └── password_reset.py         # Fonctions pour gestion de réinitialisation
├── models/
│   └── user.py                   # Ajout des colonnes 'email' et 'hashed_password'
├── routes/
│   ├── user.py                   # Ajout des variables email et password
│   └── password_reset.py         # Routes API : demande & confirmation reset
├── schemas/
│   ├── user.py                   # Pydantic : email, password
│   └── password_reset.py         # Pydantic : request / confirm reset
├── streamlit_app/
│   ├── account.py                # Ajout des variables email et password dans l'interface de compte
│   ├── forgot_password.py        # Interface demande de reset (email)
│   ├── reset_password.py         # Interface saisie nouveau mot de passe
│   └── main_app.py               # Ajout des variables email et password dans la logique Streamlit
├── utils/
│   ├── auth.py                   # Ajout du hash / vérification des mots de passe
│   └── email.py                  # Envoi de mail via SMTP (reset password)
├── main.py                       # Inclusion du router password_reset
├── requirements.txt              # Inclusion de pydantic[email]
└── .env                          # Variables d’environnement SMTP & sécurité
```

## Fonctionnalités disponibles mais non actives en local

- Création de compte avec email et mot de passe.
- Connexion par mot de passe (stocké hashé avec bcrypt).
- Réinitialisation de mot de passe par lien envoyé par email.
- Validation du token de reset avec expiration.
- Redirection automatique de Streamlit vers la page de reset si le token est détecté dans l’URL.

## Ce qui a été préparé

### Routes API

Deux routes REST ont été créées via FastAPI pour la gestion du mot de passe :

- POST /password-reset/request-password-reset
Permet de générer un token sécurisé JWT et d’envoyer un lien de réinitialisation à l’email de l’utilisateur.

- POST /password-reset/reset-password
Permet à l’utilisateur de soumettre un nouveau mot de passe en fournissant un token JWT valide.

### Gestion du token sécurisé (JWT)

Un token de réinitialisation est généré à l’aide de la fonction create_access_token et contient le nom d’utilisateur (sub) en payload.
Il est valide pendant une durée configurable (RESET_TOKEN_EXPIRE_MINUTES dans le fichier .env).

### Système d’email intégré

Un module utils/email.py a été implémenté pour envoyer des emails via SMTP Gmail en SSL.
Le message contient un lien sécurisé redirigeant vers le frontend Streamlit pour saisir un nouveau mot de passe.

Variables d’environnement utilisées :

- SMTP_USER : email d’envoi
- SMTP_PASSWORD : mot de passe/clé d’application Gmail
- FRONTEND_RESET_URL : URL du frontend (ex : http://localhost:8501)
- RESET_TOKEN_EXPIRE_MINUTES : durée de validité du token (en minutes)

Si ces variables  ne sont pas définies, les routes d’envoi d’email ne fonctionneront pas, mais l’application ne plantera pas.

### Frontend Streamlit

Deux modules Streamlit ont été développés :

- forgot_password.py : permet de saisir son adresse email pour demander une réinitialisation.
- reset_password.py : permet de saisir un nouveau mot de passe via un lien contenant un token (?token=...).

Ces modules sont intégrés dans la logique de navigation de main_app.py, mais leur affichage dépend de l’état de l’application (reset_requested ou présence du token dans l’URL).

### Backend SQL

Le modèle User contient les champs email et password, ainsi que la logique pour les stocker de manière sécurisée via hash_password().

Les fonctions suivantes sont disponibles dans crud/password_reset.py :
- get_user_by_email
- get_user_by_username
- update_user_password