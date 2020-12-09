============
INSTALLATION
============
.. image:: http://geonature.fr/img/logo-pne.jpg
    :target: http://www.ecrins-parcnational.fr



Installation de l'environnement logiciel
=========================================

::

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install postgresql-12
    sudo apt-get install postgis postgresql-12-postgis-3
    sudo apt-get install python3.6
    sudo apt-get install python3.6-venv



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

**1. Configuration de l'application :**

Copier et éditer le fichier de configuration ``./conf.py.tpl``.

::

 cp ./conf.py.tpl ./conf.py

- Vérifier que la variable 'SQLALCHEMY_DATABASE_URI' contient les bonnes informations de connexion à la base
- Renseigner les autres paramètres selon votre contexte


**2. installer l'application :**


::

  python3.6 -m venv venv
  source venv/bin/activate
  pip install -r ./requirements.txt
  deactivate


Import des données des capteurs (csv file)
=========================================

::

    source venv/bin/activate
    python3 import.py file_path.csv
    deactivate


Si les valeurs des champs ``lat``, ``lon``, ``altitude``, ``ttf`` et ``nb_sat`` de certaines lignes à importer sont vides, alors la valeur ``none`` est renseignée automatiquement et le champs ``accurate`` est renseigné à ``false``.

Pour les autres, le champs ``accurate`` est renseigné à ``true`` par défaut dans la BDD. Il n'y a pas d'autres règles actuellement permettant de renseigner le champs ``accurate`` en fonction de la précision des données. 

Mode developpement
=========================================

::

    source venv/bin/activate
    FLASK_APP=./app FLASK_DEBUG=1 flask run
