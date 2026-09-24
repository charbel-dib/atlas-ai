from sqlalchemy import select

from atlas.db.database import SessionLocal
from atlas.db.models import Company


def main() -> None:
    with SessionLocal() as session:
        statement = select(Company).order_by(Company.ticker)

        companies = session.scalars(statement).all()

        for company in companies:
            print(
                company.id,
                company.name,
                company.ticker,
                company.cik,
            )


if __name__ == "__main__":
    main()
