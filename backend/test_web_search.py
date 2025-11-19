# test_web_search.py
from rag.web_search import duckduckgo_search, format_web_results

query = "Banco Central reduz juros"
results = duckduckgo_search(query, max_results=3)

print("RESULTADOS BRUTOS:")
for r in results:
    print(r)

print("\nBLOCO FORMATADO:\n")
print(format_web_results(results))
