import os
import yaml
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"
DB_PATH = ROOT / "rayzee.db"

PERSONAS_PATH = CONFIG_DIR / "personas.yaml"
ACCOUNTS_PATH = CONFIG_DIR / "accounts.yaml"

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# X OAuth2
X_CLIENT_ID = os.getenv("X_CLIENT_ID")
X_CLIENT_SECRET = os.getenv("X_CLIENT_SECRET") or None
X_REDIRECT_URI = os.getenv("X_REDIRECT_URI")
OAUTH_SERVER_HOST = os.getenv("OAUTH_SERVER_HOST", "127.0.0.1")
OAUTH_SERVER_PORT = int(os.getenv("OAUTH_SERVER_PORT", "5000"))

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

def load_yaml(path: Path):
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

PERSONAS = load_yaml(PERSONAS_PATH).get("personas", {})
ACCOUNTS = load_yaml(ACCOUNTS_PATH).get("accounts", {})
