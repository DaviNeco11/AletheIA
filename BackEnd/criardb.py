from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

#Pegando somnte as falsas
PASTA_BASE = "Dataset/noticias_falsas"

def criar_db():
    #carregar documentos
    #gerar chunks
    #vetorizar chunks em embeddings
    documentos = carregar_documentos()
    chunks = dividir_chunks(documentos)
    vetorizar_chunks(chunks)

def carregar_documentos():
    carregador = PyPDFDirectoryLoader(PASTA_BASE, glob="*.pdf")
    documentos = carregador.load()
    return documentos

def dividir_chunks(documentos):
    separador_documentos = RecursiveCharacterTextSplitter(
        #depende do tamanho da resposta, possivelmente alterar
        chunk_size = 400,
        chunk_overlap = 200,
        length_function = len,
        add_start_index = True
    )
    chunks = separador_documentos.split_documents(documentos)
    print (len(chunks))
    return chunks

def vetorizar_chunks(chunks):
    pass
criar_db()