# app.py
"""
CLI para classificar notícias usando RAG local + (opcional) DuckDuckGo.

Uso:
  - Texto direto:
      python app.py --text "O Banco Central reduziu a taxa Selic recentemente."

  - URL de notícia:
      python app.py --url "https://exemplo.com/noticia"

  - Desativar busca na web (usar só RAG local):
      python app.py --text "..." --no-web
"""

import argparse
import sys
from typing import Optional

import requests
from bs4 import BeautifulSoup

from rag.classifier import classify_claim
from rag.classifier_web import classify_claim_with_web


def extract_text_from_url(url: str, max_chars: int = 8000) -> str:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()

    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    text = "\n".join(paragraphs).strip()

    if not text:
        raise RuntimeError("Não foi possível extrair texto útil da página.")

    return text[:max_chars]


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classificador de notícias (RAG + Ollama + DuckDuckGo).")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Texto da notícia a ser verificada.")
    group.add_argument("--url", type=str, help="URL da notícia a ser baixada e verificada.")
    parser.add_argument(
        "--no-web",
        action="store_true",
        help="Não usar DuckDuckGo (usa apenas o contexto local do Chroma).",
    )
    parser.add_argument(
        "--max-web-results",
        type=int,
        default=5,
        help="Máximo de resultados da web via DuckDuckGo (padrão: 5).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    args = parse_args(argv)

    if args.url:
        print(f"🔗 Baixando conteúdo de: {args.url}")
        claim = extract_text_from_url(args.url)
    else:
        claim = args.text

    use_web = not args.no_web

    print("\n🧠 Classificando enunciado...\n")

    if use_web:
        result = classify_claim_with_web(claim, max_web_results=args.max_web_results)
    else:
        result = classify_claim(claim)

    if "error" in result:
        print("❌ Erro ao classificar:")
        print(result["error"])
        print("Resposta bruta:")
        print(result.get("raw", ""))
        return

    label = result.get("label", "DESCONHECIDO")
    confidence = result.get("confidence", 0.0)
    rationale = result.get("rationale", "")
    used_sources = result.get("used_sources", [])
    debug = result.get("debug", {})
    hits = debug.get("hits")
    web_results = result.get("web_results", [])

    print(f"Resultado: {label}")
    print(f"Confiança: {confidence:.2f}")
    print(f"Justificativa: {rationale}\n")

    if used_sources:
        print("Fontes locais usadas (Chroma):")
        for s in used_sources:
            print(f"- {s}")

    if use_web and web_results:
        print("\nFontes da web (DuckDuckGo):")
        for i, r in enumerate(web_results, start=1):
            print(f"[W{i}] {r.get('title','')}\nURL: {r.get('url','')}\nTrecho: {r.get('snippet','')}\n")

    if hits is not None:
        print(f"\nTrechos recuperados pelo RAG local: {hits}")


if __name__ == "__main__":
    main(sys.argv[1:])
