import sqlite3

conn = sqlite3.connect("cap_db.sqlite3")
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode TEXT NOT NULL,
    selected_story_id INTEGER
);

CREATE TABLE IF NOT EXISTS game_players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    vote TEXT,
    FOREIGN KEY(game_id) REFERENCES games(id),
    FOREIGN KEY(player_id) REFERENCES players(id)
);

CREATE TABLE IF NOT EXISTS backlog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT
);
""")

try:
    cur.execute("ALTER TABLE games ADD COLUMN created_at DATETIME")
    print("✅ Colonne created_at ajoutée")
except sqlite3.OperationalError:
    print("ℹ️ Colonne created_at existe déjà")

conn.commit()
conn.close()

print("✅ Base SQLite initialisée avec succès")
