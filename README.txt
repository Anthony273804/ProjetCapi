Planning Poker - Application de Gestion de Backlog

Description
-----------
Projet Python permettant d'estimer des stories via le jeu Planning Poker. 
Interface graphique avec Tkinter et base de données SQLite intégrée.

Prérequis
---------
- Python 3.8 ou supérieur
- Tkinter (intégré à Python)
- sqlite3 (intégré à Python)

Installation et Initialisation
------------------------------
1. Cloner le dépôt :
   git clone <URL_DU_DEPOT>
   cd ProjetCapi
2. Initialiser la base de données SQLite :
   python init_db.py
3. Remplir le backlog initial avec des stories :
   python fill_backlog.py

Important : Les scripts init_db.py et fill_backlog.py doivent être exécutés avant le premier lancement.

Lancement du projet
------------------
python backend.py

Workflow et Utilisation
----------------------
1. Menu principal
2. Charger ou actualiser le backlog
3. Ajouter ou supprimer des stories
4. Ajouter des joueurs
5. Choisir un mode de jeu :
   - Strict : Unanimité obligatoire pour valider le vote. Si les votes ne sont pas identiques, un revote est demandé.
   - Majorité relative : Le vote se termine après que tous les joueurs ont choisi. Le résultat affiché est celui de la majorité.
6. Sélectionner une story à estimer
7. Phase de vote via la fenêtre graphique
8. Afficher résumé et sauvegarder la partie en base

Structure du projet
------------------
- backend.py : Script principal avec l'interface Tkinter et la logique de jeu
- db.py : Gestion de la connexion à la base SQLite
- init_db.py : Création de la base et des tables
- fill_backlog.py : Insertion de stories initiales dans la base
- backlog.json : Fichier optionnel pour importer des stories au format JSON

Fonctionnalités
---------------
- Ajout et suppression de stories
- Ajout de joueurs
- Choix de mode de jeu
- Sélection de story à estimer
- Phase de vote graphique
- Validation de votes (unanimité ou majorité relative)
- Résumé et sauvegarde automatique des parties

Tests
-----
- Utilisez pytest ou unittest pour exécuter les tests unitaires
- Exemple de commande : pytest test_menu.py

Auteur
------
Anthony Bourgeois Alan Delevaux

