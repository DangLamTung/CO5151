#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# LegalPilot-VN: All-in-One Startup Script
# ==============================================================================

echo "🚀 Starting LegalPilot-VN Foundation Setup..."

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed."
    exit 1
fi

# 2. Check or create .env file
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "📋 Copying .env.example to .env..."
        cp .env.example .env
    else
        echo "⚠️ Warning: .env.example not found. Creating a minimal .env..."
        touch .env
    fi
fi

# 3. Check Docker and start databases if available
if command -v docker &> /dev/null && docker compose version &> /dev/null; then
    echo "🐳 Starting Neo4j and Qdrant containers..."
    docker compose up -d
else
    echo "⚠️ Docker is not available. Please ensure Neo4j and Qdrant are running manually."
fi

# 4. Check virtual environment
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment (.venv)..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "📦 Activating virtual environment (venv)..."
    source venv/bin/activate
fi

# 5. Run database initialization
echo "🗄️ Initializing SQLite enterprise compliance database..."
python3 -c "from src.memory.sqlite_manager import SQLiteMemoryManager; mgr = SQLiteMemoryManager(); mgr.init_tables(); print('✅ SQLite initialized successfully.')"

echo "🎉 LegalPilot-VN Foundation is ready!"
echo "To start the Web UI, run: streamlit run src/ui/app.py"
