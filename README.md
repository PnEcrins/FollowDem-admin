# FollowDem-admin
Backoffice de FollowDem

- Python / Flask
- Authentification : https://github.com/PnX-SI/UsersHub-authentification-module
- id_application UsersHub en paramètre
- On importe toutes les données TXT dans la BDD (PostgreSQL et si possible MySQL). 
- Des règles (nb sat, HDOP, 2D/3D, altitude, boundingbox des XY) définissent si les localisations sont utilisées ou non. Les valeurs sont paramétrables. 
- Les tables sont dans un schéma dédié, permettant de fonctionner de manière autonome ou dans une BDD existante (GeoNature notamment)
- L'appli front utilise des vues (matérialisée ou non ?).

**ADMIN**

- Une liste des animaux, une des devices. Afficher, editer, supprimer, ajouter. 
- Le détail d'un animal permet d'afficher ses associations à des devices, de les modifier et d'en ajouter.

### Install database and packages dependencies

#### Linux
```sh
sudo apt install postgresql postgresql-contrib libpq-dev postgresql-9.6-postgis-scripts git-all
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```
```sql
sudo -u postgres psql postgres
CREATE DATABASE capel;
\c followdem
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
\q
```
```sh
mkdir capel-venv
cd capel-venv
sudo /usr/bin/pip3 install virtualenv  # contemporary version:
virtualenv -p python3 .                # python3 -m venv capel-venv
source ./capel-venv/bin/activate
pip install psycopg2-binary geoalchemy2 Flask flask_sqlalchemy flask_cors pyjwt Flask-Migrate
# IOS: Applications/Python\ 3.6/Install\ Certificates.command
```
