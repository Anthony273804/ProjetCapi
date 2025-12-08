import sqlite3
conn = sqlite3.connect("cap_db.sqlite")
cur = conn.cursor()
cur.executescript(open("init_db.sql").read())
conn.commit()
conn.close()
