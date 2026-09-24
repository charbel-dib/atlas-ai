from atlas.db.models import Company


def test_company_model() -> None:
    company = Company(
        name="NVIDIA Corporation",
        ticker="NVDA",
        cik="0001045810",
    )

    assert company.name == "NVIDIA Corporation"
    assert company.ticker == "NVDA"
    assert company.cik == "0001045810"
