import os
import subprocess
from datetime import datetime
from typing import Dict, Optional
import requests


def _log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def _get_env_var(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    value = os.environ.get(name, default)
    if required and value is None:
        raise ValueError(f"The {name} environment variable is required but not set.")
    return value


def _get_headers() -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    pat = _get_env_var("GANDI_PAT")
    api_key = _get_env_var("GANDI_API_KEY")
    if pat:
        headers["Authorization"] = f"Bearer {pat}"
    elif api_key:
        headers["Authorization"] = f"Apikey {api_key}"
    return headers


def notify(message: str, shoutrrr_urls: list) -> None:
    url_args = []
    for url in shoutrrr_urls:
        url_args += ["--url", url]
    try:
        env = os.environ.copy()
        env["SHOUTRRR_URL"] = shoutrrr_urls[0]
        result = subprocess.run(
            ["shoutrrr", "send"] + url_args + ["--message", message],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        if result.stdout:
            _log(f"Notification sent: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        _log(f"Failed to send notification: {e.stderr.strip()}")
    except FileNotFoundError:
        _log("shoutrrr binary not found, skipping notification")


def check_domains(domains: list, gandi_url: str, shoutrrr_urls: Optional[list]) -> None:
    url = f"{gandi_url.rstrip('/')}/domain/check"
    for domain in domains:
        try:
            response = requests.get(url, params={"name": domain}, headers=_get_headers())
            response.raise_for_status()
        except requests.HTTPError as e:
            _log(f"HTTP error while checking {domain}: {e}")
            continue
        except Exception as e:
            _log(f"Error while checking {domain}: {e}")
            continue

        grids = response.json()
        if isinstance(grids, dict):
            grids = [grids]
        if not grids:
            _log(f"{domain}: no availability data returned")
            continue

        for grid in grids:
            if not isinstance(grid, dict):
                _log(f"Unexpected API response for {domain}: {grid}")
                continue
            currency = grid.get("currency", "")
            for product in grid.get("products", []):
                name = product.get("name", domain)
                status = product.get("status", "unknown")
                if status == "available":
                    prices = product.get("prices", [])
                    price_info = ""
                    if prices:
                        p = prices[0]
                        price_info = f"\nPrix : {p.get('price_after_taxes', '?')} {currency}"
                    message = f"Le nom de domaine {name} est disponible chez Gandi.{price_info}"
                    _log(message)
                    if shoutrrr_urls:
                        notify(message, shoutrrr_urls)
                else:
                    _log(f"{name}: {status.upper()}")


if __name__ == "__main__":
    GANDI_URL = _get_env_var("GANDI_URL", "https://api.gandi.net/v5/")
    GANDI_DOMAINS = [d.strip() for d in (_get_env_var("GANDI_DOMAIN", required=True) or "").split(",") if d.strip()]
    SHOUTRRR_URLS = [
        u.strip().strip('\'"').strip()
        for u in (_get_env_var("SHOUTRRR_URL") or "").split(",")
        if u.strip().strip('\'"').strip()
    ] or None

    if SHOUTRRR_URLS:
        for u in SHOUTRRR_URLS:
            _log(f"Shoutrrr URL scheme: {u.split('://')[0]}://***")

    check_domains(GANDI_DOMAINS, GANDI_URL, SHOUTRRR_URLS)
