import requests
from bs4 import BeautifulSoup as bs
import csv
import sys
from pprint import pprint
import traceback


def main():
    url, jmeno_souboru = kontrola_vstupnich_argumentu()
    tables = scrapovani_stranky(url)
    vysledky = vysledky_do_radku(tables)
    import_do_csv(tables, vysledky, jmeno_souboru)


def scrapovani_stranky(url: str) -> list:
    """
    funkce bere jako vstupni parametr systemovy argument s url adresou daneho uzemniho celku
    a vraci list table tag s tabulkami obahujici jednotlive obce. 
    """
    odpoved = requests.get(url)
    soup = bs(odpoved.text, features="html.parser")
    tables = soup.find_all("table", {"class": "table"})
    return tables

def kontrola_vstupnich_argumentu():
    """
    Funkce kontrolující správnost vstupních systémových argumentů při spouštění skriptu Election_Scraper.py
    Ke spuštění tohoto skriptu (Election_scraper.py) je třeba zadat dva systémové argumenty ve správném pořadí.
    První argument odkazuje na scrapovanou url adresu, durhý argument na jméno soubor, do kterého se uloží vyscrapovaná data

    > python Election_scraper.py "url_adresa" "vystupní_soubor.csv"

    """

    vzor_url = "https://volby.cz/pls/ps2017nss"

    if len(sys.argv) != 3:
        print(
            "Pro spuštění programu chybí potřebný počet argumentů",
            "Zapiš příkaz ve formátu: python Election_scraper.py, 'url',  'jmeno_souboru.csv'",
            sep="\n"
        )
        quit()

    elif sys.argv[1][:len(vzor_url)] != vzor_url:
        print(
            "Zadej správnou url adresu!",
            "Zapiš příkaz ve formátu: python Election_scraper.py, 'url',  'jmeno_souboru.csv'",
            sep="\n"
        )
        quit()

    elif sys.argv[2][-3:] != "csv":
        print("Zadej správný formát výstupu: 'jmeno_souboru.csv'")
        quit()

    else:
        print(
            "Vstupy úspešně zadány",
            "Spouštím program...",
            sep="\n"
        )
    return sys.argv[1], sys.argv[2]


def code_locatation(all_tables: list) -> list:
    """
    Funkce bere jako vstupni parametr list z funkce scrapovani_stranky(url) a
    vraci list paru hodnot code a location z vybraneho okresu

    priklad:
    [['506761', 'Alojzov'],
    ['589268', 'Bedihošť'],
    ['589276', 'Bílovice-Lutotín'],
    ['589284', 'Biskupice']
    ...]
    """

    vsechny_obce = []
    for table in all_tables:
        all_tr = table.find_all("tr")
        for tr in all_tr[2:]:
            td_radek = tr.find_all("td")
            data = [
                td_radek[0].getText(),
                td_radek[1].getText()
            ]
            vsechny_obce.append(data)
    return vsechny_obce


def seznam_odkazu(tables: list) -> list:
    """
    Funkce vraci list stringů url odkazů v a_href tagu z ciselneho kodu 
    u jednolitvých obcí. Jako vstupni parametr bere list z funkce 
    scrapovani_stranky(url).
        
    přiklad"
    ['ps311?xjazyk=CZ&xkraj=12&xobec=506761&xvyber=7103',
    'ps311?xjazyk=CZ&xkraj=12&xobec=589268&xvyber=7103',
    'ps311?xjazyk=CZ&xkraj=12&xobec=589276&xvyber=7103',
    ...]
    """
    seznam_href_tagu = [
        href.find("a").get("href")
        for tabulka in tables
        for href in tabulka.find_all("td", {"class": "cislo"})
    ]
    return seznam_href_tagu


def html_vysledky_voleb(odkazy: list) -> list:
    """
    Funkce bere jako vstup list stringů url odkazů v a_href tagu 
    z ciselneho kodu u jednolitvých obcí z funkce seznam_odkazu().
    Funkce vraci jako vystup list vyparserovanych html kodu pro
    jednotlive stranky obcí s vysledky voleb.
    """
    root = "https://volby.cz/pls/ps2017nss"
    list_html_vv = []
    for new_link in odkazy:
        odpoved_link = requests.get(f"{root}/{new_link}")
        soup_link = bs(odpoved_link.text, features="html.parser")
        list_html_vv.append(soup_link)
    return list_html_vv


def volebni_data(html_stranka_1_obec) -> list: 
    """
    Funkce vraci z html stranky pro kazdou obec list tabulek 
    s volebnimi informacemi a hlasy pro jednotlive politicke strany.
    """
    tables = html_stranka_1_obec.find_all("table", {"class": "table"})
    return tables


def volebni_info_header(tables: list) -> list:
    """
    Funkce projde list vyparserovanych html kodu pro jednotlive stranky obcí 
    s vysledky voleb pomoci for smycky. Dále vyhledá na těchto stránkách
    tagy s tabulkami (tables) pomoci funkce volebni_data(). Z prvni tabulky ziska
    udaje a poctu volicu, vydanych obalek a platnych hlasu. Ty vrati v listu 
    listů s danými udaji.

    vystup:
    [['205', '145', '144'],
    ['834', '527', '524'],
    ['431', '279', '275']
    ...]

    """
    html_stranky = html_vysledky_voleb(seznam_odkazu(tables))
    list_header = []
    for stranka in html_stranky:
        all_tables = volebni_data(stranka)
        table_header = all_tables[0]
        all_td = table_header.find_all("td")
        hodnoty = [
            all_td[3].getText(),
            all_td[4].getText(),
            all_td[-2].getText()]
        list_header.append(hodnoty)
    return list_header


def nazvy_sloupcu_table(tables: list) -> list:
    """
    Funkce ziska nazvy jednotlivych politickych stran pro nazvy sloupcu
    z prvni html stranky obce s volebnimi vysledky ve vybranem okrese.
    Funkce vraci list nazvu jednotlivych sloupcu.
    """
    nazvy_ostatnich_sloupcu = ["Code", "Location", "Registered", "Envelopes", "Valid"]

    html_stranky = html_vysledky_voleb(seznam_odkazu(tables))
    all_tables = volebni_data(html_stranky[0])

    nazvy_stran = [
        tr.find_all("td")[1].getText()
        for table in all_tables[1:]
        for tr in table.find_all("tr")[2:]
    ]

    return nazvy_ostatnich_sloupcu + nazvy_stran


def pocty_hlasu(tables: list) -> list:
    """
    Funkce projde list vyparserovanych html kodu pro jednotlive stranky obcí 
    s vysledky voleb pomoci for smycky. Dále vyhledá na těchto stránkách
    tagy s tabulkami (tables) pomoci funkce volebni_data(). Z druhych dvou
    tabulek ziska pocty hlasu pro jednotlive strany, ktere vraci jako list.
    
    """
    html_stranky = html_vysledky_voleb(seznam_odkazu(tables))
    list_vysledky_voleb = []

    for stranka in html_stranky:
        all_tables = volebni_data(stranka)
        vysledky_1_obec = []
        for table in all_tables[1:]:
            all_tr = table.find_all("tr")
            for tr in all_tr[2:]:
                td_radek = tr.find_all("td")
                vysledky_1_obec.append(td_radek[2].getText())
        list_vysledky_voleb.append(vysledky_1_obec)
    return list_vysledky_voleb


def vysledky_do_radku(tables: list) ->list:
    """
    Funkce zapiše volebni vysledky pro jednotlive obce s jejich číselným
    kódem a názvem do jednoho listu, který tvořá jeden řádek v tabulce.  
    """
    kod_obec = code_locatation(tables)
    voleb_info_hlavicka = volebni_info_header(tables)
    pocty_hlasy = pocty_hlasu(tables)
    vysledky = [
        obec + hlavicka + hlasy
        for obec, hlavicka, hlasy in zip(kod_obec, voleb_info_hlavicka, pocty_hlasy)
    ]
    return vysledky


def import_do_csv(tables, vysledky, jmeno_souboru):
    """
    funkce uloží stažená data do csv souboru.
    """
    nazvy_sloupcu = nazvy_sloupcu_table(tables)

    try:
        csv_soubor = open(jmeno_souboru, mode="w", newline="", encoding="UTF-8")

    except FileExistsError:
        return traceback.format_exc()
    
    else:
        zapisovac = csv.writer(csv_soubor)
        zapisovac.writerow(nazvy_sloupcu)
        for radek in vysledky:
            zapisovac.writerow(radek)
        return print("Uloženo, ukončuji program.")
    
    finally:
        csv_soubor.close()

if __name__ == "__main__":
    main()

