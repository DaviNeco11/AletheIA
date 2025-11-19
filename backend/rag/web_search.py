# rag/web_search.py
from __future__ import annotations
from typing import List, Dict
from ddgs import DDGS


def duckduckgo_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            title = r.get("title") or ""
            url = r.get("link") or r.get("href") or ""
            snippet = r.get("body") or ""
            if title and url:
                results.append({
                    "title": title.strip(),
                    "url": url.strip(),
                    "snippet": snippet.strip(),
                })
    return results


def format_web_results(results: List[Dict[str, str]]) -> str:
    if not results:
        return "Nenhuma evidência encontrada via DuckDuckGo.\n"

    out = ["Resultados da web (DuckDuckGo):"]
    for i, r in enumerate(results, start=1):
        out.append(
            f"[W{i}] {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Trecho: {r['snippet']}\n"
        )
    return "\n".join(out)
