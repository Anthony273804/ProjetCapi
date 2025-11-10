# fichier: backend/game_setup.py



class Player:

    def __init__(self, pseudo):

        self.pseudo = pseudo

        self.vote = None  # Carte choisie plus tard (1, 2, 3, 5, etc.)



    def __repr__(self):

        return f"Player({self.pseudo})"





class Game:

    def __init__(self):

        self.players = []

        self.mode = None  # "strict", "moyenne", "mediane", etc.



    def setup_players(self):

        while True:

            try:

                nb = int(input("Nombre de joueurs : "))

                if nb < 2:

                    print("⚠️ Il faut au moins 2 joueurs !")

                    continue

                break

            except ValueError:

                print("Veuillez entrer un nombre valide.")



        for i in range(nb):

            pseudo = input(f"Pseudo du joueur {i+1} : ").strip()

            self.players.append(Player(pseudo))



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



    def summary(self):

        print("\n✅ Configuration terminée :")

        print(f"Mode choisi : {self.mode}")

        print("Joueurs :")

        for p in self.players:

            print(f" - {p.pseudo}")





if __name__ == "__main__":

    game = Game()

    game.setup_players()

    game.choose_mode()

    game.summary()