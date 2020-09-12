# Pacman-Two-Project
Zavrsen pakman2 projekat iz predmeta Osnovi Racunarske Inteligencije(ORI).

## Pokretanje igre
##### Igru možete sa datim baseline timom pokrenuti sa sledećom komandom:
  ```python
  python capture.py
  ```
##### Koje opcije postoje možete videti sa sledećom komandom:
  ```python
  python capture.py --help
  ```
##### Postoje četiri agenta, 0 i 2 su uvek crveni tim, dok su 1 i 3 plavi tim. Agenti se kreiraju pomoću fabrika, jedna za crveni i jedna za plavi tim. Pomoću sledeće komande možete birati koji agenti će biti crveni i plavi tim.
  ```python
  python capture.py -r baselineTeam -b baselineTeam
  ```
##### Da biste kontrolisali jednog od četiri agenta pomoću tastature, prosledite sledeći argument:
  ```python
  python capture.py --keys0
  ```
### Mape
##### Osnovna mapa koja se koristi je defaultcapture. Ukoliko želite da promenite mapu koristite -l agrument. Mape možete generisati na slučajan način tako što kao vrednost -l  argumenta prosledite RANDOM[seed] (npr. -l RANDOM2 će kreirati mapu sa seed-om 2).

### Snimanje partije
  Postoji mogućnost snimanja partije, za to koristite --record opciju. Igra će biti sačuvana u datoteku, nakon čega možete tu partiju ponovo pustiti pomoću --replay opcije.

### Ograničenja
  Zabranjeno je koristiti bilo koji vid rada sa više niti ili procesa.
