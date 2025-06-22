# MedSistēma - Skolas medicīnisko ierakstu pārvaldības sistēma

---

## Pārskats
MedSistēma ir **skolas medicīnisko ierakstu pārvaldības sistēma**, kas izstrādāta speciāli izglītības iestādēm, lai vienkāršotu studentu veselības ierakstu izsekošanu, uzturēšanu un pārvaldīšanu. Arvien pieaugošajam skolēnu skaitam skolās un sarežģījumiem, kas saistīti ar medicīniskās vēstures izsekošanu, MedSistēma nodrošina centralizētu un drošu platformu, lai medicīnas personāls, administratori un autorizēti darbinieki varētu nekavējoties piekļūt svarīgai informācijai par studentu veselību. Šī sistēma kalpo ne tikai kā efektīvs rīks veselības aprūpes pārvaldībai, bet arī palīdz nodrošināt, ka skolas ievēro noteikumus attiecībā uz studentu veselības informācijas konfidencialitāti.

Izveidota, izmantojot Python, Kivy un SQLite, MedSistēma izmanto mūsdienīgus programmatūras rīkus un ietvarus, lai izveidotu lietotājam draudzīgu interfeisu un stabilu aizmugures sistēmu. Tas nodrošina vieglu piekļuvi ierakstiem, garantē datu drošību un veicina vienmērīgu lietotāju pieredzi. MedSistēma mērķis ir samazināt administratīvo slogu, vienlaikus nodrošinot uzticamu sistēmu sensitīvu studentu veselības datu pārvaldībai. Neatkarīgi no tā, vai tiek reģistrētas parastas veselības vizītes vai tiek sekots līdzi hroniskām saslimšanām, MedSistēma palīdz medicīnas personālam vairāk koncentrēties uz studentu vajadzībām un mazāk uz sarežģītu datu bāzu pārvaldīšanu.

---

## Funkcijas

### 🏫 **Studentu pārvaldība**
- **Meklēt studentus** pēc pilna vārda vai unikāla ID, ļaujot ātri atrast nepieciešamo informāciju.
- **Skatīt detalizētus studentu profilus**, tostarp viņu klasi, kontaktinformāciju un medicīnisko vēsturi.
- **Rediģēt studentu informāciju**, piemēram, telefona numurus, medicīniskos ierakstus un hroniskas saslimšanas.
- **Arhivēt studentus**, kad tie pamet skolu, nodrošinot, ka vecie ieraksti tiek saglabāti, bet netraucē aktīvo sarakstu.

### 🏥 **Medicīnisko ierakstu uzskaite**
- **Reģistrēt studentu veselības apmeklējumus**, pierakstot viņu simptomus, ārstēšanu un jebkādas gūtās traumas.
- **Uzturēt organizētu ambulances žurnālu**, kur visi iepriekšējie apmeklējumi tiek glabāti un var tikt atgūti pēc datuma un laika.
- **Atjaunināt iepriekšējos ierakstus**, ja nepieciešams veikt labojumus vai pievienot papildu informāciju.
- **Kārtot un filtrēt medicīniskos ierakstus**, lai ātri atrastu attiecīgos ierakstus pēc studenta vārda, datuma vai veselības stāvokļa.

### 🔑 **Lietotāju autentifikācija**
- **Drošs pieteikšanās ekrāns**, lai nodrošinātu, ka tikai autorizēti darbinieki var piekļūt sistēmai.
- **Paroles aizsargāta piekļuve**, novēršot neatļautu izmaiņu veikšanu studentu ierakstos.
- **Sesijas pārvaldība**, kas saglabā lietotājus pierakstītus, kamēr viņi strādā, taču droši izslēdz tos pēc neaktivitātes.

### 📊 **Datu bāzes integrācija**
- **Izveidota uz SQLite**, vieglas, taču jaudīgas datu bāzes risinājuma.
- **Uzglabā studentu ierakstus** tabulā `skolenu_saraksts`, iekļaujot vārdus, dzimšanas datumus, medicīniskās vēstures un kontaktinformāciju.
- **Uztur medicīniskos žurnālus** tabulā `ambulatorais_zurnals`, kur tiek reģistrēti simptomi, ārstēšana un medicīniskie iejaukšanās.
- **Garantē datu konsekvenci** un uzticamību ar strukturētām vaicājumiem un efektīvu datu pārvaldību.

### 🎨 **Mūsdienīgs lietotāja interfeiss ar Kivy**
- **Pielāgoti pogas, krāsu tēmas un izkārtojuma komponenti**, kas nodrošina tīru un intuitīvu dizainu.
- **Viegla navigācija** starp dažādiem ekrāniem, izmantojot Kivy’s ScreenManager.
- **Atbalsts failu importēšanai** no CSV un Excel failiem, ļaujot masveida studentu datu augšupielādi.
- **Interaktīvas uznirstošās izvēlnes un formas**, lai efektīvi pārvaldītu studentu un medicīnisko informāciju.

---

## Instalācija (placeholder/varbūtība ap to, ka teksts būs jāmaina, pēc citām izmaiņām.)

### 📌 **Prasības**
- Python 3.8+ (savietojamībai un veiktspējai)
- Kivy 2.0+ (lietotāja interfeisa izstrādei)
- SQLite3 (datu bāzes pārvaldībai)
- Pandas (CSV un Excel datu apstrādei)

### 📥 **Iestatīšanas instrukcijas**
1. **Klonējiet repozitoriju** no GitHub:
   ```bash
   git clone https://github.com/Gr0vey/Med_projekts_Uni.git
   cd Med_projekts_Uni
   
2. Instalējiet nepieciešamās atkarības, izmantojot šādu pip komandu:
	```bash
   pip install kivy pandas
   
3. Palaidiet lietojumprogrammu, izpildot šo Python komandu:
	```bash
	python main.py
	
4. Piesakieties sistēmā, izmantojot savus autorizētos akreditācijas datus, un sāciet pārvaldīt studentu veselības ierakstus. Ja jums nav akreditācijas datu, sazinieties ar sistēmas administratoru.

---

## Lietošana (placeholder/varbūtība ap to, ka teksts būs jāmaina, pēc citām izmaiņām.)

- Pieteikšanās: Sāciet, ievadot savu lietotājvārdu un paroli, lai piekļūtu sistēmai. Tikai autorizētam personālam tiks piešķirta piekļuve.
- Meklēt studentu: Izmantojiet meklēšanas funkcionalitāti, lai atrastu studentu pēc vārda vai ID. Tas ir īpaši noderīgi, kad vairāki studenti apmeklē medicīnas kabinetu.
- Pievienot jaunus medicīniskos ierakstus: Kad students apmeklē veselības kabinetu, jūs varat viegli reģistrēt simptomus, diagnozi, ārstēšanu un jebkādas izrakstītās zāles.
- Rediģēt vai dzēst iepriekšējās ierakstus: Ja kāda informācija ir nepareiza vai jāatjaunina, jūs varat viegli mainīt medicīniskos ierakstus.
- Importēt studentu datus: Jūs varat importēt lielus studentu datu apjomus, izmantojot CSV vai Excel failus, ļaujot veikt efektīvas atjaunināšanas masveidā.
- Kārtot ierakstus: Sistēma piedāvā šķirošanas iespējas, ļaujot filtrēt medicīniskos ierakstus pēc vārda, datuma vai stāvokļa, padarot to vieglāk atrast konkrētus ierakstus.
- Arhivēt studentus: Kad students pamet skolu, viņa ieraksts var tikt arhivēts, nodrošinot, ka aktīvais studentu saraksts paliek atjaunināts un organizēts.

---

## Projekta struktūra

```bash
Med_projekts_Uni/
│── Kivy/                      # Lietotāja interfeisa komponenti un izkārtojumi
│── images/                    #  Lietojumprogrammas saistītās bildes
│── fonts/                     # Pielāgotās fonti lietotāja interfeisam
│── testa_datu_generacija/      # Skripti testu datu ģenerēšanai, lai simulētu medicīniskos ierakstus un studentu profilus
│── main.py                    # alvenais lietojumprogrammas skripts, kas atbild par sistēmas inicializēšanu
│── datubaze.db                 # SQLite datu bāze, kas uzglabā studentu un medicīniskos ierakstus
│── README.md                  # Projekta dokumentācija, kas izskaidro iestatīšanu, lietošanu un ieguldījuma norādījumus


```

---

## Ieguldījumi (Contribution)

Ieguldījumi MedSistēma projektā ir laipni gaidīti! Ja vēlaties uzlabot projektu, varat:

- Veikt forku no repozitorija
- Izveidot jaunu funkcionalitātes zaru
- Ieviešot izmaiņas
- Rūpīgi pārbaudīt izmaiņas, lai pārliecinātos, ka tās darbojas kā paredzēts
- Iesniegt pull pieprasījumu ar detalizētu paskaidrojumu par veiktajām izmaiņām

Lai piedāvātu funkcionalitātes ieteikumus vai ziņotu par kļūdām, lūdzu, izmantojiet GitHub Issues sadaļu.

---

## Licence 

---


