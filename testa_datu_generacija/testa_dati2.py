import random
import sqlite3 as db
import datetime
#pk nr, datums, laiks, vards uzvards, klase, simptomi, traumas ,palidziba
f_names_file = r'C:\testa_datu_generacija\dati_testam_meitenses.txt'
m_names_file = r'C:\testa_datu_generacija\dati_testam_zeni.txt'
f_lastnames_file = r'\testa_datu_generacija\dati_testam_u_meitenes.txt'
m_lastnames_file = r'\testa_datu_generacija\dati_testam_u_zeni.txt'

#datubaze = šeit bus databaze
def file_to_array(file_name):
    with open(file_name,'r',encoding='utf-8') as file:
        x = []
        word = ''
        for i in file.read():
            if i == '\n':
                x.append(word)
                word = ''
            else:
                word = word+i
    return(x)

f_names = file_to_array(f_names_file)
m_names = file_to_array(m_names_file)
f_lastnames = file_to_array(f_lastnames_file)
m_lastnames = file_to_array(m_lastnames_file)

i=1
def pk_numurs():
    i+1
    return(i)
def generate_name():
    if random.randrange(0,2) == 0:
        return(f_names[random.randrange(0,len(f_names))]+' '+f_lastnames[random.randrange(0,len(f_lastnames))])
    else:
        return(m_names[random.randrange(0,len(m_names))]+' '+m_lastnames[random.randrange(0,len(m_lastnames))])

simptomi = ('Sap Galva','Sap veders','slikta dusa','klepus','Drudzis','Nogurums','Muskuļu vai ķermeņa sāpes','Sāpošs kakls')
def generate_simptomi():
    return(random.choice(simptomi))

def generate_trauma():
    if random.randrange(0,15) == 2:
        return('+')
    else:
        return('-')

palidziba = ('Atsutu maja', 'Dod tablete','Dod atpusties')
def generate_palidziba():
    return(random.choice(palidziba))

piezimes =('Yes way','No way')
def generate_piezimes():
    if random.randrange(0,10) == 5:
        return(random.choice(piezimes))
    else:
        return('-')
    
#startDate = datetime.datetime(2022, 12, 1,8,30)
#def random_date(start,l):
#   current = start
#   while l >= 0:
#    current = current + datetime.timedelta(minutes=randrange())
#    yield current
#    l-=1

#for x in (list(random_date(startDate,100))):
#    print(x.strftime("%d/%m/%y %H:%M"))

burti = ['a','b','c','d']
with db.connect('datubaze.db') as con:
    for i in range(1,13):
        for j in range(0,random.randrange(2,5)):
            for k in range(0,27):
                cur = con.execute("""INSERT INTO ambulatorais_zurnals (klase, vards_uzvards ,pk ,dz_dati, tel_nr, med_karte, hroniskas_sl, trukst_vakc) VALUES(?,?,?,?,?,?,?,?)
                """,(str(i)+'.'+burti[j],generate_name(),))