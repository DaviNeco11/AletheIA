# rag/classifier_web.py
from __future__ import annotations
import os, json, requests
from typing import Dict, Any

from dotenv import load_dotenv
from rag.retriever import build_context, build_prompt_for_llm
from rag.web_search import duckduckgo_search, format_web_results

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")

SYSTEM_PROMPT = """Você é um verificador de fatos. Use APENAS as evidências fornecidas acima.
Responda SOMENTE em JSON com:
- label
- confidence
- rationale
- used_sources
"""

def _call_ollama_chat(prompt: str) -> str:
    url = f"{OLLAMA_HOST}/api/chat"
    body = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": {"temperature": 0.2},
    }
    resp = requests.post(url, json=body, timeout=120)
    resp.raise_for_status()
    return resp.json()["message"]["content"]

def _parse_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except:
        s, e = text.find("{"), text.rfind("}")
        if s != -1 and e != -1:
            try:
                return json.loads(text[s:e+1])
            except:
                pass
    return {"error": "JSON inválido", "raw": text}

def classify_claim_with_web(claim: str, max_web_results: int = 5) -> Dict[str, Any]:
    ctx = build_context(claim)
    local_context = ctx["context"]
    web_results = duckduckgo_search(claim, max_results=max_web_results)
    web_block = format_web_results(web_results)

    full_context = local_context + "\n\n" + web_block
    prompt = build_prompt_for_llm(claim, full_context)

    raw = _call_ollama_chat(prompt)
    parsed = _parse_json(raw)

    parsed.setdefault("used_sources", ctx["sources"])
    parsed.setdefault("web_results", web_results)
    parsed.setdefault("debug", {"hits": ctx["hits"]})

    return parsed
