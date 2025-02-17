from sqlalchemy import Column, String, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

Base = declarative_base()
engine = create_engine('sqlite:///investor.db')

class Companies(Base):
    __tablename__ = 'companies'

    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)

class Financial(Base):
    __tablename__ = 'financial'

    ticker = Column(String, primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)

    def get_ebitda(self):
        return self.ebitda if self.ebitda else 0
    def get_sales(self):
        return self.sales if self.sales else 0
    def get_net_profit(self):
        return self.net_profit if self.net_profit else 0
    def get_market_price(self):
        return self.market_price if self.market_price else 0
    def get_net_debt(self):
        return self.net_debt if self.net_debt else 0
    def get_assets(self):
        return self.assets if self.assets else 0
    def get_equity(self):
        return self.equity if self.equity else 0
    def get_cash_equivalents(self):
        return self.cash_equivalents if self.cash_equivalents else 0
    def get_liabilities(self):
        return self.liabilities if self.liabilities else 0


Session = sessionmaker(bind=engine)
session = Session()


def get_companies_by_mame(search: str) -> dict:
    query = (select(Companies, Financial)
             .join(Financial, Companies.ticker == Financial.ticker)
             .filter(Companies.name.ilike(f'%{search}%')))
    result = session.execute(query)

    company_list = dict()
    i = 0
    for company, financial in result.all():
        company_list[i] = {
            'company': company,
            'financial': financial,
        }
        i += 1

    return company_list

def get_main_menu() -> dict:
    return  {
        'title': 'MAIN MENU',
        'items': {
            0: {
                'name': 'Exit',
            },
            1: {
                'name': 'CRUD operations',
                'title': 'CRUD MENU',
                'items': {
                    0: {'name': 'Back'},
                    1: {'name': 'Create a company'},
                    2: {'name': 'Read a company'},
                    3: {'name': 'Update a company'},
                    4: {'name': 'Delete a company'},
                    5: {'name': 'List all companies'},
                }
            },
            2: {
                'name': 'Show top ten companies by criteria',
                'title': 'TOP TEN MENU',
                'items': {
                    0: {'name': 'Back'},
                    1: {'name': 'List by ND/EBITDA'},
                    2: {'name': 'List by ROE'},
                    3: {'name': 'List by ROA'},
                }
            }
        }
    }

def print_menu(menu: dict[int, str|dict]):
    print(menu.get('title'))
    for i, item in menu.get('items').items():
        print(f'{i} {item.get("name")}')
    print('')

def get_option(menu: dict[int, str|dict]) -> int:
    try:
        option = int(input('Enter an option: '))
        if option in menu.get('items'):
            return option
        else:
            print('Invalid option!\n')
    except ValueError:
        print('Invalid option!\n')

    return -1

def create_company():
    ticker = input("Enter ticker (in the format 'MOON'): ")
    company = input("Enter company (in the format 'Moon Corp'): ")
    industries = input("Enter industries (in the format 'Technology'): ")

    company = Companies(ticker=ticker, name=company, sector=industries)
    session.add(company)

    ebitda = float(input("Enter ebitda (in the format '987654321'): "))
    sales = float(input("Enter sales (in the format '987654321'): "))
    net_profit = float(input("Enter net profit (in the format '987654321'): "))
    market_price = float(input("Enter market price (in the format '987654321'): "))
    net_debt = float(input("Enter net debt (in the format '987654321'): "))
    assets = float(input("Enter assets (in the format '987654321'): "))
    equity = float(input("Enter equity (in the format '987654321'): "))
    cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'): "))
    liabilities = float(input("Enter liabilities (in the format '987654321'): "))

    financial = Financial(
        ticker=ticker,
        ebitda=ebitda,
        sales=sales,
        net_profit=net_profit,
        market_price=market_price,
        net_debt=net_debt,
        assets=assets,
        equity=equity,
        cash_equivalents=cash_equivalents,
        liabilities=liabilities
    )
    session.add(financial)

    session.commit()

    print('Company created successfully!\n')

def get_company():
    search = input("Enter company name: ")
    company_list = get_companies_by_mame(search)

    for i, (key, company) in enumerate(company_list.items()):
        print(str(key) + ' ' + company['company'].name)

    if len(company_list) > 0:
        number = int(input('Enter company number: '))
        company = company_list[number]

        print(company['company'].ticker + ' ' + company['company'].name)
        print('P/E = ' + str(
            round(company['financial'].get_market_price() / company['financial'].get_net_profit(), 2) if company['financial'].net_profit else None
        ))
        print('P/S = ' + str(
            round(company['financial'].get_market_price() / company['financial'].get_sales(), 2) if company['financial'].sales else None
        ))
        print('P/B = ' + str(
            round(company['financial'].get_market_price() / company['financial'].get_assets(), 2) if company['financial'].assets else None
        ))
        print('ND/EBITDA = ' + str(
            round(company['financial'].get_net_debt() / company['financial'].get_ebitda(), 2) if company['financial'].ebitda else None
        ))
        print('ROE = ' + str(
            round(company['financial'].get_net_profit() / company['financial'].get_equity(), 2) if company['financial'].equity else None
        ))
        print('ROA = ' + str(
            round(company['financial'].get_net_profit() / company['financial'].get_assets(), 2) if company['financial'].assets else None
        ))
        print('L/A = ' + str(
            round(company['financial'].get_liabilities() / company['financial'].get_assets(), 2) if company['financial'].assets else None
        ))
        print('')

    else:
        print('Company not found!\n')

def upd_company():
    search = input("Enter company name: ")
    company_list = get_companies_by_mame(search)

    for i, (key, company) in enumerate(company_list.items()):
        print(str(key) + ' ' + company['company'].name)

    if len(company_list) > 0:
        number = int(input('Enter company number: '))
        company = company_list[number]

        ebitda = float(input("Enter ebitda (in the format '987654321'): "))
        sales = float(input("Enter sales (in the format '987654321'): "))
        net_profit = float(input("Enter net profit (in the format '987654321'): "))
        market_price = float(input("Enter market price (in the format '987654321'): "))
        net_debt = float(input("Enter net debt (in the format '987654321'): "))
        assets = float(input("Enter assets (in the format '987654321'): "))
        equity = float(input("Enter equity (in the format '987654321'): "))
        cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'): "))
        liabilities = float(input("Enter liabilities (in the format '987654321'): "))

        query = session.query(Financial).filter(Financial.ticker == company['company'].ticker)
        query.update({
            "ebitda": ebitda,
            "sales": sales,
            "net_profit": net_profit,
            "market_price": market_price,
            "net_debt": net_debt,
            "assets": assets,
            "equity": equity,
            "cash_equivalents": cash_equivalents,
            "liabilities": liabilities
        })
        session.commit()

        print('Company updated successfully!\n')

    else:
        print('Company not found!\n')

def del_company():
    search = input("Enter company name: ")
    company_list = get_companies_by_mame(search)

    for i, (key, company) in enumerate(company_list.items()):
        print(str(key) + ' ' + company['company'].name)

    if len(company_list) > 0:
        number = int(input('Enter company number: '))
        company = company_list[number]

        session.query(Companies).filter(Companies.ticker == company['company'].ticker).delete()
        session.query(Financial).filter(Financial.ticker == company['company'].ticker).delete()
        session.commit()

        print('Company deleted successfully!\n')

    else:
        print('Company not found!\n')

def list_companies():
    print('COMPANY LIST')

    query = session.query(Companies).order_by(Companies.ticker.asc())
    for company in query.all():
        print(company.ticker + ' ' + company.name + ' ' + company.sector)

def list_companies_by_nd_ebitda():
    print('TICKER ND/EBITDA')

    query = (session.query(Companies, Financial)
             .join(Financial, Companies.ticker == Financial.ticker)
             .order_by((Financial.net_debt / Financial.ebitda).desc())
             .limit(10))
    for company, financial in query.all():
        val = round(financial.net_debt / financial.ebitda, 2)
        print(company.ticker + ' ' + str(val))

def list_companies_by_roe():
    print('TICKER ROE')

    query = (session.query(Companies, Financial)
             .join(Financial, Companies.ticker == Financial.ticker)
             .order_by((Financial.net_profit / Financial.equity).desc())
             .limit(10))
    for company, financial in query.all():
        val = round(financial.net_profit / financial.equity, 2)
        print(company.ticker + ' ' + str(val))

def list_companies_by_roa():
    print('TICKER ROA')

    query = (session.query(Companies, Financial)
             .join(Financial, Companies.ticker == Financial.ticker)
             .order_by((Financial.net_profit / Financial.assets).desc())
             .limit(10))
    for company, financial in query.all():
        val = round(financial.net_profit / financial.assets, 2)
        print(company.ticker + ' ' + str(val))

###

print('Welcome to the Investor Program!')

main_menu = get_main_menu()
level_0 = -1

while level_0 != 0:
    if level_0 < 1:
        print_menu(main_menu)
        level_0 = get_option(main_menu)
    else:
        sub_menu = main_menu.get('items').get(level_0)
        print('')
        print_menu(sub_menu)

        level_1 = get_option(sub_menu)

        match level_0:
            case 1:
                match level_1:
                    case 1:
                        create_company()
                    case 2:
                        get_company()
                    case 3:
                        upd_company()
                    case 4:
                        del_company()
                    case 5:
                        list_companies()
            case 2:
                match level_1:
                    case 1:
                        list_companies_by_nd_ebitda()
                    case 2:
                        list_companies_by_roe()
                    case 3:
                        list_companies_by_roa()

        level_0 = -1

print('Have a nice day!')
