# src/domain/document_repository.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain_core.documents import Document

class IDocumentRepository(ABC):
    """
    Interface abstrata para o repositório de documentos.
    Define os métodos para persistir e recuperar documentos e embeddings.
    """

    @abstractmethod
    def add_documents(self, documents: List[Document]):
        """
        Adiciona uma lista de documentos ao repositório de vetores.
        """
        pass

    @abstractmethod
    def search_documents(self, query: str, k: int = 5) -> List[Document]:
        """
        Pesquisa documentos no repositório com base em uma consulta.

        Args:
            query (str): A consulta de texto para pesquisa.
            k (int): O número de documentos mais relevantes a serem retornados.

        Returns:
            List[Document]: Uma lista de documentos relevantes.
        """
        pass

    @abstractmethod
    def get_document_by_id(self, doc_id: str) -> Document | None:
        """
        Recupera um documento específico pelo seu ID.

        Args:
            doc_id (str): O ID único do documento/chunk.

        Returns:
            Document | None: O objeto Document se encontrado, caso contrário None.
        """
        pass

    @abstractmethod
    def load_existing_db(self):
        """
        Carrega um banco de dados vetorial existente do disco.
        """
        pass

    @abstractmethod
    def persist_db(self):
        """
        Persiste o banco de dados vetorial no disco.
        """
        pass

    @abstractmethod
    def clear_documents(self):
        """
        Limpa todos os documentos do repositório.
        """
        pass