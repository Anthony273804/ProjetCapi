# fichier: backend/game_setup.py

import json

import os

from db import get_connection







class Player:

    def __init__(self, pseudo):

        self.pseudo = pseudo

        self.vote = None  # Carte choisie par le joueur



    def __repr__(self):

        return f"Player({self.pseudo})"





class Game:

    def __init__(self):
        self.id = None
        
        self.players = []

        self.mode = None

        self.backlog = []

        self.selected_story = None

    def save_game(self):
        """Enregistre la partie et les joueurs en DB"""
        conn = get_connection()
        cur = conn.cursor()
        # 1. Insérer la partie
        cur.execute(
            "INSERT INTO games (mode, selected_story_id) VALUES (%s, %s) RETURNING id",
            (self.mode, self.selected_story["id"] if self.selected_story else None)
        )
        self.id = cur.fetchone()["id"]

        # 2. Insérer les joueurs et votes
        for player in self.players:
            # Vérifier si le joueur existe déjà
            cur.execute("SELECT id FROM players WHERE pseudo = %s", (player.pseudo,))
            res = cur.fetchone()
            if res:
                player_id = res["id"]
            else:
                cur.execute("INSERT INTO players (pseudo) VALUES (%s) RETURNING id", (player.pseudo,))
                player_id = cur.fetchone()["id"]

            # Insérer le vote
            cur.execute(
                "INSERT INTO game_players (game_id, player_id, vote) VALUES (%s, %s, %s)",
                (self.id, player_id, player.vote)
            )

        conn.commit()
        cur.close()
        conn.close()

    def load_backlog_from_db(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM backlog ORDER BY id")
        self.backlog = cur.fetchall()
        cur.close()
        conn.close()

    # === Configuration joueurs ===

    def setup_players(self):

        while True:

            try:

                nb = int(input("Nombre de joueurs : "))

                if nb < 2:

                    print("Il faut au moins 2 joueurs !")

                    continue

                break

            except ValueError:

                print("Veuillez entrer un nombre valide.")



        for i in range(nb):

            pseudo = input(f"Pseudo du joueur {i+1} : ").strip()

            self.players.append(Player(pseudo))



    # === Mode de calcul ===

    def choose_mode(self):

        print("\nChoisissez un mode de jeu :")

        print("1. Mode strict (unanimité)")

        print("2. Majorité relative")



        choix = input("Votre choix : ")

        modes = {

            "1": "strict",

            "2": "majorite_relative"

        }

        self.mode = modes.get(choix, "strict")



    # === Import du backlog ===

    def import_backlog(self, filepath="backlog.json"):

        if not os.path.exists(filepath):

            print(f"Fichier '{filepath}' introuvable.")

            return



        with open(filepath, "r", encoding="utf-8") as f:

            try:

                self.backlog = json.load(f)

                print(f"\n✅ Backlog importé depuis '{filepath}'")

            except json.JSONDecodeError:

                print("Erreur : fichier JSON invalide.")



    def show_backlog(self):

        if not self.backlog:

            print("\nAucun backlog chargé.")

            return

        print("\n📋 Backlog disponible :")

        for story in self.backlog:

            print(f" - [{story['id']}] {story['titre']}")



    # === Sélection de la story à estimer ===

    def select_story(self):

        self.show_backlog()

        while True:

            try:

                choix = int(input("\nID de la story à estimer : "))

                story = next((s for s in self.backlog if s["id"] == choix), None)

                if story:

                    self.selected_story = story

                    print(f"\nStory sélectionnée : {story['titre']}")

                    break

                else:

                    print("ID invalide, essayez encore.")

            except ValueError:

                print("Veuillez entrer un nombre valide.")



    # === Phase de vote ===

    def start_voting(self):

        if not self.selected_story:

            print("Aucune story sélectionnée.")

            return



        print("\nPhase de vote !")

        print("Cartes disponibles : 1, 2, 3, 5, 8, 13, 20, 40, 100 ou (café)")

        possible_votes = ["1", "2", "3", "5", "8", "13", "20", "40", "100", "☕"]



        for player in self.players:

            while True:

                vote = input(f"{player.pseudo}, votre carte : ").strip()

                if vote in possible_votes:

                    player.vote = vote

                    break

                else:

                    print("Choix invalide, essayez encore.")



        print("\nVotes enregistrés !")

        for player in self.players:

            print(f" - {player.pseudo} → {player.vote}")



    # === Résumé global ===

    def summary(self):

        print("\nConfiguration terminée :")

        print(f"Mode choisi : {self.mode}")

        print("Joueurs :")

        for p in self.players:

            print(f" - {p.pseudo}")

        self.show_backlog()





if __name__ == "__main__":
    game = Game()
    
    # Charger le backlog depuis la DB
    game.load_backlog_from_db()

    # Configuration des joueurs et mode
    game.setup_players()
    game.choose_mode()
    # Sélection d'une story
    game.select_story()
    
    # Phase de vote
    game.start_voting()

    # Sauvegarde en base
    game.save_game()

    # Résumé
    game.summary()

