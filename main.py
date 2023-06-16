import investor

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
    match get_option(TOP_TEN_MENU):
        case '0':
            main()
        case _:
            print('Not implemented!')
            main()


def create_company():
    session = investor.Session()
    ticker = input("Enter ticker (in the format 'MOON'):\n")
    session.add(investor.Companies(ticker=ticker, name=input("Enter company (in the format 'Moon Corp'):\n"),
        sector=input("Enter industries (in the format 'Technology'):\n")))
    values = values_generator()
    session.add(investor.Financial(ticker=ticker, ebitda=next(values), sales=next(values),
        net_profit=next(values), market_price=next(values), net_debt=next(values), assets=next(values),
        equity=next(values), cash_equivalents=next(values), liabilities=next(values)))
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
    ...


def update_company():
    ...


def delete_company():
    ...


def list_all_companies():
    ...


def get_option(menu: dict[str, str]) -> str:
    while (option := input(get_menu(menu))) not in menu:
        print('Invalid option!')
    return option


def get_menu(menu: dict[str, str]) -> str:
    menu_string = '\n'.join(f'{k} {v}' for k, v in menu.items() if k != 'name')
    return f'\n{menu["name"]}\n{menu_string}\n\nEnter an option:\n'


if __name__ == '__main__':
    investor.prepare_database()
    main()
