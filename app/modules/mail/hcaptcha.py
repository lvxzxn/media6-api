import httpx
from app.core.config import settings

HCAPTCHA_VERIFY_URL = "https://hcaptcha.com/siteverify"

async def verify_hcaptcha(token: str, remoteip: str | None) -> bool:
    payload = {
        "secret": settings.hcaptcha_secret,
        "response": token,
    }

    if remoteip:
        payload["remoteip"] = remoteip

    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.post(HCAPTCHA_VERIFY_URL, data=payload)

    data = response.json()
    return data.get("success", False)