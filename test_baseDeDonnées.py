from db import get_connection

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")  # Vérifie la version de PostgreSQL
    print(cur.fetchone())
    cur.close()
    conn.close()
    print("Connexion réussie !")
except Exception as e:
    print("Erreur de connexion :", e)
