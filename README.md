# 📚 Paper-Pal-RAG: Assistente de Leitura para Artigos Científicos

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/LangChain-v0.2+-success?style=for-the-badge&logo=langchain" alt="LangChain Version">
  <img src="https://img.shields.io/badge/LM_Studio-Compatible-informational?style=for-the-badge&logo=ai" alt="LM Studio Compatible">
  <img src="https://img.shields.io/badge/ChromaDB-Local-important?style=for-the-badge" alt="ChromaDB">
</p>

## Visão Geral do Projeto

O **Paper-Pal-RAG** é um assistente de leitura inteligente em **Python** que usa **Retrieval Augmented Generation (RAG)** para ajudar você a extrair e entender informações de artigos científicos.

Este projeto mostra uma arquitetura modular e escalável, usando **LangChain** para orquestração, **LM Studio** como servidor da Large Language Model (LLM) local, e **ChromaDB** para armazenamento vetorial. É perfeito para quem busca uma solução robusta e com arquitetura limpa para processar e consultar documentos.

## ✨ Funcionalidades

* **Ingestão de Documentos Flexível**: Carrega artigos científicos em **PDF** (`PyPDFLoader`) e **TXT** (`TextLoader`).
* **Geração Aumentada por Recuperação (RAG)**: O sistema busca informações relevantes nos seus documentos antes de gerar uma resposta com a LLM.
* **LLM Local com LM Studio**: Conecta-se facilmente a uma LLM rodando localmente via [LM Studio](https://lmstudio.ai/), garantindo privacidade e controle.
* **Armazenamento Vetorial Persistente**: Usa **ChromaDB** para armazenar e consultar embeddings de documentos de forma eficiente e persistente.
* **Interface de Chat Simples**: Interaja com o assistente por linha de comando, fazendo perguntas sobre o conteúdo dos artigos.
* **Contexto Transparente**: Além da resposta da LLM, o sistema mostra o **ID do chunk** e o **conteúdo exato dos documentos** usados como base para a resposta, o que ajuda na validação e depuração.
* **Arquitetura Limpa**: O código é organizado em camadas (`core`, `data`, `domain`, `infrastructure`, `presentation`) para promover modularidade, testabilidade e facilitar futuras expansões.

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o Paper-Pal-RAG no seu ambiente local.

### Pré-requisitos

* **Python 3.9+**: Verifique sua versão com `python --version`.
* **LM Studio**: Baixe e instale o [LM Studio](https://lmstudio.ai/).

### 1. Clonar o Repositório

```bash
git clone https://github.com/EmmanoelMonteiro/paper-pal-rag.git
cd Paper-Pal-RAG
```

### 2. Configurar o Ambiente Virtual

É **altamente recomendado** usar um ambiente virtual para gerenciar as dependências do projeto.

```bash
python -m venv .venv
```

### 3. Ativar o Ambiente Virtual
* Windows (PowerShell):

```bash
.\.venv\Scripts\activate
```

* Linux / macOS (Bash/Zsh):
```bash
source ./.venv/bin/activate
```

### 4. Instalar Dependências
Crie um arquivo chamado requirements.txt na raiz do projeto com o seguinte conteúdo:

```bash
langchain
langchain-community
langchain-openai
pypdf
chromadb
python-dotenv
sentence-transformers
```
Agora, instale as dependências:

```bash
pip install -r requirements.txt
```

### 5. Configurar o LM Studio
1. Abra o LM Studio.

2. Na barra lateral esquerda, navegue até a seção **"Home"** (ícone de casa) ou **"Discover"** (ícone de lupa) para encontrar e baixar um modelo de sua preferência (ex: `gemma-2b-it` ou um modelo da série Llama).

3. Vá para a aba **"Local Inference Server"** (geralmente a quarta aba, ícone de terminal com "localhost").

4. Clique em **"Start Server"**. Certifique-se de que o servidor está rodando na porta `1234` (esta é a porta padrão e configurada no projeto).

### 6. Configurar Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do seu projeto (Paper-Pal-RAG/) e adicione as seguintes linhas:

```bash
# .env
LM_STUDIO_API_BASE=http://localhost:1234/v1
LM_STUDIO_MODEL_NAME=lm_studio_default # Ou o nome exato do modelo que você carregou no LM Studio, ex: gemma-2-2b-it
```

### 7. Adicionar seus Artigos
Crie uma pasta chamada `articles` dentro de `data/` na raiz do seu projeto. Coloque seus arquivos **PDFs** e **TXTs** dentro de `Paper-Pal-RAG/data/articles/.`

### 8. Estrutura do Projeto (Certifique-se de que os __init__.py existem!)
Para que o Python reconheça a estrutura de módulos corretamente, verifique se arquivos `__init__.py` (que podem ser vazios) existem nas seguintes pastas:

```bash
Paper-Pal-RAG/
├── src/
│   ├── __init__.py          <- DEVE EXISTIR
│   ├── core/
│   │   ├── __init__.py      <- DEVE EXISTIR
│   ├── data/
│   │   ├── __init__.py      <- DEVE EXISTIR
│   ├── domain/
│   │   ├── __init__.py      <- DEVE EXISTIR
│   ├── infrastructure/
│   │   ├── __init__.py      <- DEVE EXISTIR
│   ├── presentation/
│   │   ├── __init__.py      <- DEVE EXISTIR
│   ├── main.py
├── data/
│   └── articles/
│       └── seu_artigo.pdf
│       └── suas_notas.txt
├── .env
├── requirements.txt
└── README.md
```
### 9. Executar o Chatbot
Com o ambiente virtual ativado e o LM Studio rodando, execute o projeto a partir da raiz do seu diretório:

```bash
python -m src.main
```

## 🤝 Como Usar o Chatbot

Ao iniciar, você verá uma mensagem de boas-vindas. Siga os comandos:

1. **Ingerir Documentos:** Digite `ingest` e pressione Enter. O sistema carregará e processará todos os artigos na pasta `data/articles/`, criando ou atualizando o banco de dados vetorial (`data/chroma_db`).

```bash
Você (ou digite um comando): ingest
```

2. **Fazer Perguntas:** Após a ingestão, digite sua pergunta sobre o conteúdo dos artigos.

```bash
Você (ou digite um comando): Qual a metodologia principal do estudo sobre IA?
```

3. **Visualizar Contexto:** A resposta incluirá a geração da LLM e os trechos exatos dos documentos (com seus IDs e nome de arquivo) que foram usados como contexto para a resposta.

4. **Limpar Documentos:** Para remover todos os documentos do banco de dados, digite `clear`.

```bash
Você (ou digite um comando): clear
```

5. **Sair:** Digite `exit` ou `quit` para encerrar o chatbot.

Sinta-se à vontade para explorar, modificar e contribuir para este projeto. Sua colaboração é bem-vinda!

Qualquer dúvida ou problema, sinta-se à vontade para abrir uma issue no repositório.
