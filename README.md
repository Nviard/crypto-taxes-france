# Présentation

Cette application a pour but de fournir une visualisation pour déclarer ses cessions de cryptomonaies dans les formulaires d'impôts français.

L'auteur de l'application ne garantit pas que les informations calculées soient exactes, il appartient à l'utilisateur de vérifier les résultats obtenus.

# Installation

Installez python 3.

Depuis le dossier où vous avez cloné le dépôt :


Exécutez les commandes suivantes :

```
pip install django
django-admin startproject mysite .
```

Dans le fichier mysite/settings.py

- ajouter `'crypto'` dans INSTALLED_APPS
- remplacer la valeur de LANGUAGE_CODE par `'fr-fr'`
- remplacer la valeur de TIME_ZONE par `'Europe/Paris'`

Dans le fichier mysite/urls.py

- ajouter `from django.urls import include`
- ajouter `path("crypto/", include("crypto.urls"))` dans urlpatterns

Exécutez la commande suivante :

```
python manage.py migrate
```

# Paramètrage


# Ajout des données


# Lancement du site

Exécutez la commande suivante :

```
python manage.py runserver
```

Se rendre à l'url [http://localhost:8000/crypto/]

# Interface