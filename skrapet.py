import requests
import time
from bs4 import BeautifulSoup as bs

URL = 'https://www.ss.lv/lv/transport/cars/today/sell/'
LAPAS = 'lapas/'

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
        print(rinda)
        print("=======================")
        print("=======================")
        print("=======================")    

info('lapas/1_lapa.html')