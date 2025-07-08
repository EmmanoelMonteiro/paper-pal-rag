# src/infrastructure/vector_store_impl.py

from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings # Para embeddings locais
from langchain_core.documents import Document
import os

from src.domain.document_repository import IDocumentRepository
from src.core.config import CHROMA_DB_DIR, EMBEDDING_MODEL_NAME
from src.core.exceptions import EmbeddingGenerationError, DocumentNotFoundError

class ChromaDocumentRepository(IDocumentRepository):
    """
    Implementação do IDocumentRepository usando ChromaDB como banco de dados vetorial.
    """

    def __init__(self, db_directory: str = CHROMA_DB_DIR, embedding_model_name: str = EMBEDDING_MODEL_NAME):
        """
        Inicializa o repositório ChromaDB.

        Args:
            db_directory (str): O caminho para o diretório onde o ChromaDB será persistido.
            embedding_model_name (str): O nome do modelo de embeddings a ser usado.
        """
        self.db_directory = db_directory
        self.embedding_model_name = embedding_model_name
        self.embeddings = self._initialize_embeddings()
        self.vector_store: Chroma | None = None
        self.load_existing_db() # Tenta carregar o DB existente na inicialização

    def _initialize_embeddings(self):
        """
        Inicializa o modelo de embeddings.
        """
        try:
            # Baixa e carrega o modelo de embeddings do HuggingFace
            return HuggingFaceEmbeddings(model_name=self.embedding_model_name)
        except Exception as e:
            raise EmbeddingGenerationError(f"Erro ao inicializar o modelo de embeddings '{self.embedding_model_name}': {e}")

    def add_documents(self, documents: List[Document]):
        """
        Adiciona uma lista de documentos ao repositório de vetores ChromaDB.
        Se o DB não existir, ele será criado.
        """
        if not documents:
            print("Nenhum documento para adicionar.")
            return

        if self.vector_store is None:
            print("Criando novo banco de dados Chroma ou carregando existente...")
            self.vector_store = Chroma.from_documents(
                documents,
                self.embeddings,
                persist_directory=self.db_directory
            )
        else:
            print(f"Adicionando {len(documents)} documentos ao banco de dados Chroma existente...")
            self.vector_store.add_documents(documents)
        
        print("Documentos adicionados ao ChromaDB.")

    def search_documents(self, query: str, k: int = 5) -> List[Document]:
        """
        Pesquisa documentos no repositório com base em uma consulta usando similaridade vetorial.

        Args:
            query (str): A consulta de texto para pesquisa.
            k (int): O número de documentos mais relevantes a serem retornados.

        Returns:
            List[Document]: Uma lista de documentos relevantes (chunks).
        """
        if self.vector_store is None:
            print("Banco de dados vetorial não carregado ou não existe. Retornando lista vazia.")
            return []
        
        # Realiza a busca por similaridade
        results = self.vector_store.similarity_search(query, k=k)
        print(f"Encontrados {len(results)} documentos relevantes.")
        return results

    def get_document_by_id(self, doc_id: str) -> Document | None:
        """
        Recupera um documento específico (chunk) pelo seu ID de metadado.
        Note: O ChromaDB não tem um método direto para buscar por um ID arbitrário nos metadados.
        Esta implementação fará uma busca por todos os documentos e filtrará.
        Para grandes volumes, considere otimizações ou um ID direto na coleção do Chroma.
        """
        if self.vector_store is None:
            return None
        
        # Esta é uma abordagem simplificada e pode ser ineficiente para muitos documentos.
        # Uma alternativa seria armazenar um mapeamento de ID -> Document em memória ou em outro DB.
        # Ou, usar o get() do Chroma se você armazenar o ID como o "ID" da coleção Chroma.
        
        # Atualmente, o Chroma.get() retorna docs pelos seus IDs internos.
        # Para buscar por um metadado 'chunk_id', precisaríamos de um método de filtro
        # ou iterar sobre os documentos (o que não é exposto facilmente via API de alto nível).
        
        # Uma forma de simular isso para fins de demonstração (ineficiente para muitos docs)
        # seria buscar algo muito genérico e depois filtrar, mas isso é inviável.
        # A melhor forma seria que o DocumentLoader/Parser garantisse que 'chunk_id'
        # fosse o ID direto do documento no Chroma.

        # Para manter simples, vamos considerar que para a demonstração, o `retrieved_docs`
        # do search_documents já nos dará os IDs dos chunks.
        # Se você precisar de um get_by_id robusto, precisaríamos de uma estratégia diferente
        # ao adicionar documentos ao Chroma (e.g., passar um id explícito para add_documents).

        # Retornamos None por enquanto, pois a API do Chroma não facilita esta busca direta por metadado.
        # No seu chatbot, você receberá os documentos COMPLETOS (chunks) na lista `retrieved_docs`.
        # Você pode então simplesmente iterar sobre essa lista e pegar o `chunk_id` e `page_content`.
        
        # Se realmente precisar de um get_document_by_id, o ideal seria:
        # 1. Quando adicionar documentos, você passa uma lista de IDs personalizados:
        #    self.vector_store.add_documents(documents, ids=[doc.metadata['chunk_id'] for doc in documents])
        # 2. Então você pode usar self.vector_store.get(ids=[doc_id])
        print(f"Funcionalidade 'get_document_by_id' não implementada diretamente para metadados no ChromaDB de forma eficiente.")
        print(f"Para ver o conteúdo de um documento recuperado, observe o campo 'page_content' e 'chunk_id' nos documentos retornados pelo 'search_documents'.")
        return None


    def load_existing_db(self):
        """
        Carrega um banco de dados vetorial Chroma existente do disco.
        """
        if os.path.exists(self.db_directory) and len(os.listdir(self.db_directory)) > 0:
            print(f"Carregando banco de dados Chroma existente de: {self.db_directory}")
            self.vector_store = Chroma(
                persist_directory=self.db_directory,
                embedding_function=self.embeddings # Importante passar a função de embedding novamente
            )
            print("Banco de dados Chroma carregado.")
        else:
            print(f"Diretório do ChromaDB não encontrado ou vazio em: {self.db_directory}. Um novo será criado na primeira adição.")
            self.vector_store = None # Garante que o vector_store é None se não houver DB
            # Não é necessário criar aqui, será criado na primeira chamada a add_documents

    def persist_db(self):
        """
        Persiste o banco de dados vetorial no disco.
        """
        if self.vector_store:
            self.vector_store.persist()
            print(f"Banco de dados Chroma persistido em: {self.db_directory}")
        else:
            print("Nenhum banco de dados Chroma para persistir.")
    
    def clear_documents(self):
        """
        Remove todos os documentos do banco de dados vetorial e o diretório de persistência.
        """
        if os.path.exists(self.db_directory):
            import shutil
            try:
                shutil.rmtree(self.db_directory)
                self.vector_store = None
                print(f"Banco de dados Chroma em '{self.db_directory}' e todos os documentos removidos.")
            except Exception as e:
                print(f"Erro ao remover o diretório do ChromaDB: {e}")
        else:
            print("Nenhum banco de dados Chroma encontrado para remover.")