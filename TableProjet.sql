-- === Table des joueurs ===
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    pseudo VARCHAR(50) NOT NULL
);

-- === Table des jeux ===
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    mode VARCHAR(50) NOT NULL, -- strict, majorite_relative
    selected_story_id INT REFERENCES backlog(id)
);

-- === Table backlog (stories) ===
CREATE TABLE backlog (
    id INT PRIMARY KEY, -- correspond à l'ID dans le JSON
    titre VARCHAR(255) NOT NULL
);

-- === Table de liaison joueurs / parties (pour stocker les votes) ===
CREATE TABLE game_players (
    game_id INT REFERENCES games(id),
    player_id INT REFERENCES players(id),
    vote VARCHAR(10), -- peut être '1', '2', ..., '100' ou '☕'
    PRIMARY KEY (game_id, player_id)
);
