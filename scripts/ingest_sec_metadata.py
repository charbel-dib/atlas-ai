import argparse
import json

from sqlalchemy import select

from atlas.db.database import SessionLocal
from atlas.db.models import Company, Document
from atlas.ingestion.raw_store import save_raw_response
from atlas.ingestion.sec_client import SecClient
from atlas.ingestion.sec_filings import (
    find_latest_filing,
    submissions_url,
)


def main(ticker: str) -> None:
    ticker = ticker.upper()

    with SessionLocal() as session:
        company = session.scalar(select(Company).where(Company.ticker == ticker))

        if company is None:
            raise ValueError(f"Company {ticker} does not exist in database.")

        url = submissions_url(company.cik)

        print(f"Fetching: {url}")

        with SecClient() as client:
            response = client.get(url)

        raw_path = save_raw_response(
            ticker=company.ticker,
            filename="submissions.json",
            content=response.content,
            source_url=url,
        )

        print(f"Raw SEC metadata stored at: {raw_path}")

        submissions = json.loads(response.content)

        filing = find_latest_filing(
            submissions=submissions,
            cik=company.cik,
            form_type="10-K",
        )

        print()
        print("Latest 10-K")
        print("-----------")
        print("Form:", filing.form)
        print("Filing date:", filing.filing_date)
        print("Report date:", filing.report_date)
        print("Accession:", filing.accession_number)
        print("Primary document:", filing.primary_document)
        print("Archive URL:", filing.archive_url)

        existing_document = session.scalar(
            select(Document).where(
                Document.company_id == company.id,
                Document.accession_number == filing.accession_number,
            )
        )

        if existing_document:
            print()
            print("Document already exists in database. Skipping insert.")
            return

        document = Document(
            company_id=company.id,
            accession_number=filing.accession_number,
            document_type=filing.form,
            filing_date=filing.filing_date,
            title=(f"{company.name} {filing.form} filed {filing.filing_date}"),
            source_url=filing.archive_url,
        )

        session.add(document)
        session.commit()
        session.refresh(document)

        print()
        print(f"Created document database row with id={document.id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "ticker",
        help="Company ticker, for example NVDA",
    )

    args = parser.parse_args()

    main(args.ticker)
