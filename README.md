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
git clone [https://github.com/seu-usuario/Paper-Pal-RAG.git](https://github.com/seu-usuario/Paper-Pal-RAG.git)
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

```
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

###5. Configurar o LM Studio
1. Abra o LM Studio.

2. Na barra lateral esquerda, navegue até a seção **"Home"** (ícone de casa) ou **"Discover"** (ícone de lupa) para encontrar e baixar um modelo de sua preferência (ex: `gemma-2b-it` ou um modelo da série Llama).

3. Vá para a aba **"Local Inference Server"** (geralmente a quarta aba, ícone de terminal com "localhost").

4. Clique em **"Start Server"**. Certifique-se de que o servidor está rodando na porta `1234` (esta é a porta padrão e configurada no projeto).