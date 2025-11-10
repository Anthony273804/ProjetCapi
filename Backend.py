# fichier: backend/game_setup.py

import json

import os



class Player:

    def __init__(self, pseudo):

        self.pseudo = pseudo

        self.vote = None  # Carte choisie par le joueur



    def __repr__(self):

        return f"Player({self.pseudo})"





class Game:

    def __init__(self):

        self.players = []

        self.mode = None

        self.backlog = []

        self.selected_story = None



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

        print("2. Moyenne")

        print("3. Médiane")

        print("4. Majorité absolue")

        print("5. Majorité relative")



        choix = input("Votre choix : ")

        modes = {

            "1": "strict",

            "2": "moyenne",

            "3": "mediane",

            "4": "majorite_absolue",

            "5": "majorite_relative"

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

    game.import_backlog()

    game.setup_players()

    game.choose_mode()

    game.select_story()

    game.start_voting()
