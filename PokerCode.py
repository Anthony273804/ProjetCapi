import tkinter as tk
from tkinter import simpledialog, messagebox
from db import get_connection
import datetime

# -----------------------------
# Classes de base
# -----------------------------
class Player:
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.vote = None

class Game:
    def __init__(self):
        self.id = None
        self.players = []
        self.mode = None
        self.backlog = []
        self.selected_story = None
        self.created_at = datetime.datetime.now()

    def check_unanimity(self):
        """Retourne True si tous les votes sont identiques (strict)"""
        votes = [p.vote for p in self.players]
        return all(v == votes[0] for v in votes)

    # ---------------------------------------------------------
    # DB: sauvegarder la partie
    # ---------------------------------------------------------
    def save_game(self):
        conn = get_connection()
        cur = conn.cursor()

        # Partie
        cur.execute(
            "INSERT INTO games (mode, selected_story_id, created_at) VALUES (?, ?, ?)",
            (self.mode, self.selected_story["id"] if self.selected_story else None, self.created_at)
        )
        self.id = cur.lastrowid

        # Joueurs et votes
        for player in self.players:
            cur.execute("SELECT id FROM players WHERE pseudo = ?", (player.pseudo,))
            res = cur.fetchone()
            if res:
                player_id = res[0]
            else:
                cur.execute("INSERT INTO players (pseudo) VALUES (?)", (player.pseudo,))
                player_id = cur.lastrowid
            cur.execute(
                "INSERT INTO game_players (game_id, player_id, vote) VALUES (?, ?, ?)",
                (self.id, player_id, player.vote)
            )

        conn.commit()
        conn.close()

    # ---------------------------------------------------------
    # Charger backlog
    # ---------------------------------------------------------
    def load_backlog(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM backlog ORDER BY id")
        rows = cur.fetchall()
        conn.close()
        self.backlog = [{"id": row[0], "titre": row[1], "description": row[2]} for row in rows]

    # ---------------------------------------------------------
    # Supprimer story
    # ---------------------------------------------------------
    def remove_story(self, story_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM backlog WHERE id = ?", (story_id,))
        conn.commit()
        conn.close()
        self.load_backlog()

# -----------------------------
# Interface Tkinter
# -----------------------------
class GameUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Planning Poker")
        self.game = Game()
        self.game.load_backlog()

        # Listbox pour backlog
        self.listbox = tk.Listbox(master, width=50)
        self.listbox.pack(pady=10)
        self.update_listbox()


        # Boutons backlog
        tk.Button(master, text="Ajouter story", command=self.add_story).pack(pady=5)
        tk.Button(master, text="Supprimer story sélectionnée", command=self.remove_story).pack(pady=5)
        tk.Button(master, text="Actualiser backlog", command=self.refresh_backlog).pack(pady=5)
       
        # Boutons joueurs
        tk.Button(master, text="Ajouter joueur", command=self.add_player).pack(pady=5)
        tk.Button(master, text="Choisir mode", command=self.choose_mode).pack(pady=5)
        tk.Button(master, text="Sélection story", command=self.select_story).pack(pady=5)
        tk.Button(master, text="Phase de vote", command=self.start_voting).pack(pady=5)
        tk.Button(master, text="Résumé & Sauvegarde", command=self.summary_and_save).pack(pady=10)

        # Affichage des joueurs
        self.players_label = tk.Label(master, text="Joueurs : Aucun")
        self.players_label.pack()

        # Affichage du mode
        self.mode_label = tk.Label(master, text="Mode : Aucun")
        self.mode_label.pack()

        # Affichage story sélectionnée
        self.story_label = tk.Label(master, text="Story sélectionnée : Aucune")
        self.story_label.pack()

    # -------------------------
    # Backlog
    # -------------------------
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, story in enumerate(self.game.backlog, start=1):
            self.listbox.insert(tk.END, f"{idx}. {story['titre']}")

    def refresh_backlog(self):
        self.game.load_backlog()
        self.update_listbox()

    def remove_story(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Alerte", "Sélectionnez une story à supprimer")
            return
        index = selection[0]
        story = self.game.backlog[index]
        if messagebox.askyesno("Confirmer", f"Supprimer '{story['titre']}' ?"):
            self.game.remove_story(story["id"])
            self.update_listbox()
    
    # Méthode pour ajouter une story :
    def add_story(self):
        titre = simpledialog.askstring("Ajouter story", "Titre de la story :")
        if not titre:
            return
        description = simpledialog.askstring("Ajouter story", "Description (optionnelle) :") or ""
        
        # Insérer en DB
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO backlog (titre, description) VALUES (?, ?)", (titre, description))
        conn.commit()
        conn.close()
        
        # Actualiser la liste
        self.game.load_backlog()
        self.update_listbox()

    # -------------------------
    # Joueurs
    # -------------------------
    def add_player(self):
        pseudo = simpledialog.askstring("Ajouter joueur", "Pseudo du joueur :")
        if pseudo:
            self.game.players.append(Player(pseudo))
            self.update_players_label()

    def update_players_label(self):
        if self.game.players:
            text = "Joueurs : " + ", ".join(p.pseudo for p in self.game.players)
        else:
            text = "Joueurs : Aucun"
        self.players_label.config(text=text)

    # -------------------------
    # Mode
    # -------------------------
    def choose_mode(self):
        choix = simpledialog.askstring("Mode", "Choisissez un mode :\n1. strict\n2. majorite_relative")
        if choix == "1":
            self.game.mode = "strict"
        elif choix == "2":
            self.game.mode = "majorite_relative"
        else:
            self.game.mode = "strict"
        self.mode_label.config(text=f"Mode : {self.game.mode}")

    # -------------------------
    # Sélection story
    # -------------------------
    def select_story(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Alerte", "Sélectionnez une story")
            return
        index = selection[0]
        self.game.selected_story = self.game.backlog[index]
        self.story_label.config(text=f"Story sélectionnée : {self.game.selected_story['titre']}")

    # -------------------------
    # Phase de vote
    # -------------------------
    def start_voting(self):
        if not self.game.selected_story:
            messagebox.showwarning("Erreur", "Aucune story sélectionnée")
            return

        if not self.game.players:
            messagebox.showwarning("Erreur", "Aucun joueur")
            return

        self.vote_window = tk.Toplevel(self.master)
        self.vote_window.title("Phase de vote")

        self.vote_vars = []
        possible_votes = ["1", "2", "3", "5", "8", "13", "20", "40", "100", "café"]

        for player in self.game.players:
            frame = tk.Frame(self.vote_window)
            frame.pack(padx=10, pady=5, anchor="w")

            tk.Label(frame, text=player.pseudo, width=15, anchor="w").pack(side="left")

            var = tk.StringVar()
            tk.OptionMenu(frame, var, *possible_votes).pack(side="left")

            self.vote_vars.append((player, var))

        tk.Button(
            self.vote_window,
            text="Valider les votes",
            command=self.validate_votes
        ).pack(pady=10)

    def validate_votes(self):
        # Récupérer les votes
        for player, var in self.vote_vars:
            vote = var.get()
            if not vote:
                messagebox.showerror("Erreur", f"{player.pseudo} n'a pas voté")
                return
            player.vote = vote

        # MODE STRICT → vérifier unanimité
        if self.game.mode == "strict":
            votes = [p.vote for p in self.game.players]
            if len(set(votes)) != 1:
                messagebox.showwarning(
                    "Pas unanime",
                    "Les votes ne sont pas unanimes.\nRevotez."
                )
                return  # ⚠️ on reste dans la fenêtre

        # MODE MAJORITÉ RELATIVE (ou strict validé)
        messagebox.showinfo("Votes validés", "Votes enregistrés avec succès")
        self.vote_window.destroy()

    # -------------------------
    # Résumé & sauvegarde
    # -------------------------
    def summary_and_save(self):
        self.game.save_game()
        summary = f"Mode : {self.game.mode}\nJoueurs : {', '.join(p.pseudo for p in self.game.players)}"
        if self.game.selected_story:
            summary += f"\nStory sélectionnée : {self.game.selected_story['titre']}"
        votes = "\n".join([f"{p.pseudo} : {p.vote}" for p in self.game.players])
        summary += f"\nVotes :\n{votes}"
        messagebox.showinfo("Résumé", summary)

# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = GameUI(root)
    root.mainloop()
