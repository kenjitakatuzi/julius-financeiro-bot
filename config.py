import os
import base64
from dotenv import load_dotenv

load_dotenv()

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')


def setup_google_credentials():
    """Setup Google credentials from environment variable if credentials file doesn't exist"""
    if os.path.exists(GOOGLE_CREDENTIALS_FILE):
        print(f"✓ Arquivo {GOOGLE_CREDENTIALS_FILE} encontrado")
        return

    creds_env = os.getenv('GOOGLE_CREDENTIALS')
    if not creds_env:
        print(f"⚠️ Arquivo {GOOGLE_CREDENTIALS_FILE} não encontrado e GOOGLE_CREDENTIALS não está definido")
        return

    try:
        if not creds_env.strip().startswith('{'):
            print("Decodificando credenciais do Google de base64...")
            creds_json = base64.b64decode(creds_env)
        else:
            print("Usando credenciais do Google da variável de ambiente...")
            creds_json = creds_env.encode()

        with open(GOOGLE_CREDENTIALS_FILE, 'wb') as f:
            f.write(creds_json)
        print(f"✓ Credenciais do Google salvas em {GOOGLE_CREDENTIALS_FILE}")
    except Exception as e:
        print(f"❌ Erro ao processar credenciais do Google: {e}")


def validate_config():
    """Validate required configuration"""
    setup_google_credentials()

    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN não encontrado nas variáveis de ambiente")
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY não encontrada nas variáveis de ambiente")
    if not GOOGLE_SHEET_ID:
        raise ValueError("GOOGLE_SHEET_ID não encontrado nas variáveis de ambiente")