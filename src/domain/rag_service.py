# src/domain/rag_service.py

import os
from typing import List, Tuple
from langchain_core.documents import Document

from src.domain.document_repository import IDocumentRepository
from src.data.document_loader import DocumentLoader
from src.data.document_parser import DocumentParser
from src.infrastructure.llm_connector import LLMConnector
from src.core.exceptions import DocumentLoadingError, LLMGenerationError

class RAGService:
    """
    Serviço que orquestra as operações de RAG (Retrieval Augmented Generation).
    Lida com o carregamento, processamento, armazenamento e consulta de documentos,
    e a geração de respostas com a LLM.
    """

    def __init__(self,
                 document_loader: DocumentLoader,
                 document_parser: DocumentParser,
                 document_repo: IDocumentRepository,
                 llm_connector: LLMConnector):
        """
        Inicializa o RAGService.

        Args:
            document_loader (DocumentLoader): O carregador de documentos.
            document_parser (DocumentParser): O parser/splitter de documentos.
            document_repo (IDocumentRepository): O repositório para persistência de documentos e embeddings.
            llm_connector (LLMConnector): O conector para o modelo de linguagem (LLM).
        """
        self.document_loader = document_loader
        self.document_parser = document_parser
        self.document_repo = document_repo
        self.llm_connector = llm_connector

    def ingest_documents_from_directory(self, directory_path: str):
        """
        Carrega, processa e adiciona documentos de um diretório ao repositório.

        Args:
            directory_path (str): O caminho para o diretório contendo os artigos.
        """
        print(f"Iniciando ingestão de documentos do diretório: {directory_path}")
        loaded_documents: List[Document] = []
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    docs = self.document_loader.load_document(file_path)
                    loaded_documents.extend(docs)
                    print(f" - Carregado: {file_name}")
                except DocumentLoadingError as e:
                    print(f" - Erro ao carregar {file_name}: {e}")
        
        if not loaded_documents:
            print("Nenhum documento carregado para ingestão.")
            return

        print(f"Total de {len(loaded_documents)} documentos brutos carregados. Dividindo em chunks...")
        chunks = self.document_parser.split_documents(loaded_documents)
        print(f"Total de {len(chunks)} chunks gerados.")

        print("Adicionando chunks ao banco de dados vetorial...")
        self.document_repo.add_documents(chunks)
        print("Documentos adicionados e embeddings gerados.")
        self.document_repo.persist_db() # Persiste o DB após adicionar
        print("Banco de dados vetorial persistido.")

    def query_documents(self, query: str) -> Tuple[str, List[Document]]:
        """
        Realiza uma consulta RAG: pesquisa documentos relevantes e gera uma resposta com a LLM.

        Args:
            query (str): A pergunta do usuário.

        Returns:
            Tuple[str, List[Document]]: Uma tupla contendo a resposta gerada pela LLM
                                        e a lista de documentos (chunks) usados como contexto.
        
        Raises:
            LLMGenerationError: Se a LLM falhar ao gerar uma resposta.
        """
        print(f"\nBuscando documentos relevantes para a consulta: '{query}'...")
        retrieved_docs = self.document_repo.search_documents(query)
        
        if not retrieved_docs:
            print("Nenhum documento relevante encontrado para a consulta.")
            # Gerar uma resposta base sem contexto se nenhum documento for encontrado
            try:
                base_response = self.llm_connector.generate_response(f"Responda à seguinte pergunta: {query}")
                return f"Não encontrei informações diretamente relevantes nos artigos, mas posso tentar responder: {base_response}", []
            except LLMGenerationError as e:
                raise LLMGenerationError(f"Erro ao gerar resposta sem contexto: {e}")

        # Construir o contexto para a LLM
        context_texts = "\n---\n".join([doc.page_content for doc in retrieved_docs])
        
        print(f"Documentos relevantes encontrados. Enviando para a LLM...")
        try:
            response = self.llm_connector.generate_response(query, context=context_texts)
            return response, retrieved_docs
        except Exception as e:
            raise LLMGenerationError(f"Erro ao gerar resposta da LLM: {e}")

    def load_repository(self):
        """
        Carrega o banco de dados vetorial existente.
        """
        self.document_repo.load_existing_db()
        print("Banco de dados vetorial carregado (se existir).")
    
    def clear_all_documents(self):
        """
        Limpa todos os documentos do repositório.
        """
        self.document_repo.clear_documents()
        print("Todos os documentos foram removidos do repositório.")