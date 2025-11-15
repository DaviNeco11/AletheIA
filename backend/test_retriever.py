from rag.vectordb import reset_collection, add_documents
from rag.retriever import build_context

# 1) zera a coleção (opcional, mas recomendado para teste)
reset_collection()

# 2) insere alguns documentos fictícios
texts = [
    "O Banco Central anunciou queda na taxa de juros hoje.",
    "Cientistas brasileiros descobriram uma nova espécie de dinossauro.",
    "O time venceu o campeonato nacional após vencer na prorrogação.",
]

metas = [
    {"title": "Economia", "label": "VERDADEIRA", "source": "https://economia.exemplo"},
    {"title": "Ciência", "label": "VERDADEIRA", "source": "https://ciencia.exemplo"},
    {"title": "Esportes", "label": "VERDADEIRA", "source": "https://esportes.exemplo"},
]

ids = ["doc-1", "doc-2", "doc-3"]

print("Indexando documentos...")
add_documents(texts, metas, ids)

# 3) testando o retriever com uma consulta
query = "A taxa Selic foi reduzida recentemente pelo Banco Central"
ctx = build_context(query, top_k=2)

print("\n===== CONTEXTO FINAL DO RAG =====\n")
print(ctx["context"])

print("\n===== FONTE USADAS =====\n")
print(ctx["sources"])

print("\n===== HITS (quantidade de trechos recuperados) =====\n")
print(ctx["hits"])

print("\n===== RAW (retorno bruto para debug) =====\n")
print(ctx["raw"])
