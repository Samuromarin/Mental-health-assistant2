import threading
import uvicorn
from fastchat.serve.openai_api_server import app as openai_api_app
from src.config.settings import FASTCHAT_CONFIG

def start_api_server():
    """Inicia el servidor API compatible con OpenAI"""
    cfg = FASTCHAT_CONFIG["api_server"]
    uvicorn.run(
        openai_api_app,
        host=cfg["host"],
        port=cfg["port"]
    )

def launch_api_server():
    """Lanza el servidor API como un proceso daemon"""
    api_thread = threading.Thread(target=start_api_server)
    api_thread.daemon = True
    api_thread.start()
    cfg = FASTCHAT_CONFIG["api_server"]
    print(f"✅ Servidor API iniciado en {cfg['host']}:{cfg['port']}")
    return api_thread