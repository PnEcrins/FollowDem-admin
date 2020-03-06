============
INSTALLATION
============
.. image:: http://geonature.fr/img/logo-pne.jpg
    :target: http://www.ecrins-parcnational.fr


Création de la base de données PostgreSQL
=========================================

**1. Modification du fichier de configuration**

* Créer le fichier de configuration à partir du template 'settings.ini.tpl':

::

  cd ./install
  cp settings.ini.tpl settings.ini


* Ajouter les informations dans le fichier settings.ini pour se connecter à la base de données 



**2. Création de la base de données 'followdem' et du schéma 'utilisateur'**


* Rendre le fichier exécutable 'install_db_postgres.sh'

::

    chmod +x ./install_db_postgres.sh


* Lancer le script d'Installation

::

    ./install_db_postgres.sh



Installation de l'application
=========================================

**1. Installation de l'environnement logiciel**
::

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install postgresql postgresql-contrib postgis postgresql-9.6-postgis-2.3 postgresql-9.6-postgis-2.3-scripts
    sudo apt-get install python3
    sudo apt-get install python3-venv


**2. Configuration de l'application :**

Copier et éditer le fichier de configuration ``./conf.py.tpl``.

::

 cp ./conf.py.tpl ./conf.py

- Vérifier que la variable 'SQLALCHEMY_DATABASE_URI' contient les bonnes informations de connexion à la base
- Renseigner les autres paramètres selon votre contexte


**3. installer l'application :**

::

  python3 -m venv venv
  source venv/bin/activate
  pip install -r ./requirements.txt
  deactivate


Import des données des capteurs (csv file)
=========================================

::

    python import.py file_path.csv


Mode developpement
=========================================

::

    source venv/bin/activate
    FLASK_APP=./appy FLASK_DEBUG=1 flask run
