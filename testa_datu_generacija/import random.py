import random
import os
import sqlite3 as db

datu_baze = r'datubaze.db'

x = random.randrange(789,2840) 
print(x)
# WHERE skolena_id={x}
with db.connect(datu_baze) as con:
    cur = con.execute(f'''SELECT skolena_id FROM skolenu_saraksts''')
    mem = cur.fetchall()
    y = random.choice(mem)
    cur2 = con.execute(f'''SELECT skolena_id,vards_uzvards,klase FROM skolenu_saraksts WHERE skolena_id={y[0]}''')
    mem2 = cur2.fetchone()
    print(mem2)

