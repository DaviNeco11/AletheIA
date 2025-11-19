# evaluate.py
"""
Avaliação do classificador em lote usando o CSV de seed.

Fluxo:
1) Lê data/seed.csv (ou outro caminho configurado via SEED_CSV_PATH no .env)
2) Para cada linha, chama classify_claim(text)
3) Compara o rótulo previsto com o rótulo real (coluna 'label')
4) Imprime métricas (precision, recall, f1) por classe e no geral
"""

import os
import time

import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from sklearn.metrics import classification_report, confusion_matrix

from rag.classifier import classify_claim

load_dotenv()

CSV_PATH = os.getenv("SEED_CSV_PATH", "data/seed.csv")

# mapeamento opcional para normalizar labels
# (ajuste aqui se seu CSV usa "True"/"False", "real"/"fake", etc.)
NORMALIZE = {
    "VERDADEIRA": "VERDADEIRA",
    "V": "VERDADEIRA",
    "TRUE": "VERDADEIRA",
    "T": "VERDADEIRA",
    "FALSA": "FALSA",
    "F": "FALSA",
    "FALSE": "FALSA",
}


def normalize_label(x: str) -> str:
    if not isinstance(x, str):
        return "FALSA"
    x = x.strip().upper()
    return NORMALIZE.get(x, x)


def main():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("O CSV precisa ter as colunas 'text' e 'label'.")

    # limpa e normaliza
    df = df.dropna(subset=["text", "label"]).reset_index(drop=True)
    df["label"] = df["label"].apply(normalize_label)

    print(f"Total de amostras para avaliação: {len(df)}")
    print("Iniciando avaliação...\n")

    y_true = []
    y_pred = []

    start = time.time()

    for _, row in tqdm(df.iterrows(), total=len(df)):
        text = str(row["text"])
        true_label = row["label"]

        try:
            out = classify_claim(text)
            pred_label = out.get("label", "FALSA")
            pred_label = normalize_label(pred_label)
        except Exception as e:
            print(f"\n⚠️ Erro ao classificar uma amostra: {e}")
            pred_label = "FALSA"

        y_true.append(true_label)
        y_pred.append(pred_label)

    elapsed = time.time() - start

    print("\n===== RELATÓRIO DE CLASSIFICAÇÃO =====\n")
    print(classification_report(y_true, y_pred, digits=3))

    print("===== MATRIZ DE CONFUSÃO =====\n")
    print(confusion_matrix(y_true, y_pred, labels=["VERDADEIRA", "FALSA"]))
    print("\nLinhas/colunas na ordem: ['VERDADEIRA', 'FALSA']")

    print(f"\nTempo total: {elapsed:.1f} segundos")
    if len(df) > 0:
        print(f"Tempo médio por amostra: {elapsed / len(df):.2f} s")


if __name__ == "__main__":
    main()
