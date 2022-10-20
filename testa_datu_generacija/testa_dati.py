import random
import os
f_names_file = r'C:\Users\aleks\Documents\GitHub\Med_projekts\testa_datu_generacija\dati_testam_meitenses.txt'
m_names_file = r'C:\Users\aleks\Documents\GitHub\Med_projekts\testa_datu_generacija\dati_testam_zeni.txt'
f_lastnames_file = r'C:\Users\aleks\Documents\GitHub\Med_projekts\testa_datu_generacija\dati_testam_u_meitenes.txt'
m_lastnames_file = r'C:\Users\aleks\Documents\GitHub\Med_projekts\testa_datu_generacija\dati_testam_u_zeni.txt'
slimibas_file = r'C:\Users\aleks\Documents\GitHub\Med_projekts\testa_datu_generacija\dati_hroni_slim.txt'

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
slimibas = file_to_array(slimibas_file)

def generate_name():
    if random.randrange(0,2) == 0:
        return(f_names[random.randrange(0,len(f_names))]+' '+f_lastnames[random.randrange(0,len(f_lastnames))])
    else:
        return(m_names[random.randrange(0,len(m_names))]+' '+m_lastnames[random.randrange(0,len(m_lastnames))])
            
def generate_datums_un_pk(klase):#Gads 2003-2015 #Mēnesis 01-12 #Diena 01-31
    gads = str(random.randrange(2003+12-klase,2004+13-klase))
    menesis = str(random.randrange(1,12))
    diena = str(random.randrange(1,31))
    if len(menesis) == 1:
        menesis = '0'+menesis
    if len(diena) == 1:
        diena = '0'+diena
    return('{}.{}.{}'.format(diena,menesis,gads),'{}{}{}-{}'.format(diena,menesis,gads[2:],str(random.randrange(10000,99999))))

def generate_tel():
    return('+3712'+str(random.randrange(1000000,9999999)))

def generate_medkarte():
    if random.randrange(0,2) == 0:
        return('ir')
    else:
        return('nav')

def generate_slimibas():
    if random.randrange(0,20) == 1:
        return(str(slimibas[random.randrange(0,len(slimibas)+1)]))
    else: 
        return('-')

 
datums, pk = generate_datums_un_pk(12)
name = generate_name()
print(name)
print(datums)
print(pk)
print(generate_tel())
print(generate_medkarte())
print(generate_slimibas())