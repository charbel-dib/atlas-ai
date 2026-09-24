import time
from typing import Self

import httpx

from atlas.core.config import settings

RETRYABLE_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}


class SecClient:
    def __init__(
        self,
        timeout_seconds: float = 20.0,
        max_attempts: int = 4,
    ) -> None:
        self.max_attempts = max_attempts

        self.client = httpx.Client(
            headers={
                "User-Agent": settings.sec_user_agent,
                "Accept-Encoding": "gzip, deflate",
            },
            timeout=timeout_seconds,
            follow_redirects=True,
        )

    def get(self, url: str) -> httpx.Response:
        for attempt in range(1, self.max_attempts + 1):
            try:
                response = self.client.get(url)

                if response.status_code in RETRYABLE_STATUS_CODES and attempt < self.max_attempts:
                    wait_seconds = 2 ** (attempt - 1)

                    print(f"SEC returned {response.status_code}. Retrying in {wait_seconds}s.")

                    time.sleep(wait_seconds)
                    continue

                response.raise_for_status()

                # Be deliberately conservative with SEC traffic.
                time.sleep(0.2)

                return response

            except httpx.RequestError:
                if attempt == self.max_attempts:
                    raise

                wait_seconds = 2 ** (attempt - 1)

                print(f"Network error. Retrying in {wait_seconds}s.")

                time.sleep(wait_seconds)

        raise RuntimeError("SEC request failed unexpectedly.")

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
