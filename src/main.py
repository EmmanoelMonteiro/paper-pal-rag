# main.py

from src.data.document_loader import DocumentLoader
from src.data.document_parser import DocumentParser
from src.infrastructure.vector_store_impl import ChromaDocumentRepository
from src.infrastructure.llm_connector import LLMConnector
from src.domain.rag_service import RAGService
from src.presentation.cli_chatbot import CLIChatbot
from src.core.config import ARTICLES_DIR, CHROMA_DB_DIR # Importar os diretórios do config

def main():
    """
    Função principal que inicializa e executa o chatbot Paper-Pal-RAG.
    """
    # 1. Inicializa os componentes da camada de Infraestrutura
    print("Inicializando componentes de infraestrutura...")
    llm_connector = LLMConnector()
    document_repo = ChromaDocumentRepository() # Tenta carregar o DB existente aqui

    # 2. Inicializa os componentes da camada de Dados
    print("Inicializando componentes de dados...")
    document_loader = DocumentLoader()
    document_parser = DocumentParser()

    # 3. Inicializa o Serviço de Domínio (Lógica de Negócio)
    print("Inicializando serviço RAG...")
    rag_service = RAGService(
        document_loader=document_loader,
        document_parser=document_parser,
        document_repo=document_repo,
        llm_connector=llm_connector
    )

    # 4. Inicializa e executa a Interface de Usuário
    print("Iniciando interface do chatbot...")
    chatbot = CLIChatbot(rag_service=rag_service)
    chatbot.run()

if __name__ == "__main__":
    main()