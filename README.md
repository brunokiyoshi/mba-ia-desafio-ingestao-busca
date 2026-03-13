# Desafio MBA Engenharia de Software com IA - Full Cycle

## Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose instalados
- Python 3.10+ com as dependências do projeto instaladas
- Uma chave de API da OpenAI

## Configuração do ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
OPENAI_API_KEY=sua-chave-aqui
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
PDF_PATH=caminho/para/o/arquivo.pdf
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documentos
```

Instale as dependências Python:

```bash
pip install -r requirements.txt
```

## Como executar

### 1. Subir os serviços

Inicie o banco de dados PostgreSQL com a extensão pgvector:

```bash
docker compose up -d
```

Aguarde os serviços ficarem saudáveis antes de prosseguir.

### 2. Ingerir o documento PDF

Execute o script de ingestão para carregar e indexar o PDF no banco de dados:

```bash
python src/ingest.py
```

Este passo processa o PDF definido em `PDF_PATH`, divide o conteúdo em chunks, gera os embeddings via OpenAI e armazena os vetores no PostgreSQL.

### 3. Iniciar o chat

Com os dados ingeridos, inicie a interface de chat para fazer perguntas sobre o documento:

```bash
python src/chat.py
```

Digite sua pergunta no prompt e pressione Enter. Para sair, digite `tchau` ou pressione `Ctrl+C`.

> **Observação:** O chat responde apenas com base no conteúdo do documento ingerido. Perguntas fora do contexto do documento receberão a resposta padrão indicando ausência de informação.