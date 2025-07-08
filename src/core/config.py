# src/core/config.py

import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Caminhos de Diretório ---
# Obtém o diretório base do projeto (onde main.py está localizado)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Caminho para a pasta onde os artigos (PDFs/TXTs) serão armazenados
ARTICLES_DIR = os.path.join(BASE_DIR, 'data', 'articles')

# Caminho para o diretório onde o banco de dados vetorial será persistido
# Usaremos 'chroma_db' como o nome do diretório do banco de dados Chroma
CHROMA_DB_DIR = os.path.join(BASE_DIR, 'data', 'chroma_db')

# --- Configurações do LM Studio (LLM) ---
# Endereço base do servidor LM Studio (padrão é http://localhost:1234/v1)
# Você pode configurar isso como uma variável de ambiente se preferir, mas aqui está direto para simplificar
LM_STUDIO_API_BASE = os.getenv("LM_STUDIO_API_BASE", "http://localhost:1234/v1")
# Nome do modelo a ser usado (pode não ser necessário se o LM Studio estiver configurado para um único modelo)
LM_STUDIO_MODEL_NAME = os.getenv("LM_STUDIO_MODEL_NAME", "lm_studio_default")

# --- Configurações do Embeddings ---
# Modelo de embeddings a ser usado.
# 'sentence-transformers/all-MiniLM-L6-v2' é um bom modelo leve para começar.
# Se você tiver um modelo de embeddings no LM Studio, pode usá-lo também.
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# --- Configurações do Splitter de Texto ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# --- Metadados Padrão ---
# Metadados que podem ser adicionados aos documentos carregados
DEFAULT_METADATA = {
    "source_type": "scientific_article"
}