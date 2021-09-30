import requests
import time
from bs4 import BeautifulSoup as bs
import csv

URL = 'https://www.ss.lv/lv/transport/cars/today/sell/'
LAPAS = 'lapas/'
DATI = 'dati/'

def saglabat(url, datne):
    rezultats = requests.get(url)
    if rezultats.status_code == 200:
        with open(f"{LAPAS}{datne}", 'w', encoding='UTF-8') as f:
            f.write(rezultats.text)
    else:
        print(f"ERROR: Statusa kods {rezultats.status_code}")

def lejupieladet_lapas(cik):
    for i in range(1, cik + 1):
        saglabat(f"{URL}/page{i}.html", f"{i}_lapa.html")
        time.sleep(1)


def info(datne):
    dati = []
    with open(datne, 'r', encoding='UTF-8') as f:
        html = f.read()

    zupa = bs(html, "html.parser")

    galvena = zupa.find(id = 'page_main')

    tabulas = galvena.find_all("table")

    # for tabula in tabulas:
    #     print(tabula)
    #     print("=======================")
    #     print("=======================")
    #     print("=======================")

    auto_tabula = tabulas[2]

    rindas = auto_tabula.find_all("tr")

    for rinda in rindas[1:-1]:
        auto = {}
        # print(rinda)
        # print("=======================")
        # print("=======================")
        # print("=======================")    

        lauki = rinda.find_all("td")
        # for lauks in lauki:
        #     print(lauks)
        #     print("=======================")
        
        auto['saite'] = lauki[1].find("a")["href"]
        auto['bilde'] = lauki[1].find("img")["src"]
        auto['apraksts'] = lauki[2].find("a").text.replace("\n", "")

        lauki[3].br.replace_with('!')
        auto['marka'] = lauki[3].text.replace("!", " ")
        auto['razotajs'] = lauki[3].text.split("!")[0]
        auto['modelis'] = lauki[3].text.split("!")[1]

        auto['gads'] = lauki[4].text

        tilpums = lauki[5].text
        if tilpums[-1] == "D":
            auto['tilpums'] = tilpums[:-1]
            auto['dzinejs'] = "Dīzelis"
        elif tilpums[-1] == "H":
            auto['tilpums'] = tilpums[:-1]
            auto['dzinejs'] = "Hibrīds"
        elif tilpums[-1] == "E":
            auto['tilpums'] = 0
            auto['dzinejs'] = "Elektro"
        else:
            auto['tilpums'] = tilpums
            auto['dzinejs'] = "Benzīns"
        
        
        if lauki[6].text != "-":
            auto['nobraukums'] = lauki[6].text.replace(" tūkst.", "")
        else:
            continue

        auto['cena'] = lauki[7].text.replace("  €", "").replace(",", "")
        
        dati.append(auto)

    return dati

def saglabat_datus(dati):
    with open(f"{DATI}ss_lv_auto.csv", 'w', encoding='UTF-8', newline="") as f:
        kolonu_nosaukumi = ['razotajs', 'modelis', 'marka', 'gads', 'tilpums', 'dzinejs', 'nobraukums', 'cena', 'apraksts', 'bilde', 'saite']
        w = csv.DictWriter(f, fieldnames= kolonu_nosaukumi)
        w.writeheader()
        for auto in dati:
            w.writerow(auto)


automasinas = info('lapas/1_lapa.html')
saglabat_datus(automasinas)