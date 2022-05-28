# Présentation

Cette application a pour but de fournir une visualisation pour déclarer ses cessions de cryptomonaies dans les formulaires d'impôts français.

L'auteur de l'application ne garantit pas que les informations calculées soient exactes, il appartient à l'utilisateur de vérifier les résultats obtenus.

# Installation

Installez python 3.

Depuis le dossier où vous avez cloné le dépôt :


Exécutez les commandes suivantes :

```
pip install django django-extensions pycoingecko
django-admin startproject mysite .
```

Dans le fichier mysite/settings.py

- ajouter `'django_extensions'` dans INSTALLED_APPS
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

Il faut rechercher les commentaires `#TODO` pour repérer où modifier des paramètres dans les scripts.

## gettrades

Ajouter les paramètres d'API crypto.com. Il est possible de les stocker dans le gestionnaire d'identités windows.

Optionnel : Ajouter des dépôts à ignorer, s'ils sont déja pris en compte par un autre script.

## importcryptoapp

Rien.

## importcryptoexchange

## importnexo

## importuphold

# Ajout des données

Les donnèes peuvent être ajoutées en exécutant :

```
python manage.py runscript [scriptname]
```

À l'exception de gettrades, les scripts suppriment et recréent les données dans la base de données.

## gettrades

Ce script permet de récupérer les dernières transactions réalisées sur Crypto.com Exchange.

## importcryptoapp

Ce script permet d'importer les données provenant de l'export CSV de Crypto.com App.

## importcryptoexchange

## importnexo

## importuphold

# Lancement du site

Exécutez la commande suivante :

```
python manage.py runserver
```

Se rendre à l'url [http://localhost:8000/crypto/]

# Interface