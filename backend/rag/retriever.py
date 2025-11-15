# rag/retriever.py
"""
Retriever do RAG:
- Consulta o banco vetorial (Chroma) pelos documentos mais similares ao texto de entrada
- Organiza os resultados em um 'contexto' legível para ser usado pelo LLM
- Retorna também uma lista de fontes e um payload bruto para depuração
"""

from __future__ import annotations
import os
import math
from typing import Dict, Any, List, Tuple
from dotenv import load_dotenv

from rag.vectordb import query_similar

load_dotenv()

DEFAULT_TOP_K = int(os.getenv("TOP_K", "6"))
# limite de caracteres por trecho (evita contexto enorme)
SNIPPET_MAX_CHARS = int(os.getenv("RAG_SNIPPET_MAX", "800"))
# limite total de caracteres do contexto concatenado
CONTEXT_MAX_CHARS = int(os.getenv("RAG_CONTEXT_MAX", "6000"))


def _truncate_txt(txt: str, max_chars: int) -> str:
    """Corta um texto em no máximo max_chars, preservando fim limpo."""
    if not txt or len(txt) <= max_chars:
        return txt or ""
    cut = txt[: max_chars].rstrip()
    # tenta não cortar no meio da palavra
    last_space = cut.rfind(" ")
    if last_space > 0 and max_chars - last_space < 40:
        cut = cut[:last_space]
    return cut + "..."


def _unique_sources(metadatas: List[dict]) -> List[str]:
    """Extrai fontes únicas (title + source) preservando ordem."""
    seen = set()
    out: List[str] = []
    for m in metadatas:
        title = (m or {}).get("title", "").strip()
        src = (m or {}).get("source", "").strip()
        label = (m or {}).get("label", "").strip()
        tag = f"{title} | {src} | {label}"
        if tag and tag not in seen:
            seen.add(tag)
            out.append(tag)
    return out


def _format_block(doc: str, meta: dict, rank: int, distance: float | None) -> str:
    """Formata um bloco de contexto com título, fonte e trecho."""
    title = (meta or {}).get("title", "").strip() or f"Documento {rank}"
    source = (meta or {}).get("source", "").strip()
    label = (meta or {}).get("label", "").strip()
    head = f"[{rank}] {title}"
    if label:
        head += f" (label={label})"
    if source:
        head += f"\nFonte: {source}"
    if distance is not None and not math.isnan(distance):
        head += f"\nSimilaridade: {1 - float(distance):.3f}"
    body = _truncate_txt(doc or "", SNIPPET_MAX_CHARS)
    return f"{head}\nTrecho: {body}"


def build_context(
    query: str,
    top_k: int | None = None,
    include_distances: bool = True,
) -> Dict[str, Any]:
    """
    Executa a busca semântica e monta o contexto RAG.

    Retorna:
    {
      "context": "<texto pronto para o LLM>",
      "hits": <int>,
      "sources": ["Titulo | url | label", ...],
      "raw": {  # resposta bruta do Chroma para debug
         "documents": [...],
         "metadatas": [...],
         "distances": [...]
      }
    }
    """
    k = int(top_k or DEFAULT_TOP_K)
    res = query_similar(
        query_text=query,
        top_k=k,
        include_distances=include_distances,
    )

    docs: List[str] = (res.get("documents") or [[]])[0]
    metas: List[dict] = (res.get("metadatas") or [[]])[0]
    dists: List[float] = (res.get("distances") or [[]])[0] if include_distances else [None] * len(docs)

    blocks: List[str] = []
    used_chars = 0
    for i, (d, m, dist) in enumerate(zip(docs, metas, dists), start=1):
        block = _format_block(d, m, rank=i, distance=dist if include_distances else None)
        if used_chars + len(block) > CONTEXT_MAX_CHARS and blocks:
            break
        blocks.append(block)
        used_chars += len(block)

    context = "\n\n---\n\n".join(blocks)
    sources = _unique_sources(metas)

    return {
        "context": context,
        "hits": len(blocks),
        "sources": sources,
        "raw": {
            "documents": docs,
            "metadatas": metas,
            "distances": dists if include_distances else [],
        },
    }


def build_prompt_for_llm(claim: str, ctx: str) -> str:
    """
    Monta um prompt amigável para LLM usando o contexto já formatado.
    (Útil se você quiser testar rapidamente numa chamada ao LLM.)
    """
    return (
        "Você é um verificador de fatos. Use APENAS as evidências abaixo para avaliar o enunciado.\n\n"
        "Enunciado a avaliar:\n"
        f"```\n{claim}\n```\n\n"
        "Evidências (contexto recuperado):\n"
        f"{ctx}\n\n"
        "Instruções:\n"
        "1) Se as evidências contradizem, responda FALSA.\n"
        "2) Se corroboram consistentemente, responda VERDADEIRA.\n"
        "3) Se o material for insuficiente, indique incerteza e reduza a confiança.\n"
    )
