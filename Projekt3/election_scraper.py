"""
election_scraper.py: třetí projekt do Engeto Online Python Akademie
author: Jaroslav Šafránek
email: jaroslav.safranek@rako.cz
discord: Joker055#6334
"""

import csv
import sys

from requests import get
from bs4 import BeautifulSoup as bs


def ziskani_parsovane_odpovedi(url: str) -> bs:
    odpoved_serveru = get(url)
    if not odpoved_serveru.ok:
        print("Server je aktuálně nedostupný. Zkuste to prosím později.")
        sys.exit()
    return bs(get(url).text, features="html.parser")


def ziskani_td_tagu(odpoved: bs, atribut: str, hodnota_atributu: str) -> list:
    return odpoved.find_all("td", {atribut: hodnota_atributu})


def ziskani_hodnoty_td_tagu(odpoved: bs, hodnota_atributu: str) -> int:
    return int(
        odpoved.find("td", {"headers": hodnota_atributu}).text.replace(
            "\xa0", ""
        )
    )


def vytvor_seznam_obci(list_tagu: list) -> list[dict]:
    """
    Vytvoří list dictionary pro všechny obce ze zadané url

    | Argument:
    | list_tagu: list td tagu, obsahujici cislo kazde obce

    | Vrací:
    | dict s kombinaci kódu a názvu obce: {'code': '598925', 'location': 'Albrechtice'}
    """
    seznam_obci = list()
    for td_tag_obce in list_tagu:
        obec_dict = dict()
        obec_dict["code"] = td_tag_obce.text
        obec_dict["location"] = td_tag_obce.find_next_sibling("td").text
        seznam_obci.append(obec_dict)
    return seznam_obci


def ziskani_obci(url: str) -> list[dict]:
    """
    | Ze zadaného url získá naparsovanou odpověd serveru.
    | Z odpovědi vytvoří list td tagů se zvoleným atributem a jeho hodnotou.
    | Z listu td tagů vytvoří list dictionary s nazvem a cislem obce

    | Argument:
    | url: vybrana url adresa pro ziskani vysledku voleb zadana jako argument

    | Vrací:
    | dict s kombinaci kódu a názvu obce: {'code': '598925', 'location': 'Albrechtice'}
    """
    parsovana_odpoved = ziskani_parsovane_odpovedi(url)
    list_tagu = ziskani_td_tagu(parsovana_odpoved, "class", "cislo")
    return vytvor_seznam_obci(list_tagu)


def ziskani_vysledku_obce(dict_obec: dict, kraj: str, vyber: str) -> None:
    """
    | Získá výsledky voleb v jednotlivé obci a rozšíří o ně dict s údaji o obci

    | Argument:
    | obec: dictionary, obsahující údaje o obci
    | kraj: číslo kraje vyexportované ze zadaná url adresy
    | vyber: číslo výběru vyexportované ze zadané url adresy
    """

    url_obec = f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&{kraj}&xobec={dict_obec['code']}&xvyber={vyber}"
    parsovana_odpoved = ziskani_parsovane_odpovedi(url_obec)
    dict_obec["registered"] = ziskani_hodnoty_td_tagu(parsovana_odpoved, "sa2")
    dict_obec["envelopes"] = ziskani_hodnoty_td_tagu(parsovana_odpoved, "sa3")
    dict_obec["valid"] = ziskani_hodnoty_td_tagu(parsovana_odpoved, "sa6")
    vysledky_stran_v_obci = ziskani_td_tagu(
        parsovana_odpoved, "headers", "t1sb2"
    )
    vysledky_stran_v_obci = vysledky_stran_v_obci + ziskani_td_tagu(
        parsovana_odpoved, "headers", "t2sb2"
    )
    for vysledek_strany_v_obci in vysledky_stran_v_obci:
        if vysledek_strany_v_obci.text == "-":
            continue
        dict_obec[vysledek_strany_v_obci.text] = int(
            vysledek_strany_v_obci.find_next_sibling("td").text.replace(
                "\xa0", ""
            )
        )


def ulozeni_vysledku_do_csv(seznam_obci: list[dict], csv_soubor: str) -> None:
    """
    | Uloží obsah z dictionary s výsledky voleb v obci do csv souboru
    | Pokud je csv soubor již otevřen, tak zahlácí chybu a ukončí program

    | Argument:
    | seznam_obci: list dictionary, obsahující výsledky z jednotlivých obcí
    | csv_soubor: název csv souboru, do kterého se výsledky uloží
    """

    try:
        print(f"Zapisuji data do souboru: {csv_soubor}")
        zahlavi = seznam_obci[0].keys()
        with open(
            csv_soubor, mode="w", newline="", encoding="utf-8-sig"
        ) as soubor:
            zapisovac = csv.DictWriter(
                soubor, fieldnames=zahlavi, delimiter=";"
            )
            zapisovac.writeheader()
            zapisovac.writerows(seznam_obci)
    except PermissionError:
        print("Soubor je otevřený. Zavřete ho prosím!")


def ziskani_seznamu_moznych_url(
    pocatecni_index_tabulky: int = 1, konecny_index_tabulky: int = 15
) -> list:
    """
    | Ziska z vybrane url adresy seznam všech url adres, které je možné zadávat jako argument pro získání výsledku voleb

    | Vrací:
    | list url adres pro porovnání se zadanou url adresou
    """

    seznam_odkazu = list()
    url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    parsovana_odpoved = ziskani_parsovane_odpovedi(url)

    for index in range(pocatecni_index_tabulky, konecny_index_tabulky):
        hodnota_atributu = f"t{index}sa3"
        td_tagy = ziskani_td_tagu(
            parsovana_odpoved, "headers", hodnota_atributu
        )
        for td_tag in td_tagy:
            novy_odkaz = td_tag.find("a")["href"]
            seznam_odkazu.append(
                f"https://volby.cz/pls/ps2017nss/{novy_odkaz}"
            )

    return seznam_odkazu


def kontrola_vstupnich_argumentu(seznam_moznych_url: list) -> str:
    """
    | Porovná argumenty zadaná při spuštění scriptu a neumožní získat výsledky o hlasování ze zahraničí:
    |   1) Zda jsou zadány 2 argumenty a ve správném pořadí
    |   2) Zda je url adresa v seznamu možných url adres
    |   3) Zda je soubor pro uložení výsledků typu csv a má délku alespoň 1 znak

    | Argument:
    | seznam_moznych_url: list obsahující seznam url, které je možné zadat

    | Vrací:
    | url_okres: string s validní url adresou
    | csv_soubor: string s validním nízvem souboru pro uložení výsledků
    """

    try:
        url_okres = sys.argv[1]
        csv_soubor = sys.argv[2]
    except IndexError:
        print("Nezadán dostatečný počet argumentů")
        sys.exit()

    if "https://www.volby.cz/" in url_okres:
        url_okres = url_okres.replace(
            "https://www.volby.cz/", "https://volby.cz/"
        )

    if url_okres == "https://volby.cz/pls/ps2017nss/ps36?xjazyk=CZ":
        print("Není možné scrapovat data o volbách ze zahraničí.")
        sys.exit()
    elif url_okres not in seznam_moznych_url:
        print("Zadána špatná url adresa.")
        sys.exit()
    elif not csv_soubor.endswith(".csv") or len(csv_soubor) < 5:
        print("Zadán špatný soubor pro uložení")
        sys.exit()

    return url_okres, csv_soubor


if __name__ == "__main__":

    seznam_moznych_url = ziskani_seznamu_moznych_url()

    (url_okres, csv_soubor) = kontrola_vstupnich_argumentu(seznam_moznych_url)

    zvoleny_kraj = url_okres.split("&")[1]
    zvoleny_vyber = url_okres.split("xnumnuts=")[1]

    print(f"Stahuji data z vybraneho url: {url_okres}")

    seznam_obci = ziskani_obci(url_okres)
    for dict_obce in seznam_obci:
        ziskani_vysledku_obce(dict_obce, zvoleny_kraj, zvoleny_vyber)

    ulozeni_vysledku_do_csv(seznam_obci, csv_soubor)

print(f"Ukončuji {sys.argv[0]}")
