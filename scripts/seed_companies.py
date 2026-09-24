from sqlalchemy import select

from atlas.db.database import SessionLocal
from atlas.db.models import Company

COMPANIES = [
    {
        "name": "NVIDIA Corporation",
        "ticker": "NVDA",
        "cik": "0001045810",
    },
    {
        "name": "Advanced Micro Devices, Inc.",
        "ticker": "AMD",
        "cik": "0000002488",
    },
    {
        "name": "Microsoft Corporation",
        "ticker": "MSFT",
        "cik": "0000789019",
    },
]


def main() -> None:
    with SessionLocal() as session:
        for company_data in COMPANIES:
            ticker = company_data["ticker"]

            statement = select(Company).where(Company.ticker == ticker)

            existing_company = session.scalar(statement)

            if existing_company:
                print(f"{ticker} already exists, skipping.")
                continue

            company = Company(**company_data)

            session.add(company)

            print(f"Adding {ticker}.")

        session.commit()

    print("Company seeding completed.")


if __name__ == "__main__":
    main()
