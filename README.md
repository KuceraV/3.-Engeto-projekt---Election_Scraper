# 3.-Engeto-projekt-Election_Scraper
Třetí projekt Engeto Python akademie

# Popis projektu
Skript vybere jakýkoliv územní celek z daného odkazu (https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). Z tohoto odkazu "vyscrapuje" výsledky hlasování pro všechny obce.

# Popis projektu
Knihovny potřebné ke spuštění tohoto projektu je možné nainstalovat do virtuálního prostředí ze souboru requirements.txt.
K instalaci zadejte příkaz:
> pip --version # ověří verzi pip manažeru

> pip install -r requirements.txt # nainstaluje knihovny z listu requirements.txt

# Spuštění skriptu
Soubor Election_scraper je třeba spustit pomocí příkazové řádky a zadat dva povinné argumenty
např.: 
> python Election_scraper.py "url_adresa_uzemniho_celku" "jmeno_souboru.csv"

volební výsledky z vybraného odkazu se poté uloží do csv souboru
