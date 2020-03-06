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

### Install 

- Documentation d'installation : https://github.com/PnEcrins/FollowDem-admin/tree/master/docs/installation.rst