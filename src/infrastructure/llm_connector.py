# src/infrastructure/llm_connector.py

from langchain_openai import ChatOpenAI # <-- NOVA IMPORTAÇÃO
from langchain_core.prompts import PromptTemplate
from src.core.config import LM_STUDIO_API_BASE, LM_STUDIO_MODEL_NAME
from src.core.exceptions import LLMGenerationError
from langchain_core.messages import HumanMessage, SystemMessage # <-- NOVA IMPORTAÇÃO para prompts de chat

class LLMConnector:
    """
    Conector para interagir com um modelo de linguagem (LLM) hospedado via LM Studio.
    """

    def __init__(self, api_base: str = LM_STUDIO_API_BASE, model_name: str = LM_STUDIO_MODEL_NAME):
        """
        Inicializa o conector LLM.

        Args:
            api_base (str): O URL base da API do LM Studio (ex: "http://localhost:1234/v1").
            model_name (str): O nome do modelo a ser usado (pode ser ignorado pelo LM Studio
                              se apenas um modelo estiver carregado).
        """
        # Inicializa ChatOpenAI apontando para o LM Studio
        # A chave de API não é necessária para o LM Studio local
        self.llm = ChatOpenAI(
            openai_api_base=api_base,
            openai_api_key="not-needed",  # Chave de API não é necessária para LM Studio
            model_name=model_name,        # Pode ser "lm_studio_default" ou o nome real do modelo
            temperature=0.1,              # Ajuste conforme desejar a criatividade da resposta
            streaming=True                # Opcional: permite streaming da resposta
        )

        # O template de prompt precisa ser ajustado para o formato de mensagens de chat
        # A cadeia será construída com `messages` em vez de `PromptTemplate` direto no invoke
        # O prompt `self.template` e `self.prompt` serão removidos ou adaptados para uso futuro com LCEL
        # Por enquanto, vamos construir a lista de mensagens diretamente na função generate_response.

    def generate_response(self, question: str, context: str = "") -> str:
        """
        Gera uma resposta da LLM com base na pergunta e no contexto fornecido.

        Args:
            question (str): A pergunta do usuário.
            context (str): O texto de contexto recuperado dos documentos.

        Returns:
            str: A resposta gerada pela LLM.

        Raises:
            LLMGenerationError: Se a chamada à LLM falhar.
        """
        try:
            messages = [
                SystemMessage(content="Você é um assistente de leitura de artigos científicos. Use as informações do CONTEXTO para responder à PERGUNTA do usuário. Se a resposta não estiver no contexto, diga que não tem informações suficientes nos documentos fornecidos. Seja conciso, útil e direto."),
            ]

            if context.strip():
                messages.append(HumanMessage(content=f"CONTEXTO:\n{context}\n\nPERGUNTA: {question}"))
            else:
                messages.append(HumanMessage(content=f"PERGUNTA: {question}"))

            print("Enviando requisição à LLM...")
            # Usar .invoke com a lista de mensagens
            response = self.llm.invoke(messages)
            return response.content.strip() # ChatOpenAI retorna um objeto ChatMessage

        except Exception as e:
            raise LLMGenerationError(f"Erro ao chamar a LLM para geração de resposta: {e}")