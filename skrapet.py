import requests

URL = 'https://www.ss.lv/lv/transport/cars/today/sell/'
LAPAS = 'lapas/'

rezultats = requests.get(URL)
if rezultats.status_code == 200:
    with open('1_lapa.html', 'w', encoding='UTF-8') as f:
        f.write(rezultats.text)
else:
    print(f"ERROR: Statusa kods {rezultats.status_code}")