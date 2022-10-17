import sqlite3 as db
with db.connect('datubaze.db') as con:
    cur = con.execute("""SELECT klase FROM skolenu_saraksts WHERE id = 1
    """)
    skoleni = cur.fetchall()
for i in skoleni:
    print(i[2],' ar personas kodu ',i[3])
    