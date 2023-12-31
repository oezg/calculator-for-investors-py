import csv
import os.path
import sqlalchemy.orm
from contextlib import contextmanager

engine = sqlalchemy.create_engine("sqlite:///investor.db")
Base = sqlalchemy.orm.declarative_base()


@contextmanager
def session_manager():
    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    yield session
    session.commit()
    session.close()


class Companies(Base):
    __tablename__ = 'companies'

    ticker = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    sector = sqlalchemy.Column(sqlalchemy.String)


class Financial(Base):
    __tablename__ = 'financial'

    ticker = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    ebitda = sqlalchemy.Column(sqlalchemy.Float)
    sales = sqlalchemy.Column(sqlalchemy.Float)
    net_profit = sqlalchemy.Column(sqlalchemy.Float)
    market_price = sqlalchemy.Column(sqlalchemy.Float)
    net_debt = sqlalchemy.Column(sqlalchemy.Float)
    assets = sqlalchemy.Column(sqlalchemy.Float)
    equity = sqlalchemy.Column(sqlalchemy.Float)
    cash_equivalents = sqlalchemy.Column(sqlalchemy.Float)
    liabilities = sqlalchemy.Column(sqlalchemy.Float)


def prepare_database() -> None:
    if not os.path.exists('investor.db'):
        Base.metadata.create_all(engine)
        read_companies()
        read_financial()
    print("Welcome to the Investor Program!")


def read_companies() -> None:
    with open("test/companies.csv") as csv_file, session_manager() as session:
        companies_reader = csv.DictReader(csv_file)
        for company in companies_reader:
            session.add(Companies(ticker=company['ticker'], name=company['name'], sector=company['sector']))


def read_financial() -> None:
    with open("test/financial.csv") as csv_file, session_manager() as session:
        financial_reader = csv.DictReader(csv_file)
        for financial in financial_reader:
            session.add(Financial(
                    ticker=financial['ticker'],
                    ebitda=financial['ebitda'] if financial['ebitda'] else None,
                    sales=financial['sales'] if financial['sales'] else None,
                    net_profit=financial['net_profit'] if financial['net_profit'] else None,
                    market_price=financial['market_price'] if financial['market_price'] else None,
                    net_debt=financial['net_debt'] if financial['net_debt'] else None,
                    assets=financial['assets'] if financial['assets'] else None,
                    equity=financial['equity'] if financial['equity'] else None,
                    cash_equivalents=financial['cash_equivalents'] if financial['cash_equivalents'] else None,
                    liabilities=financial['liabilities'] if financial['liabilities'] else None))
