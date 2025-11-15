# ingest.py
"""
Script de ingestão:
- Lê um CSV com notícias/itens rotulados
- Gera embeddings via Ollama
- Indexa tudo no ChromaDB (coleção 'news' por padrão)
"""

import os

import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

from rag.vectordb import add_documents, reset_collection

load_dotenv()

CSV_PATH = os.getenv("SEED_CSV_PATH", "data/seed.csv")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "news")


def load_seed_csv(path: str) -> pd.DataFrame:
    """
    Carrega o CSV de seed e faz uma validação básica.
    Espera pelo menos a coluna 'text'.
    Opcionalmente: title, label, source.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {path}")

    df = pd.read_csv(path)
    if "text" not in df.columns:
        raise ValueError("O CSV precisa ter pelo menos a coluna 'text'.")

    # garante colunas opcionais
    for col in ["title", "label", "source"]:
        if col not in df.columns:
            df[col] = ""

    # remove linhas sem texto
    df = df.dropna(subset=["text"]).reset_index(drop=True)
    return df


def ingest():
    print(f"Carregando dataset de: {CSV_PATH}")
    df = load_seed_csv(CSV_PATH)
    print(f"Total de linhas: {len(df)}")

    # opcional: limpar coleção antes de reindexar
    print(f"Limpando coleção '{COLLECTION_NAME}'...")
    reset_collection(COLLECTION_NAME)

    texts = []
    metadatas = []
    ids = []

    print("Preparando documentos para indexação...")
    for i, row in tqdm(df.iterrows(), total=len(df)):
        text = str(row["text"]).strip()
        if not text:
            continue

        texts.append(text)
        metadatas.append(
            {
                "title": str(row.get("title", "")) if not pd.isna(row.get("title", "")) else "",
                "label": str(row.get("label", "")) if not pd.isna(row.get("label", "")) else "",
                "source": str(row.get("source", "")) if not pd.isna(row.get("source", "")) else "",
            }
        )
        ids.append(f"doc-{i}")

    print(f"Indexando {len(texts)} documentos no Chroma...")
    add_documents(texts=texts, metadatas=metadatas, ids=ids, coll_name=COLLECTION_NAME)

    print("✅ Ingestão concluída com sucesso.")


if __name__ == "__main__":
    ingest()
