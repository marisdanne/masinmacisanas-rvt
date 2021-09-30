import requests
import time

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

        