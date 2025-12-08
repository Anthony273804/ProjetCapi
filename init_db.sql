CREATE TABLE IF NOT EXISTS backlog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode TEXT,
    selected_story_id INTEGER,
    FOREIGN KEY(selected_story_id) REFERENCES backlog(id)
);

CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS game_players (
    game_id INTEGER,
    player_id INTEGER,
    vote TEXT,
    FOREIGN KEY(game_id) REFERENCES games(id),
    FOREIGN KEY(player_id) REFERENCES players(id)
);
