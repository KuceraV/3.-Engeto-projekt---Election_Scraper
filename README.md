# 3.-Engeto-projekt-Election_Scraper
Třetí projekt Engeto Python akademie

## Popis projektu
Skript vybere jakýkoliv územní celek z daného odkazu (https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). Z tohoto odkazu "vyscrapuje" výsledky hlasování pro všechny obce.

## Instalace knihoven
Knihovny potřebné ke spuštění tohoto projektu je možné nainstalovat do virtuálního prostředí ze souboru requirements.txt.
K instalaci zadejte příkaz:
> pip --version # ověří verzi pip manažeru

> pip install -r requirements.txt # nainstaluje knihovny z listu requirements.txt

## Spuštění skriptu
Soubor Election_Scraper je třeba spustit pomocí příkazové řádky a zadat dva povinné argumenty
např.: 
> python Election_Scraper.py "url_adresa_uzemniho_celku" "jmeno_souboru.csv"

volební výsledky z vybraného odkazu se poté uloží do csv souboru

## Ukázka projektu
Výsledky hlasování pro okres Benešov:
1. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
2. argument: vysledky_Benesov.csv

Spuštění programu:
> python Election_Scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_Benesov.csv"

Průběh stahování:
> Vstupy úspešně zadány

> Spouštím program...

> Uloženo, ukončuji program.

Částečný výstup:
> Code,Location,Registered,Envelopes,Valid,...

> 529303,Benešov,13 104,8 485,8 437,1 052,10,2,624,3,802,597,109,35,112,6,11,948,3,6,414,2 577,3,21,314,5,58,17,16,682,10

> 532568,Bernartice,191,148,148,4,0,0,17,0,6,7,1,4,0,0,0,7,0,0,3,39,0,0,37,0,3,0,0,20,0

> 530743,Bílkovice,170,121,118,7,0,0,15,0,8,18,0,2,0,0,0,3,0,0,2,47,1,0,6,0,0,0,0,9,0

> ...