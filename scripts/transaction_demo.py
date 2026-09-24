from sqlalchemy import select

from atlas.db.database import SessionLocal
from atlas.db.models import Company


def main() -> None:
    with SessionLocal() as session:
        try:
            company = Company(
                name="Fake Test Company",
                ticker="TEST",
                cik="9999999999",
            )

            session.add(company)

            print("Company added to session.")

            raise RuntimeError("Simulated failure!")

            session.commit()

        except RuntimeError as exc:
            print(f"Something failed: {exc}")
            print("Rolling back transaction.")

            session.rollback()

    with SessionLocal() as session:
        statement = select(Company).where(Company.ticker == "TEST")

        company = session.scalar(statement)

        print("Company in database:", company)


if __name__ == "__main__":
    main()
