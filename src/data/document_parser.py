# src/data/document_parser.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

from src.core.config import CHUNK_SIZE, CHUNK_OVERLAP

class DocumentParser:
    """
    Classe para processar e dividir documentos em chunks.
    """

    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        """
        Inicializa o DocumentParser com o tamanho do chunk e a sobreposição.

        Args:
            chunk_size (int): O número máximo de caracteres em cada chunk.
            chunk_overlap (int): O número de caracteres que se sobrepõem entre chunks adjacentes.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Divide uma lista de documentos em chunks menores.

        Args:
            documents (List[Document]): Uma lista de objetos Document a serem divididos.

        Returns:
            List[Document]: Uma lista de novos objetos Document, cada um representando um chunk.
        """
        chunks = self.text_splitter.split_documents(documents)
        
        # Adicionar um ID único e sequencial para cada chunk
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_id'] = f"{chunk.metadata.get('file_name', 'unknown')}_chunk_{i}"
        
        return chunks