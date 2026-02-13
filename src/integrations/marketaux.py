import os
import requests
from typing import Any, Dict, List

BASE = "https://api.marketaux.com/v1"

def _token() -> str:
    t = os.getenv("MARKETAUX_API_TOKEN", "").strip()
    if not t:
        raise RuntimeError("MARKETAUX_API_TOKEN yok. .env veya environment variable set et.")
    return t

def _get(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    # Marketaux auth: api_token query param ([marketaux.com/documentation])
    params = {"api_token": _token(), **params}
    r = requests.get(f"{BASE}{path}", params=params, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"Marketaux HTTP {r.status_code}: {r.text}")
    return r.json()

def find_best_symbol(query: str, country: str = "us") -> str:
    q = query.strip().upper()

    # 1) direkt dene
    data = _get("/entity/search", {"search": q, "countries": country}).get("data", [])
    for it in data:
        if (it.get("symbol") or "").upper() == q:
            return it["symbol"]

    # 2) .US suffix varsa kırp
    if q.endswith(".US"):
        q2 = q[:-3]
        data2 = _get("/entity/search", {"search": q2, "countries": country}).get("data", [])
        for it in data2:
            if (it.get("symbol") or "").upper() == q2:
                return it["symbol"]
        if data2:
            return data2[0]["symbol"]

    # 3) fallback ilk sonuç
    if data:
        return data[0]["symbol"]

    raise ValueError(f"Entity bulunamadı: {query}")

def get_industry_for_symbol(symbol: str, country: str = "us") -> str:
    data = _get("/entity/search", {"search": symbol, "countries": country}).get("data", [])
    for it in data:
        if (it.get("symbol") or "").upper() == symbol.upper() and it.get("industry"):
            return it["industry"]
    if data and data[0].get("industry"):
        return data[0]["industry"]
    raise ValueError(f"Industry bulunamadı: {symbol}")

def _news_page(params: Dict[str, Any]) -> Dict[str, Any]:
    # news/all parametreleri: symbols, industries, limit, page, group_similar... ([marketaux.com/documentation])
    base = {
        "filter_entities": "true",
        "must_have_entities": "true",
        "group_similar": "false",
        "language": "en",
        "sort": "published_at",
    }
    base.update(params)
    return _get("/news/all", base)

def get_last_n_news(params_key: str, params_val: str, n: int = 10, per_req: int = 3) -> List[Dict[str, Any]]:
    collected: List[Dict[str, Any]] = []
    seen = set()
    page = 1

    while len(collected) < n:
        resp = _news_page({params_key: params_val, "limit": per_req, "page": page})
        items = resp.get("data", [])
        if not items:
            break

        for it in items:
            uid = it.get("uuid")
            if uid and uid in seen:
                continue
            if uid:
                seen.add(uid)
            collected.append(it)
            if len(collected) >= n:
                break

        meta = resp.get("meta", {})
        returned = meta.get("returned")
        limit = meta.get("limit")
        if returned is not None and limit is not None and returned < limit:
            break

        page += 1

    return collected[:n]

def get_ticker_and_industry_news(ticker_like: str, country: str = "us", n: int = 10, per_req: int = 3) -> Dict[str, Any]:
    symbol = find_best_symbol(ticker_like, country=country)
    industry = get_industry_for_symbol(symbol, country=country)
    ticker_news = get_last_n_news("symbols", symbol, n=n, per_req=per_req)
    industry_news = get_last_n_news("industries", industry, n=n, per_req=per_req)
    return {"symbol": symbol, "industry": industry, "ticker_news": ticker_news, "industry_news": industry_news}
