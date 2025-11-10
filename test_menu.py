import pytest

import json

from backend import Game, Player



# --- Fixtures utiles pour préparer les tests ---



@pytest.fixture

def sample_backlog(tmp_path):

    """Crée un fichier backlog JSON temporaire pour les tests."""

    backlog_data = [

        {"id": 1, "titre": "Réinitialisation du mot de passe"},

        {"id": 2, "titre": "Connexion via Google"}

    ]

    file_path = tmp_path / "backlog.json"

    with open(file_path, "w", encoding="utf-8") as f:

        json.dump(backlog_data, f)

    return str(file_path)





@pytest.fixture

def sample_game():

    """Crée une instance de jeu vide."""

    game = Game()

    game.players = [Player("Alice"), Player("Bob"), Player("Charlie")]

    return game





# --- Tests unitaires ---



def test_player_initialization():

    """Vérifie la création d’un joueur."""

    p = Player("Alan")

    assert p.pseudo == "Alan"

    assert p.vote is None

    assert repr(p) == "Player(Alan)"





def test_import_backlog(sample_backlog):

    """Vérifie l'import d'un backlog JSON valide."""

    game = Game()

    game.import_backlog(sample_backlog)

    assert len(game.backlog) == 2

    assert game.backlog[0]["titre"] == "Réinitialisation du mot de passe"





def test_select_story(monkeypatch, sample_backlog):

    """Vérifie la sélection d'une story à partir du backlog."""

    game = Game()

    game.import_backlog(sample_backlog)



    # Simule la saisie utilisateur "2" (pour story id=2)

    monkeypatch.setattr("builtins.input", lambda _: "2")

    game.select_story()



    assert game.selected_story["id"] == 2

    assert game.selected_story["titre"] == "Connexion via Google"





def test_voting_phase(monkeypatch, sample_game):

    """Vérifie que les votes des joueurs sont enregistrés correctement."""

    inputs = iter(["3", "5", "8"])  # Simule les votes de Alice, Bob, Charlie

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))



    sample_game.selected_story = {"id": 1, "titre": "Réinitialisation du mot de passe"}

    sample_game.start_voting()



    votes = [p.vote for p in sample_game.players]

    assert votes == ["3", "5", "8"]





def test_invalid_vote(monkeypatch, sample_game, capsys):

    """Vérifie que le programme gère un vote invalide."""

    # Simule une première entrée invalide, puis une entrée valide

    inputs = iter(["99", "☕", "☕", "☕"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))



    sample_game.selected_story = {"id": 1, "titre": "Story test"}

    sample_game.start_voting()



    captured = capsys.readouterr()

    assert "⚠️ Choix invalide" in captured.out

    assert all(p.vote == "☕" for p in sample_game.players)

