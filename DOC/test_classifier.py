from rag.vectordb import reset_collection, add_documents
from rag.classifier import classify_claim

# Limpa a coleção
reset_collection()

# Indexa documentos de exemplo
texts = [
    "O Banco Central anunciou queda na taxa de juros hoje.",
    "Cientistas brasileiros descobriram uma nova espécie de dinossauro.",
]
metas = [
    {"title": "Economia", "label": "VERDADEIRA", "source": "https://economia.exemplo"},
    {"title": "Ciência", "label": "VERDADEIRA", "source": "https://ciencia.exemplo"},
]
ids = ["doc-1", "doc-2"]
add_documents(texts, metas, ids)

claim = "O Banco Central reduziu a taxa Selic recentemente."
res = classify_claim(claim)

print(res)
