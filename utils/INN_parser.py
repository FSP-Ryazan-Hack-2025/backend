import requests
import json
import datetime as dt
import httpx
from bs4 import BeautifulSoup


def parse_inn(inn: str):
    try:
        response = requests.get(f'https://api-fns.ru/api/search?q={inn}&key=32689b0a573b4e56a63bd753a6531da27cce0896')
        #print(response.status_code, response.text)

        page = BeautifulSoup(response.text, 'html5lib')
        json_data = json.loads(page.body.text)
        ip_data = list(json_data["items"][0].values())

        return ip_data[0]
    
    except Exception as e:
        print(e)
        return ValueError('Неверный ИНН')
        # raise ValueError('Неверный ИНН')


def parse_inn_self_employed(inn: str, date: dt.date = None) -> dict:

    date = date or dt.date.today()
    date_str = date.isoformat()
    url = "https://statusnpd.nalog.ru/api/v1/tracker/taxpayer_status"
    
    data = {
        "inn": inn,
        "requestDate": date_str,
    }

    resp = httpx.post(url=url, json=data)
    return resp.json()


def parse_passport_data(fam: str, nam: str, otch: str, bdate: str, docno: str):
    try:

        response = requests.get(f'https://api-fns.ru/api/innfl?fam={fam}&nam={nam}&otch={otch}&bdate={bdate}&doctype=21&docno={docno}&key=32689b0a573b4e56a63bd753a6531da27cce0896')
        #print(response.status_code, response.text)
        page = BeautifulSoup(response.text, 'html5lib')
        json_data = json.loads(page.body.text)
        ip_data = list(json_data["items"][0].values())

        return ip_data[0]
    
    except Exception as e:
        print(e)
        return ValueError('Неверные паспортные данные')
        # raise ValueError('Неверные паспортные данные')



