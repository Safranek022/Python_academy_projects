# Election Scraper

Třetí projekt Python akademiie od Engeta

## Popis projektu

Tento projekt slouží k extrahování výsledků parlamentních voleb v ČR v roce 2017. Odkaz je je zde [a link](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). Výsledky jsou vyextrahovány do csv souboru.

## Table of Contents

- [Popis projektu](#popis)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Instalace knihoven

Knihovny a jejich správné verze, které jsou použity v kódu, jsou uložené v souboru requirements.txt. Pro instalaci je doporučeno použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
$ pip --version #ověření verze manageru
$ pip install -r requirements.txt #instalace použitých knihoven

## Spuštění projektu

Soubor elections_scraper.py se spouští v rámci příkazové řádky. Pro spuštění je nutné zadat dva povinné argumenty:
<odkaz_uzemniho_celku> - je nutné zvolit url z části pro výběr obce
<vysledny_soubor> - je nutné zvolit soubor s příponou .csv

python election_scraper.py <odkaz_uzemniho_celku> <vysledny_soubor>

Po spuštění dojde ke stažení dat ze zvoleného odkazu do souboru csv s zvoleným názvem.
Projekt neumožňuje extrahovat výsledky voleb v zahraničí.

## Ukázka projektu

Výsledky hlasování pro okres Rakovník:

![Vyber okresu](vyber_okresu.png)

1.  argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2112
2.  argument: vysleky_rakovnik.csv

Průběh stahování:
Stahuji data z vybraneho url: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2112
Zapisuji data do souboru: vysledky_rakovnik.csv
Ukončuji election_scraper.py

Částečný výstup:
[{'code': '565423', 'location': 'Bdín', 'registered': 51, 'envelopes': 34, 'valid': 34, 'Občanská demokratická strana': 1, 'Řád národa - Vlastenecká unie': 0, 'CESTA ODPOVĚDNÉ SPOLEČNOSTI': 0, 'Česká str.sociálně demokrat.': 7, 'Radostné Česko': 0, 'STAROSTOVÉ A
NEZÁVISLÍ': 1, 'Komunistická str.Čech a Moravy': 1, 'Strana zelených': 1, 'ROZUMNÍ-stop migraci,diktát.EU': 0, 'Strana svobodných občanů': 0, 'Blok proti islam.-Obran.domova': 0, 'Občanská demokratická aliance': 0, 'Česká pirátská strana': 3, 'Unie H.A.V.E.L.': 0, 'Referendum o Evropské unii': 0, 'TOP 09': 1, 'ANO 2011': 15, 'Dobrá volba 2016': 0, 'SPR-Republ.str.Čsl. M.Sládka': 0, 'Křesť.demokr.unie-Čs.str.lid.': 0, 'Česká strana národně sociální': 0, 'REALISTÉ': 0, 'SPORTOVCI': 0, 'Dělnic.str.sociální spravedl.': 0, 'Svob.a př.dem.-T.Okamura (SPD)': 4, 'Strana Práv Občanů': 0},...]
