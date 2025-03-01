import datetime as dt
from INN_parser import parse_passport_data, parse_inn, parse_inn_self_employed

def parse_comparator(inn: str, fam: str, nam: str, otch: str, bdate: str, docno: str,  date: dt.date = None):

    fam = fam.lower()
    nam = nam.lower()
    otch = otch.lower()

    inn_data = parse_inn(inn)
    passport_data = parse_passport_data(fam, nam, otch, bdate, docno)

    if inn != passport_data:
        return False
    
    elif inn_data == ValueError('Неверный ИНН'):
        tax_data = parse_inn_self_employed(inn, date)
        return tax_data["status"]
    
    else:
        username = [x.lower() for x  in inn_data["ФИОПолн"].split()]
        address = inn_data["АдресПолн"]
        activity = inn_data["ОснВидДеят"]   
        if username == [fam, nam, otch] and inn == passport_data and "Рязан" in address:
            return [username, address, activity]
        else:
            return False


if __name__ == "__main__":
    default_inn = "623008230466"
    print(parse_comparator(default_inn, "Панков", "Иван", "Александрович", "06.11.2005", "6119147212"))