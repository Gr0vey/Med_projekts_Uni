import sqlite3 as db
with db.connect('datubaze.db') as con:
    cur = con.execute("""SELECT klase, vards_uzvards FROM skolenu_saraksts
    """)
    skoleni = cur.fetchall()
    for i in skoleni:print(' '.join(i))
    