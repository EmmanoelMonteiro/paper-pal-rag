# src/core/exceptions.py

class DocumentLoadingError(Exception):
    """Exceção levantada quando há um erro ao carregar um documento."""
    pass

class EmbeddingGenerationError(Exception):
    """Exceção levantada quando há um erro ao gerar embeddings."""
    pass

class LLMGenerationError(Exception):
    """Exceção levantada quando há um erro na geração da LLM."""
    pass

class DocumentNotFoundError(Exception):
    """Exceção levantada quando um documento não é encontrado no repositório."""
    pass