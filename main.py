import sqlite3 as db
with db.connect('datubaze.db') as con:
    cur = con.execute("""SELECT * FROM skolenu_saraksts
    """)
    skoleni = cur.fetchall()
for i in skoleni:
    print(i[2],' ar personas kodu ',i[3])
    