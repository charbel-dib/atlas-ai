from pathlib import Path

from atlas.ingestion.raw_store import save_raw_response
from atlas.ingestion.sec_client import SecClient


def download_filing(
    ticker: str,
    accession_number: str,
    source_url: str,
) -> Path:
    filename = f"{accession_number}.html"

    print(f"Downloading filing: {source_url}")

    with SecClient() as client:
        response = client.get(source_url)

    content_type = response.headers.get(
        "content-type",
        "",
    )

    print(f"Received {len(response.content):,} bytes with content type: {content_type}")

    path = save_raw_response(
        ticker=ticker,
        filename=filename,
        content=response.content,
        source_url=source_url,
    )

    return path
