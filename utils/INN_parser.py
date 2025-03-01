import requests
import json
import datetime as dt
import httpx
from bs4 import BeautifulSoup


def parse_inn(inn):
    try:
        response = requests.get(f'https://api-fns.ru/api/search?q={inn}&key=32689b0a573b4e56a63bd753a6531da27cce0896')
        print(response.status_code, response.text)
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


if __name__ == "__main__":
    default_inn = 623008230466
    print(parse_inn(str(default_inn)))
    response = parse_inn_self_employed(str(default_inn))
    print(response)

# username = ip_data["ФИОПолн"]
# inn = ip_data["ИНН"]
# ogrn = ip_data["ОГРН"]
# date_ogrn = ip_data["ДатаОГРН"]
# status = ip_data["Статус"]
# address = ip_data["АдресПолн"]
# activity = ip_data["ОснВидДеят"]

# print(f"ФИО: {username}")
# print(f"ИНН: {inn}")
# print(f"ОГРН: {ogrn}")
# print(f"Дата ОГРН: {date_ogrn}")
# print(f"Статус: {status}")
# print(f"Адрес: {address}")
# print(f"Вид деятельности: {activity}")

# print(page)
