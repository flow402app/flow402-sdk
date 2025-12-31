import httpx
from fastapi import Request, Response
from typing import Optional
import os

class Flow402Reporter:
    """
    FastAPI middleware that automatically reports successful x402 payments to Flow402 dashboard.
    Usage:
        app.add_middleware(Flow402Reporter, api_key="fk_...")
    """
    def __init__(self, app, api_key: str, backend_url: str = None):
        self.app = app
        self.api_key = api_key or os.getenv("FLOW402_API_KEY")
        self.backend_url = backend_url or "https://flow402-backend.onrender.com"  # Twój URL!

        if not self.api_key:
            raise ValueError("Flow402 API key required")

        app.middleware("http")(self.middleware)

    async def middleware(self, request: Request, call_next):
        response: Response = await call_next(request)

        # Tylko raportuj udane requesty (200-299)
        if 200 <= response.status_code < 300:
            # Tutaj w przyszłości możemy automatycznie wyciągać dane z nagłówków x402
            # Na MVP użytkownik sam woła report_event ręcznie lub podaje dane
            pass

        return response

    async def report_event(
        self,
        endpoint: str,
        payer_wallet: str,
        amount_usd: float,
        tx_hash: Optional[str] = None,
        event_type: str = "revenue"
    ):
        """Manual report – user calls this after successful x402 verification"""
        payload = {
            "endpoint": endpoint,
            "payer_wallet": payer_wallet,
            "amount_usd": amount_usd,
            "tx_hash": tx_hash,
            "event_type": event_type
        }

        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    f"{self.backend_url}/webhook/event",
                    json=payload,
                    headers={"X-API-Key": self.api_key},
                    timeout=5.0
                )
            except Exception:
                pass  # fail silently – nie blokujemy API użytkownika
