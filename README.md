# AI Engineer Journey
This is personal learning project for AI engineer.

# Ubuntu 22.04 Environment Setup
- curl -fsSL https://ollama.com/install.sh | sh  # Ollama is open source, locally-running large language model, as kind of "local ChatGPT"
- systemctl status ollama
- ollama pull qwen2.5-coder:7b

# Python venv
- python3 -m venv venv
- source venv/bin/activate
- pip install --upgrade pip
- pip install openai pydantic
- pip install chromadb sentence-transformers    # Task 2.2, RAG vector database

# Environment Re-check
- curl http://localhost:11434/api/tags ( If "{"models":[{"name":"qwen2.5-coder:7b",...}]}" was found, environment is okay )
- python3 -c "import openai; from pydantic import BaseModel; print('Environment dependencies check is pass.')"
