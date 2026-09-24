import json
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

RAW_SEC_ROOT = Path("data/raw/sec")


def save_raw_response(
    ticker: str,
    filename: str,
    content: bytes,
    source_url: str,
) -> Path:
    company_dir = RAW_SEC_ROOT / ticker.upper()

    company_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    data_path = company_dir / filename

    data_path.write_bytes(content)

    metadata = {
        "source_url": source_url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "sha256": sha256(content).hexdigest(),
        "size_bytes": len(content),
    }

    metadata_path = company_dir / f"{filename}.meta.json"

    metadata_path.write_text(
        json.dumps(
            metadata,
            indent=2,
        ),
        encoding="utf-8",
    )

    return data_path
