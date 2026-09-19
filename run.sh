#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# LegalPilot-VN: Environment Startup Script
# ==============================================================================

echo "[+] Starting LegalPilot-VN foundation setup..."

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Error: python3 is not installed."
    exit 1
fi

# 2. Check or create .env file
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "[+] Creating .env from .env.example..."
        cp .env.example .env
    else
        echo "[!] Warning: .env.example not found. Creating empty .env..."
        touch .env
    fi
fi

# 3. Check Docker and start database services
if command -v docker &> /dev/null && docker compose version &> /dev/null; then
    echo "[+] Starting Neo4j and Qdrant services..."
    docker compose up -d
else
    echo "[!] Warning: Docker is not available. Ensure Neo4j and Qdrant are running."
fi

# 4. Check and activate virtual environment
if [ -d ".venv" ]; then
    echo "[+] Activating virtual environment (.venv)..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "[+] Activating virtual environment (venv)..."
    source venv/bin/activate
fi

# 5. Run database initialization
echo "[+] Initializing SQLite enterprise compliance database..."
python3 -c "from src.memory.sqlite_manager import SQLiteMemoryManager; mgr = SQLiteMemoryManager(); mgr.init_tables(); print('[+] SQLite tables verified.')"

echo "[+] LegalPilot-VN foundation setup completed."
echo "    Start the Web UI with: streamlit run src/ui/app.py"
