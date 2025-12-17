<!-- Repository-specific Copilot instructions for Virtual Rajeev -->
# Virtual Rajeev — Copilot Instructions

This project is a local AI assistant that combines Retrieval-Augmented Generation (RAG) with a local LLM (Ollama). The instructions below capture the key patterns, workflows, and pitfalls an AI coding agent should know to be productive here.

- **Big picture**: The repo stores a small knowledge base under `knowledge/`. `build_memory.py` encodes those documents with `sentence-transformers` and saves a FAISS index (`memory.index`) plus raw texts (`memory.pkl`). The runtime scripts (`chat_with_memory.py`, `telegram_bot.py`) load `memory.index` + `memory.pkl`, encode an incoming query, retrieve top-k contexts, then call `ollama.chat` (model `llama3.2`) with a strict system prompt that forbids adding external knowledge.

- **Key files to inspect**: `build_memory.py`, `chat_with_memory.py`, `telegram_bot.py`, `test_ai_ollama.py`, `memory.index`, `memory.pkl`, and the `knowledge/` directory.

- **Primary workflows (explicit commands)**:
  - Rebuild retrieval memory after editing `knowledge/`:
    ```bash
    python build_memory.py
    ```
  - Quick local chat (CLI):
    ```bash
    python chat_with_memory.py
    ```
  - Run Telegram bot (ensure token and Ollama are running):
    ```bash
    python telegram_bot.py
    ```

- **Runtime expectations & dependencies**:
  - Requires a running Ollama service with the `llama3.2` model available.
  - Python deps used in code: `faiss`, `pickle` (builtin), `ollama` (client), `sentence-transformers`, `pypdf`, `python-telegram-bot`.
  - `SentenceTransformer("all-MiniLM-L6-v2")` is used for embeddings (download at first run).
  - FAISS index file `memory.index` and `memory.pkl` live at repo root after `build_memory.py` runs.

- **Project-specific patterns and conventions**:
  - Privacy guard: both `chat_with_memory.py` and `telegram_bot.py` explicitly block queries containing words like `mobile`, `phone`, `email`, `address`. Follow and preserve this pattern when adding endpoints or tests.
  - Query-aware routing: scripts include a `ROUTING_HINTS` dict (e.g., `"skill" -> "technical skills"`) to normalize search terms before embedding; maintain this when adding other entry points.
  - Strict-context answering: system messages instruct the model to answer ONLY from retrieved context and to return exactly: `This information is not mentioned in the provided data.` when unknown. Tests and new handlers must respect this exact phrasing.
  - Different top-k: `chat_with_memory.py` uses `k=3`, `telegram_bot.py` uses `k=5`. Preserve or intentionally change these values with a clear reason.

- **Debugging & quick checks (repo-specific)**:
  - If `memory.index` is missing or retrieval returns empty indices, run `python build_memory.py` and confirm `memory.index` and `memory.pkl` created.
  - If Ollama calls fail, verify the Ollama daemon and installed models (outside repo) — the code expects a reachable Ollama client and model `llama3.2`.
  - Use `test_ai_ollama.py` to verify basic Ollama connectivity and prompt format.

- **Security & maintenance notes discovered in code**:
  - `telegram_bot.py` contains a hardcoded `BOT_TOKEN` variable in `main()`; treat this as sensitive — prefer moving it to an environment variable and replacing with `os.environ.get("BOT_TOKEN")` when editing.

- **When editing or adding features**:
  - For any change that affects user-facing answers, check `chat_with_memory.py` and `telegram_bot.py` for the strict system prompt and SENSITIVE keywords to avoid breaking privacy behavior.
  - After adding or changing documents in `knowledge/`, always run `python build_memory.py` to keep `memory.index` and `memory.pkl` in sync.
  - Keep retrieval logic (embedding -> index.search -> join contexts) consistent: code expects `texts` to be aligned with FAISS indices loaded from `memory.pkl`.

If anything here is unclear or you'd like the instructions adjusted (more examples, different tone, or additional run/debug commands), tell me which part to expand or modify.
