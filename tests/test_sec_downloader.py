from pathlib import Path
from unittest.mock import MagicMock, patch

from atlas.ingestion.sec_downloader import download_filing


@patch("atlas.ingestion.sec_downloader.save_raw_response")
@patch("atlas.ingestion.sec_downloader.SecClient")
def test_download_filing_saves_raw_response(
    mock_sec_client_class: MagicMock,
    mock_save_raw_response: MagicMock,
    tmp_path: Path,
) -> None:
    response = MagicMock()
    response.content = b"<html>test filing</html>"
    response.headers = {
        "content-type": "text/html",
    }

    client = MagicMock()
    client.get.return_value = response

    mock_sec_client_class.return_value.__enter__.return_value = client

    expected_path = tmp_path / "filing.html"

    mock_save_raw_response.return_value = expected_path

    source_url = "https://example.com/filing.htm"

    result = download_filing(
        ticker="NVDA",
        accession_number="0001045810-26-000001",
        source_url=source_url,
    )

    client.get.assert_called_once_with(source_url)

    mock_save_raw_response.assert_called_once_with(
        ticker="NVDA",
        filename="0001045810-26-000001.html",
        content=b"<html>test filing</html>",
        source_url=source_url,
    )

    assert result == expected_path
