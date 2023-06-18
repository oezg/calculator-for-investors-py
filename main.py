from investor import *
from sqlalchemy import func, desc

MAIN_MENU = {
    'name': 'MAIN MENU',
    '0': 'Exit',
    '1': 'CRUD operations',
    '2': 'Show top ten companies by criteria',
}

CRUD_MENU = {
    'name': 'CRUD MENU',
    '0': 'Back',
    '1': 'Create a company',
    '2': 'Read a company',
    '3': 'Update a company',
    '4': 'Delete a company',
    '5': 'List all companies',
}

TOP_TEN_MENU = {
    'name': 'TOP TEN MENU',
    '0': 'Back',
    '1': 'List by ND/EBITDA',
    '2': 'List by ROE',
    '3': 'List by ROA',
}


def main() -> None:
    match get_option(MAIN_MENU):
        case '0':
            print('Have a nice day!')
        case '1':
            crud()
        case '2':
            top_ten()


def crud() -> None:
    match get_option(CRUD_MENU):
        case '1':
            create_company()
        case '2':
            read_company()
        case '3':
            update_company()
        case '4':
            delete_company()
        case '5':
            list_all_companies()
    main()


def top_ten() -> None:
    option = input(get_menu(TOP_TEN_MENU))
    if option in ('1', '2', '3'):
        match option:
            case '1':
                lst = get_top_ten(Financial.net_debt, Financial.ebitda)
            case '2':
                lst = get_top_ten(Financial.net_profit, Financial.equity)
            case _:
                lst = get_top_ten(Financial.net_profit, Financial.assets)
        list_top_ten(option, lst)
    elif option != '0':
        print('Invalid option!')
    main()


def list_top_ten(option, lst):
    print(TOP_TEN_MENU[option].replace('List by', 'TICKER'))
    for company in lst:
        print(f"{company.ticker} {round(company.ratio, 2)}")


def get_top_ten(a, b):
    session = get_session()
    lst = session.query(Financial.ticker, func.round(a / b, 2).label('ratio')).order_by(desc('ratio')).limit(10).all()
    session.close()
    return lst


def create_company():
    session = get_session()
    ticker = input("Enter ticker (in the format 'MOON'):\n")
    session.add(Companies(ticker=ticker, name=input("Enter company (in the format 'Moon Corp'):\n"),
                          sector=input("Enter industries (in the format 'Technology'):\n")))
    values = values_generator()
    session.add(Financial(ticker=ticker, ebitda=next(values), sales=next(values),
                          net_profit=next(values), market_price=next(values), net_debt=next(values),
                          assets=next(values), equity=next(values), cash_equivalents=next(values),
                          liabilities=next(values)))
    session.commit()
    session.close()
    print('Company created successfully!')


def values_generator():
    for x in ("ebitda,sales,net_profit,market_price,net_debt,assets,equity,cash_equivalents,liabilities".split(",")):
        try:
            y = float(input(f"Enter {x.replace('_', ' ')} (in the format '987654321'):\n"))
        except ValueError:
            y = None
        yield y


def read_company():
    if found := find_company_name_and_ticker():
        session = get_session()
        record = session.query(Financial).filter(Financial.ticker == found[1])[0]
        session.close()
        print(found[1], found[0])
        print(f"P/E = {divide(record.market_price, record.net_profit)}")
        print(f"P/S = {divide(record.market_price, record.sales)}")
        print(f"P/B = {divide(record.market_price, record.assets)}")
        print(f"ND/EBITDA = {divide(record.net_debt, record.ebitda)}")
        print(f"ROE = {divide(record.net_profit, record.equity)}")
        print(f"ROA = {divide(record.net_profit, record.assets)}")
        print(f"L/A = {divide(record.liabilities, record.assets)}")


def find_company_name_and_ticker():
    session = get_session()
    found = session.query(Companies).filter(Companies.name.like('%{}%'.format(input("Enter company name:\n")))).all()
    if not found:
        print("Company not found!")
        session.close()
        return
    for i, company in enumerate(found):
        print(f"{i} {company.name}")
    try:
        company = found[int(input("Enter company number:\n"))]
    except (ValueError, IndexError):
        print("Invalid input!")
    else:
        return company.name, company.ticker
    finally:
        session.close()


def divide(a, b):
    if a is None or b is None or b == 0:
        return None
    return round(a / b, 2)


def update_company():
    if found := find_company_name_and_ticker():
        values = values_generator()
        session = get_session()
        record = session.query(Financial).filter(Financial.ticker == found[1])
        record.update({'ebitda': next(values), 'sales': next(values), 'net_profit': next(values),
                       'market_price': next(values), 'net_debt': next(values), 'assets': next(values),
                       'equity': next(values), 'cash_equivalents': next(values), 'liabilities': next(values)})
        session.commit()
        session.close()
        print("Company updated successfully!")


def delete_company():
    if found := find_company_name_and_ticker():
        session = get_session()
        session.query(Companies).filter(Companies.ticker == found[1]).delete()
        session.query(Financial).filter(Financial.ticker == found[1]).delete()
        session.commit()
        session.close()
        print("Company deleted successfully!")


def list_all_companies():
    print("COMPANY LIST")
    session = get_session()
    for company in session.query(Companies).order_by(Companies.ticker).all():
        print(f"{company.ticker} {company.name} {company.sector}")
    session.close()


def get_option(menu: dict[str, str]) -> str:
    while (option := input(get_menu(menu))) not in menu:
        print('Invalid option!')
    return option


def get_menu(menu: dict[str, str]) -> str:
    menu_string = '\n'.join(f'{k} {v}' for k, v in menu.items() if k != 'name')
    return f'{menu["name"]}\n{menu_string}\nEnter an option:\n'


if __name__ == '__main__':
    prepare_database()
    main()
