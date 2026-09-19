from typing import Any

import httpx


async def get_json(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 8.0,
) -> Any:
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(timeout),
        follow_redirects=True,
        headers=headers,
    ) as client:
        response = await client.get(url, params=params)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise httpx.HTTPStatusError(
                f"HTTP {exc.response.status_code}: "
                f"{exc.response.text[:200]}",
                request=exc.request,
                response=exc.response,
            ) from exc

        return response.json()