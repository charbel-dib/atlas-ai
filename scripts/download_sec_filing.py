import argparse

from sqlalchemy import select

from atlas.db.database import SessionLocal
from atlas.db.models import Company, Document
from atlas.ingestion.sec_downloader import download_filing


def main(ticker: str) -> None:
    ticker = ticker.upper()

    with SessionLocal() as session:
        company = session.scalar(select(Company).where(Company.ticker == ticker))

        if company is None:
            raise ValueError(f"Unknown company ticker: {ticker}")

        document = session.scalar(
            select(Document)
            .where(
                Document.company_id == company.id,
                Document.document_type == "10-K",
            )
            .order_by(Document.filing_date.desc())
        )

        if document is None:
            raise ValueError(
                f"No 10-K found for {ticker}. Run SEC metadata ingestion first."
            )

        if document.accession_number is None:
            raise ValueError("Document has no accession number.")

        path = download_filing(
            ticker=company.ticker,
            accession_number=document.accession_number,
            source_url=document.source_url,
        )

        print()
        print("Filing downloaded successfully.")
        print(f"Saved to: {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "ticker",
        help="Company ticker, e.g. NVDA, AMD or MSFT",
    )

    args = parser.parse_args()

    main(args.ticker)
