from langchain_community.document_loaders import PyPDFDirectoryLoader


def criar_db():
    #carregar documentos
    #gerar chunks
    #vetorizar chunks em embeddings
    documentos = carregar_documentos()
    chunks = dividir_chunks(documentos)
    vetorizar_chunks(chunks)

    def carregar_documentos
        carregador = PyPDFDirectoryLoader(Dataset, glob="*.pdf")
        documentos = carregador.load()