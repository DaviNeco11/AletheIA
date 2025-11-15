# rag/classifier.py
"""
Classificador de notícias usando RAG + LLM (Ollama).

Fluxo:
1) Usa o retriever para buscar contexto relevante no Chroma.
2) Monta um prompt estruturado com:
   - enunciado (claim)
   - contexto (evidências)
3) Chama o modelo de linguagem (llama3.1:8b) via Ollama.
4) Espera uma resposta ESTRITAMENTE em JSON:
   {
     "label": "VERDADEIRA" ou "FALSA",
     "confidence": 0.0 a 1.0,
     "rationale": "texto explicando",
     "used_sources": ["titulo | url | label", ...]
   }
"""

from __future__ import annotations

import os
import json
from typing import Dict, Any

import requests
from dotenv import load_dotenv

from rag.retriever import build_context, build_prompt_for_llm

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")

SYSTEM_PROMPT = """Você é um verificador de fatos especializado.
Você deve analisar o enunciado usando APENAS o contexto fornecido.
Responda ESTRITAMENTE no formato JSON com as chaves:
- "label": "VERDADEIRA" ou "FALSA"
- "confidence": número entre 0 e 1 (use no mínimo 0.5 e no máximo 0.99)
- "rationale": explicação breve em português (máx. 3 frases)
- "used_sources": lista de strings com "titulo | url | label" usadas como evidência

Regras:
- Se o contexto contradiz claramente o enunciado, use "FALSA".
- Se o contexto corrobora de forma consistente, use "VERDADEIRA".
- Se o contexto for insuficiente ou contraditório, escolha o lado mais suportado, mas reduza "confidence".
- Nunca invente fatos fora do contexto fornecido.
- NÃO inclua texto fora do JSON. NÃO inclua comentários. Apenas o objeto JSON.
"""


def _call_ollama_chat(prompt: str) -> str:
    """
    Faz uma chamada ao endpoint /api/chat do Ollama
    e retorna o conteúdo textual da resposta do modelo.
    """
    url = f"{OLLAMA_HOST}/api/chat"
    body = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.2,
        },
    }
    resp = requests.post(url, json=body, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    # Estrutura típica: {"message": {"role": "assistant", "content": "..."}}
    msg = data.get("message", {}) or {}
    content = msg.get("content", "")
    return content


def _parse_json_safely(text: str) -> Dict[str, Any]:
    """
    Tenta interpretar a resposta do modelo como JSON.
    Se vier texto extra, tenta extrair apenas o bloco JSON.
    """
    text = text.strip()
    # tentativa direta
    try:
        return json.loads(text)
    except Exception:
        pass

    # tentativa de extrair o primeiro bloco {...}
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        fragment = text[start : end + 1]
        try:
            return json.loads(fragment)
        except Exception:
            pass

    # fallback: retorna erro bruto
    return {
        "error": "Resposta do modelo não é um JSON válido.",
        "raw": text,
    }


def classify_claim(claim: str) -> Dict[str, Any]:
    """
    Classifica um enunciado (notícia) como VERDADEIRA ou FALSA usando RAG + LLM.

    Retorno esperado (ideal):
    {
      "label": "VERDADEIRA" ou "FALSA",
      "confidence": 0.85,
      "rationale": "explicação curta...",
      "used_sources": ["titulo | url | label", ...],
      "debug": { ... }  # info extra opcional
    }
    """
    # 1) monta contexto com os documentos mais relevantes
    ctx = build_context(claim)
    context_text = ctx["context"]
    sources = ctx["sources"]

    # 2) monta prompt amigável para o LLM
    user_prompt = build_prompt_for_llm(claim, context_text)

    # 3) chama o modelo via Ollama
    raw_response = _call_ollama_chat(user_prompt)

    # 4) tenta interpretar a resposta como JSON
    parsed = _parse_json_safely(raw_response)

    # 5) enriquece com info de debug (opcional)
    if isinstance(parsed, dict):
        parsed.setdefault("used_sources", sources)
        parsed.setdefault("debug", {})
        parsed["debug"].update(
            {
                "hits": ctx["hits"],
                "raw_sources": sources,
            }
        )
    return parsed
