import csv

from sqlalchemy import Column, String, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

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


Base.metadata.create_all(engine)

###

Session = sessionmaker(bind=engine)
session = Session()

with open('test/companies.csv', 'r') as csv_file:
    csv_file_reader = csv.DictReader(csv_file, delimiter=",")
    for line in csv_file_reader:
        company = Companies(ticker=line['ticker'], name=line['name'], sector=line['sector'])
        session.add(company)

with open('test/financial.csv', 'r') as csv_file:
    csv_file_reader = csv.DictReader(csv_file, delimiter=",")
    for line in csv_file_reader:
        financial = Financial(
            ticker=line['ticker'],
            ebitda=float(line['ebitda']) if line['ebitda'] != '' else None,
            sales=float(line['sales']) if line['sales'] != '' else None,
            net_profit=float(line['net_profit']) if line['net_profit'] != '' else None,
            market_price=float(line['market_price']) if line['market_price'] != '' else None,
            net_debt=float(line['net_debt']) if line['net_debt'] != '' else None,
            assets=float(line['assets']) if line['assets'] != '' else None,
            equity=float(line['equity']) if line['equity'] != '' else None,
            cash_equivalents=float(line['cash_equivalents']) if line['cash_equivalents'] != '' else None,
            liabilities=float(line['liabilities']) if line['liabilities'] != '' else None
        )
        session.add(financial)

session.commit()

print('Database created successfully!')