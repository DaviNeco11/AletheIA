import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import ollama  # 1. Importa a biblioteca do Ollama
import json    # 2. Importa a biblioteca JSON para processar a resposta

# --- Modelo de Dados (sem mudança) ---
class NewsItem(BaseModel):
    text: str

# --- App FastAPI e CORS (sem mudança) ---
app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. PROMPT DO SISTEMA ---
# Esta é a instrução principal para o LLM.
# Pedir para ele responder APENAS com JSON é a parte mais importante.
SYSTEM_PROMPT = """
Você é um assistente de checagem de fatos especializado em política. 
Sua tarefa é analisar o texto da notícia fornecido e determinar sua provável veracidade.

Responda APENAS com um objeto JSON com o seguinte formato:
{
  "veracidade": "FATO" ou "FALSO" ou "INCONCLUSIVO",
  "score": um número de 0.0 (totalmente falso) a 1.0 (totalmente fato),
  "analise": "Uma breve explicação (em uma frase) da sua conclusão."
}
"""

# --- Endpoints da API ---

@app.get("/")
async def root():
    return {"message": "AletheIA Backend está rodando!"}


@app.post("/api/verify")
async def verify_news(item: NewsItem):
    """
    Endpoint principal que agora chama o OLLAMA.
    """
    
    try:
        # 4. Prepara as mensagens para o LLM
        messages = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': item.text}
        ]
        
        # 5. Chama o Ollama
        # Usamos o modelo que você baixou e o 'format='json'' para forçar a saída
        response = ollama.chat(
            model='gemma3:1b',
            messages=messages,
            format='json'  # Garante que a resposta seja uma string JSON válida
        )

        # 6. Processa a resposta
        # A resposta do Ollama é um dicionário, e o conteúdo que queremos é uma string JSON.
        response_content_string = response['message']['content']
        
        # Imprime no terminal do backend para você ver
        print(f"Resposta bruta do Ollama (string): {response_content_string}") 
        
        # Converte a string JSON em um dicionário Python
        json_response = json.loads(response_content_string)
        
        # 7. Retorna o dicionário para o frontend
        return json_response

    except json.JSONDecodeError as e:
        # Erro se o LLM não retornar um JSON válido
        print(f"Erro ao decodificar JSON do LLM: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar a resposta do LLM.")
    except Exception as e:
        # Captura outros erros (ex: Ollama não está rodando)
        print(f"Erro ao chamar Ollama: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# --- Ponto de Entrada (sem mudança) ---
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)