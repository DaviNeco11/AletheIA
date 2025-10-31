## AletheIA: Assistente de Detecção de Fake News com IA


1. Visão Geral
    O AletheIA é um assistente inteligente projetado para combater a desinformação no cenário político brasileiro. Utilizando um Modelo de Linguagem de Grande Porte (LLM) de última geração e a arquitetura de         Geração Aumentada por Recuperação (RAG), nossa ferramenta analisa uma notícia fornecida pelo usuário e retorna um score de probabilidade de ser falsa, acompanhado de uma justificativa detalhada.

    O objetivo é fornecer ao usuário uma ferramenta poderosa e transparente para a verificação de fatos, ajudando a mitigar o impacto negativo da disseminação de notícias falsas.

2. O Problema
    A rápida disseminação de notícias falsas, especialmente através de redes sociais, representa uma ameaça significativa para a sociedade, influenciando a opinião pública e a estabilidade política. O contexto político brasileiro, em particular, é um dos principais alvos desse tipo de desinformação.
    
    A verificação manual de notícias é um processo complexo, caro e demorado, incapaz de acompanhar o enorme volume de conteúdo gerado diariamente. Embora soluções de aprendizado de máquina existam, muitas dependem de modelos proprietários e pagos, e poucas foram empiricamente validadas para as nuances do cenário brasileiro.

3. Nossa Solução: RAG + Gemma 3
    Para resolver esse desafio, implementamos uma solução que combina duas tecnologias de ponta:
    
    a) Geração Aumentada por Recuperação (RAG):
    Em vez de depender apenas do conhecimento interno do modelo, nosso sistema primeiro busca informações relevantes em uma base de conhecimento confiável. Essa base é composta por notícias verificadas de fontes jornalísticas respeitadas (G1, UOL, etc.) e dados de agências de checagem. Isso permite que nossa análise seja baseada em fatos atuais e verificados, tornando o sistema mais preciso e menos propenso a "alucinações".
    
    b) Modelo Google Gemma 3:
    O núcleo do nosso assistente é o Gemma 3, um LLM de código aberto do Google. A escolha foi baseada em um estudo empírico que comparou sete diferentes LLMs para a detecção de fake news políticas no Brasil. Os resultados foram claros:
    
    - Desempenho Superior: O Gemma 3 superou todos os outros modelos, incluindo o GPT-4, apresentando o maior F1-score (0.90) na tarefa.
    
    - Excelente Explicabilidade: O modelo demonstrou uma capacidade notável de gerar justificativas claras e coerentes, identificando características de desinformação (como sensacionalismo e falta de fontes) e de veracidade (detalhes específicos e fontes confiáveis).
    
    - Vantagem Open-Source: Sendo um modelo de código aberto, o Gemma 3 nos dá flexibilidade, controle e elimina a dependência de APIs pagas.

4. Como Funciona

    - O fluxo de trabalho do assistente é simples e transparente:
    
    - Entrada do Usuário: O usuário insere o texto de uma notícia que deseja verificar.
    
    - Recuperação de Contexto (RAG): O sistema converte a notícia em um vetor e busca em nossa base de dados por notícias e fatos similares de fontes confiáveis.
    
    - Análise Aumentada: A notícia original, juntamente com o contexto recuperado, é enviada ao Gemma 3 através de um prompt estruturado. O prompt instrui o modelo a atuar como um checador de fatos e cruzar as informações.
    
    - Geração da Resposta: O Gemma 3 analisa o material e gera uma resposta contendo:
    
        - Uma classificação final: "fake" ou "real".
    
        - Uma justificativa em tópicos, explicando os motivos da classificação.
  
        - Saída Final: O sistema processa a resposta do modelo e apresenta ao usuário:
    
        - Um score de probabilidade (ex: 95% de chance de ser fake).
    
        - A justificativa gerada pela IA.

5. Arquitetura Técnica
    - Modelo de Linguagem: Google Gemma 3 (executado via Ollama).

    - Arquitetura de Análise: RAG (Retrieval-Augmented Generation).

    - Base de Conhecimento: Banco de dados vetorial (ex: ChromaDB, FAISS) populado com notícias de fontes confiáveis.

    - Backend: Python (usando bibliotecas como LangChain ou LlamaIndex para orquestrar o fluxo RAG).

    - Frontend: Vue.js.

--------------

#### Como rodar localmente:

- Front-end:

    - Necessário npm;
 
    - No diretório do projeto, rode:
        - cd frontend;
        - npm install;
        - npm install vue-feather-icons
        - npm run format
        - npm run dev
    - Acesse no navegador com a URL: http://localhost:5173/
          
        
