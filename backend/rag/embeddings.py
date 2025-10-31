# rag/embeddings.py
import os
import requests
from dotenv import load_dotenv

#Carrega o env

load_dotenv()

#Variaveis de ambiente ENV
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Gera embeddings chamando o endpoint /api/embeddings do Ollama.
    Retorna uma lista de vetores (um por texto).
    """
    url = f"{OLLAMA_HOST}/api/embeddings"
    out: list[list[float]] = []
    for t in texts:
        resp = requests.post(url, json={"model": EMBED_MODEL, "prompt": t})
        resp.raise_for_status()
        data = resp.json()
        out.append(data["embedding"])
    return out

def embed_one(text: str) -> list[float]:
    return embed_texts([text])[0]
