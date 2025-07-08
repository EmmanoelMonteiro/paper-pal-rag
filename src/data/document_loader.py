# src/data/document_loader.py

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
import os
from typing import List, Dict, Any

from src.core.exceptions import DocumentLoadingError
from src.core.config import DEFAULT_METADATA

class DocumentLoader:
    """
    Classe para carregar documentos de diferentes formatos (PDF, TXT).
    """

    def load_document(self, file_path: str) -> List[Document]:
        """
        Carrega um documento a partir do caminho do arquivo.
        Determina o carregador apropriado com base na extensão do arquivo.

        Args:
            file_path (str): O caminho completo para o arquivo do documento.

        Returns:
            List[Document]: Uma lista de objetos Document carregados.
                            Normalmente, um PDF pode ser carregado como várias páginas,
                            cada uma se tornando um Document.

        Raises:
            DocumentLoadingError: Se o formato do arquivo não for suportado ou houver erro no carregamento.
        """
        if not os.path.exists(file_path):
            raise DocumentLoadingError(f"Arquivo não encontrado: {file_path}")

        file_extension = os.path.splitext(file_path)[1].lower()
        documents: List[Document] = []

        try:
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            elif file_extension == '.txt':
                loader = TextLoader(file_path)
                documents = loader.load()
            else:
                raise DocumentLoadingError(f"Formato de arquivo não suportado: {file_extension}")

            # Adicionar metadados padrão e o caminho do arquivo original
            for doc in documents:
                doc.metadata.update(DEFAULT_METADATA)
                doc.metadata["file_path"] = file_path
                doc.metadata["file_name"] = os.path.basename(file_path)

            return documents
        except Exception as e:
            raise DocumentLoadingError(f"Erro ao carregar o documento '{file_path}': {e}")