# src/presentation/cli_chatbot.py

from src.domain.rag_service import RAGService
from src.core.exceptions import LLMGenerationError
import os
from src.core.config import ARTICLES_DIR # Importa o diretório dos artigos

class CLIChatbot:
    """
    Interface de chatbot de linha de comando para o Paper-Pal-RAG.
    """

    def __init__(self, rag_service: RAGService):
        """
        Inicializa o CLIChatbot.

        Args:
            rag_service (RAGService): O serviço RAG que lida com a lógica de negócio.
        """
        self.rag_service = rag_service
        self._check_articles_directory() # Verifica se a pasta de artigos existe

    def _check_articles_directory(self):
        """Verifica se o diretório de artigos existe e o cria se não."""
        if not os.path.exists(ARTICLES_DIR):
            os.makedirs(ARTICLES_DIR)
            print(f"Diretório de artigos '{ARTICLES_DIR}' criado. Por favor, adicione seus PDFs e TXTs aqui.")

    def run(self):
        """
        Inicia o loop principal do chatbot, permitindo a interação com o usuário.
        """
        print("-" * 50)
        print("Bem-vindo ao Paper-Pal-RAG!")
        print("Seu assistente para artigos científicos.")
        print("Comandos disponíveis:")
        print("  - 'ingest' para carregar novos documentos na base de conhecimento.")
        print("  - 'clear' para remover todos os documentos da base de conhecimento.")
        print("  - 'exit' ou 'quit' para sair.")
        print("-" * 50)

        # Tenta carregar o banco de dados existente ao iniciar
        self.rag_service.load_repository()

        while True:
            user_input = input("\nVocê (ou digite um comando): ").strip().lower()

            if user_input in ['exit', 'quit']:
                print("Saindo do Paper-Pal-RAG. Até logo!")
                break
            elif user_input == 'ingest':
                self.rag_service.ingest_documents_from_directory(ARTICLES_DIR)
                print("Ingestão de documentos concluída.")
                continue
            elif user_input == 'clear':
                confirm = input("Tem certeza que deseja remover todos os documentos? (sim/não): ").strip().lower()
                if confirm == 'sim':
                    self.rag_service.clear_all_documents()
                else:
                    print("Operação de limpeza cancelada.")
                continue

            if not user_input:
                print("Por favor, digite sua pergunta ou um comando.")
                continue

            try:
                response, retrieved_docs = self.rag_service.query_documents(user_input)
                print("\n" + "=" * 50)
                print("Resposta do Paper-Pal-RAG:")
                print(response)
                print("=" * 50)

                if retrieved_docs:
                    print("\n--- Documentos Referenciados (Para Comparação) ---")
                    for i, doc in enumerate(retrieved_docs):
                        # Assegura que 'chunk_id' e 'file_name' estão nos metadados
                        chunk_id = doc.metadata.get('chunk_id', 'N/A')
                        file_name = doc.metadata.get('file_name', 'N/A')
                        
                        print(f"\nDocumento {i+1} (ID: {chunk_id}, Arquivo: {file_name}):")
                        print("Conteúdo:")
                        print(doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)
                        # Opcional: printar mais metadados
                        # print(f"Metadados: {doc.metadata}")
                    print("--------------------------------------------------")
                else:
                    print("\nNenhum documento relevante encontrado para esta consulta no contexto.")

            except LLMGenerationError as e:
                print(f"Erro ao gerar resposta: {e}. Por favor, verifique se o LM Studio está rodando e configurado corretamente.")
            except Exception as e:
                print(f"Ocorreu um erro inesperado: {e}")