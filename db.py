import sqlite3

DB_FILE = "cap_db.sqlite3"

def get_connection():
    """
    Ouvre une connexion SQLite et retourne un objet connexion.
    row_factory = sqlite3.Row permet d'accéder aux colonnes par nom (`row["id"]`)
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
