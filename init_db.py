import sqlite3

conn = sqlite3.connect("cap_db.sqlite3")
cur = conn.cursor()

# 1. Ajouter created_at à la table games (si pas déjà fait)
try:
    cur.execute("ALTER TABLE games ADD COLUMN created_at TEXT")
    print("Colonne 'created_at' ajoutée à 'games'.")
except sqlite3.OperationalError:
    print("Colonne 'created_at' existe déjà.")

# 2. Ajouter une table pour gérer les storys si nécessaire (optionnel)
# Ici on suppose que backlog existe déjà

conn.commit()
conn.close()
