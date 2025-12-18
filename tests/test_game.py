import unittest
import sqlite3
import datetime

from Backend import Game, Player
from db import get_connection


class TestGameLogic(unittest.TestCase):

    def setUp(self):
        """Préparation avant chaque test"""
        self.game = Game()
        self.game.players = [
            Player("Alice"),
            Player("Bob"),
            Player("Charlie")
        ]

    # -------------------------
    # Test unanimité
    # -------------------------
    def test_check_unanimity_true(self):
        for p in self.game.players:
            p.vote = "5"
        self.assertTrue(self.game.check_unanimity())

    def test_check_unanimity_false(self):
        self.game.players[0].vote = "5"
        self.game.players[1].vote = "8"
        self.game.players[2].vote = "5"
        self.assertFalse(self.game.check_unanimity())

    # -------------------------
    # Test joueurs
    # -------------------------
    def test_players_added(self):
        self.assertEqual(len(self.game.players), 3)
        pseudos = [p.pseudo for p in self.game.players]
        self.assertIn("Alice", pseudos)

    # -------------------------
    # Test backlog
    # -------------------------
    def test_load_backlog(self):
        self.game.load_backlog()
        self.assertIsInstance(self.game.backlog, list)

    def test_remove_story(self):
        self.game.load_backlog()
        if not self.game.backlog:
            self.skipTest("Backlog vide, test ignoré")

        initial_len = len(self.game.backlog)
        story_id = self.game.backlog[0]["id"]

        self.game.remove_story(story_id)
        self.assertEqual(len(self.game.backlog), initial_len - 1)

    # -------------------------
    # Test sauvegarde game
    # -------------------------
    def test_save_game(self):
        self.game.mode = "strict"
        self.game.selected_story = {"id": 1, "titre": "Test"}

        for p in self.game.players:
            p.vote = "3"

        self.game.save_game()

        self.assertIsNotNone(self.game.id)

        # Vérifier en base
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM games WHERE id = ?", (self.game.id,))
        game_row = cur.fetchone()
        conn.close()

        self.assertIsNotNone(game_row)


if __name__ == "__main__":
    unittest.main()
