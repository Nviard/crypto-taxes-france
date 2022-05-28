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
python manage.py createsuperuser
```

Créez le nom et mot de passe de votre superutilisateur.

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

Optionnel : Ajouter des bénéfices du supercharger impossible à exporter.

## importnexo

Rien.

## importuphold

Optionnel : Gérer les envois vers un autre compte personnel (exemple commenté avec ethereum vers Crypto.com).

# Ajout des données

Les donnèes peuvent être ajoutées en exécutant :

```
python manage.py runscript [scriptname]
```

À l'exception de gettrades, les scripts suppriment et recréent les données dans la base de données.

## gettrades

Ce script permet de récupérer les dernières transactions réalisées sur Crypto.com Exchange.

## importcryptoapp

Ce script permet d'importer les données provenant de l'export CSV de Crypto.com App depuis le fichier cryptocom.csv.

## importcryptoexchange

Ce script permet d'importer les données provenant de l'export CSV de Crypto.com Exchange depuis les fichiers STAKE_INTEREST.csv et TRADE_FEE_REBATE.csv.

## importnexo

Ce script permet d'importer les données provenant de l'export CSV de Nexo depuis le fichier nexo.csv

## importuphold

Ce script permet d'importer les données provenant de l'export CSV d'Uphold depuis le fichier uphold.csv. Il remplit aussi une plateforme Cred si vous l'avez utilisé depuis Uphold.

# Lancement du site

Exécutez la commande suivante :

```
python manage.py runserver
```

Se rendre à l'url [http://localhost:8000/crypto/](Crypto)


Si vous obtenez l'erreur "Could not find coin with the given id", il faut renseigner manuellement les identifiants des monnaies dans [http://localhost:8000/admin/crypto/coin/](Coin) en se connectant avec votre superuser.

Les identifiants doivent correspondre à ceux de [https://api.coingecko.com/api/v3/coins/list](Coingecko).
Profitez en aussi pour vérifier que les monnaies fiat sont bien identifiées comme telles.

# Interface

L'url [http://localhost:8000/crypto/](Crypto) vous présente les informations utiles. Elles peuvent être filtrées par plateforme en ajoutant `/Uphold`, `/Supercharger`, `/Crypto.com Exchange`, `/Crypto.com App`, `/Cred`, `/Crypto Earn` ou `/Nexo` à la fin de l'url.

## Résumé

Donne la valeur de vos cryptomonnaies. Coût est calculé en fonction de la valeur en euros au moment de l'achat. Coût réel est calculé à partir de la proportion d'euros investis ayant servi à acquérir la monnaie.

## Historique

Donne un suivi mensuel des valeurs.

## Simulation

Donne une idée de la valeur qu'auraient eu vos cryptos en ne réalisant que 0 25 50 ou 75% des échanges entre cryptos. Gain représente le gain que vous avez ou allez réalisé en n'ayant pas simplement HODL.

## Impôts

Répertorie vos cessions et indique les valeurs à renseigner dans les formulaires de déclarations de plus values.