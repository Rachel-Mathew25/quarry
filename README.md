# ⛏ Quarry

Quarry is an autonomous founder intelligence agent that helps students find the right founders to cold email — and actually get responses.

Most cold emails fail because students email the wrong founder, at the wrong time, about the wrong thing. Quarry fixes the root cause.

## What it does

- Finds founders across GitHub, Twitter, LinkedIn, and the web — no username needed
- Analyzes their stack, recent activity, and what they're actively struggling with
- Compares their needs against your skills and identifies the exact gap
- Recommends a specific project to build that closes that gap
- Writes a brutally precise cold email that references something real
- Sends it automatically — zero effort from the student

## Architecture

agents/        # ReAct agent loop — orchestrates everything
tools/         # GitHub, Twitter, LinkedIn, web, email
rag/           # semantic chunking, embeddings, hybrid retrieval, memory
core/          # founder + student profiles, evaluation
data/chroma/   # vector database

## Tech stack

- LLM: Groq (LLaMA 3.3 70B)
- Embeddings: BAAI/bge-large-en-v1.5 via HuggingFace
- Vector DB: ChromaDB + FAISS
- Retrieval: Hybrid dense + sparse with cross-encoder reranking
- Web search: Tavily
- Scraping: BeautifulSoup
- Email: SMTP + Gmail API

## Setup

```bash
git clone https://github.com/Rachel-Mathew25/quarry
cd quarry
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
python main.py
```

## Status

🚧 Active development — Phase 1

Built by Rachel Mathew | Building in public: #buildinpublic
