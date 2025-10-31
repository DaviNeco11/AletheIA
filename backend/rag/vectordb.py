# rag/vectordb.py
"""
Camada de persistência vetorial usando ChromaDB.
- Cria/recupera a coleção persistida em disco
- Indexa documentos com embeddings vindos do Ollama (rag/embeddings.py)
- Faz busca por similaridade e retorna textos + metadados + distâncias
"""

from __future__ import annotations
import os
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings

from rag.embeddings import embed_texts, embed_one

load_dotenv()

# Diretório onde o Chroma grava os arquivos do índice
CHROMA_DIR = os.getenv("CHROMA_DIR", "./db")
# Nome padrão da coleção
DEFAULT_COLLECTION = "news"


def get_client() -> chromadb.Client:
    """
    Cria um cliente Chroma com persistência em disco.
    """
    return chromadb.Client(
        Settings(
            persist_directory=CHROMA_DIR,
            anonymized_telemetry=False,  # evita enviar métricas
        )
    )


def get_collection(name: str = DEFAULT_COLLECTION):
    """
    Obtém (ou cria) uma coleção persistida.
    Importante: usamos embeddings MANUAIS (embedding_function=None),
    porque geramos os vetores com o Ollama (rag/embeddings.py).
    """
    client = get_client()
    return client.get_or_create_collection(
        name=name,
        embedding_function=None,  # vamos passar embeddings prontos
        metadata={"hnsw:space": "cosine"},  # métrica de similaridade
    )


def add_documents(
    texts: List[str],
    metadatas: List[Dict[str, Any]],
    ids: List[str],
    coll_name: str = DEFAULT_COLLECTION,
) -> None:
    """
    Indexa uma lista de documentos:
    - Gera embeddings via Ollama
    - Salva docs + metadados + vetores na coleção

    Observações:
    - IDs devem ser ÚNICOS. Se repetir, o Chroma lança erro.
    - Se quiser sobrescrever, primeiro delete pelos IDs e depois adicione.
    """
    if not (len(texts) == len(metadatas) == len(ids)):
        raise ValueError("texts, metadatas e ids precisam ter o mesmo tamanho.")

    col = get_collection(coll_name)
    vectors = embed_texts(texts)  # gera embeddings no Ollama
    col.add(documents=texts, metadatas=metadatas, ids=ids, embeddings=vectors)


def query_similar(
    query_text: str,
    top_k: int = 6,
    coll_name: str = DEFAULT_COLLECTION,
    include_distances: bool = True,
) -> Dict[str, Any]:
    """
    Busca por similaridade:
    - Gera embedding do 'query_text'
    - Retorna os top_k documentos mais próximos.
    """
    col = get_collection(coll_name)
    qvec = embed_one(query_text)

    res = col.query(
        query_embeddings=[qvec],
        n_results=top_k,
        include=["documents", "metadatas", "distances"] if include_distances else ["documents", "metadatas"],
    )
    # Normaliza ausência de resultados
    res.setdefault("documents", [[]])
    res.setdefault("metadatas", [[]])
    if include_distances:
        res.setdefault("distances", [[]])
    return res


def delete_by_ids(ids: List[str], coll_name: str = DEFAULT_COLLECTION) -> None:
    """
    Remove documentos específicos pelos seus IDs.
    Útil quando for reindexar algum item.
    """
    if not ids:
        return
    col = get_collection(coll_name)
    col.delete(ids=ids)


def reset_collection(coll_name: str = DEFAULT_COLLECTION) -> None:
    """
    Limpa completamente a coleção (apaga todos os itens).
    Use com cuidado.
    """
    client = get_client()
    try:
        client.delete_collection(coll_name)
    except Exception:
        # Se não existir, ignora
        pass
    # recria vazia
    client.get_or_create_collection(name=coll_name, embedding_function=None, metadata={"hnsw:space": "cosine"})
