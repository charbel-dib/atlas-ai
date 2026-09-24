from dataclasses import dataclass
from datetime import date

SEC_SUBMISSIONS_BASE = "https://data.sec.gov/submissions"
SEC_ARCHIVES_BASE = "https://www.sec.gov/Archives/edgar/data"


@dataclass(frozen=True)
class SecFiling:
    cik: str
    form: str
    accession_number: str
    filing_date: date
    report_date: date | None
    primary_document: str

    @property
    def archive_url(self) -> str:
        cik_without_leading_zeros = str(int(self.cik))

        accession_without_dashes = self.accession_number.replace("-", "")

        return (
            f"{SEC_ARCHIVES_BASE}/"
            f"{cik_without_leading_zeros}/"
            f"{accession_without_dashes}/"
            f"{self.primary_document}"
        )


def submissions_url(cik: str) -> str:
    normalized_cik = cik.zfill(10)

    return f"{SEC_SUBMISSIONS_BASE}/CIK{normalized_cik}.json"


def _parse_optional_date(value: str) -> date | None:
    if not value:
        return None

    return date.fromisoformat(value)


def find_latest_filing(
    submissions: dict,
    cik: str,
    form_type: str,
) -> SecFiling:
    recent = submissions["filings"]["recent"]

    forms = recent["form"]

    for index, form in enumerate(forms):
        if form != form_type:
            continue

        return SecFiling(
            cik=cik,
            form=form,
            accession_number=recent["accessionNumber"][index],
            filing_date=date.fromisoformat(recent["filingDate"][index]),
            report_date=_parse_optional_date(recent["reportDate"][index]),
            primary_document=recent["primaryDocument"][index],
        )

    raise ValueError(f"No recent filing found for form {form_type}.")
