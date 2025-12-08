import sqlite3

conn = sqlite3.connect("cap_db.sqlite3")
cur = conn.cursor()

stories = [
    ("Créer la page de login", "Ajout de l'écran de connexion utilisateur"),
    ("Mettre en place la base de données", "Créer les tables SQLite pour le projet"),
    ("Afficher le backlog", "Créer la liste des stories à l'écran"),
    ("Système de vote", "Permettre aux joueurs de voter une carte"),
]

cur.executemany(
    "INSERT INTO backlog (titre, description) VALUES (?, ?)",
    stories
)

conn.commit()
conn.close()

print("Backlog inséré ✔")
