import sys
import os
import time
import importlib
from dotenv import load_dotenv

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar variables de entorno
load_dotenv()

from src.config.settings import OPENAI_API_KEY, FASTCHAT_CONFIG
from src.fastchat.controller import launch_controller
from src.fastchat.model_worker import launch_worker
from src.fastchat.api_server import launch_api_server
from src.fastchat.web_ui import launch_web_server

def import_module_safely(name):
    """Importa un módulo de forma segura, mostrando un error claro si falla"""
    try:
        return importlib.import_module(name)
    except ImportError as e:
        print(f"❌ Error al importar {name}: {e}")
        return None
    
def check_api_keys():
    """Verifica que las claves API necesarias estén configuradas"""
    if not OPENAI_API_KEY and FASTCHAT_CONFIG["model_worker"]["model_path"] == "facebook/opt-350m":
        print("⚠️ No se ha encontrado la clave API de OpenAI ni un modelo local.")
        print("   Se utilizará un modelo pequeño OPT-350M para demostraciones.")
        print("   Para mejor rendimiento, configura MODEL_PATH en .env con un modelo de LLM local")
        print("   o configura OPENAI_API_KEY para usar la API de OpenAI.")
        return True
    return True

def initialize_fastchat():
    """Inicializa todos los componentes de FastChat"""
    # 1. Iniciar controlador
    controller_thread = launch_controller()
    
    # 2. Iniciar trabajador del modelo
    worker_thread = launch_worker()
    
    # 3. Iniciar servidor API
    api_thread = launch_api_server()
    
    # 4. Iniciar interfaz web
    web_thread = launch_web_server()
    
    return {
        "controller": controller_thread,
        "worker": worker_thread,
        "api": api_thread,
        "web": web_thread
    }

def main():
    """Función principal para ejecutar el asistente"""
    try:
        print("🤖 Iniciando Asistente de Salud Mental con FastChat...")
        
        # Verificar si el modelo está descargado
        try:
            from src.utils.download_model import is_model_downloaded, download_vicuna
            
            model_path = os.getenv("MODEL_PATH", "lmsys/vicuna-7b-v1.5")
            print(f"📦 Modelo configurado: {model_path}")
            
            if not is_model_downloaded(model_path):
                print(f"⚠️ El modelo {model_path} no está descargado.")
                download = input("¿Deseas descargarlo ahora? (s/n): ")
                if download.lower() == "s":
                    downloaded_path = download_vicuna(model_path)
                    if downloaded_path:
                        os.environ["MODEL_PATH"] = downloaded_path
                        print(f"✅ Modelo descargado en: {downloaded_path}")
                    else:
                        print("❌ No se pudo descargar el modelo. El asistente podría no funcionar correctamente.")
                else:
                    print("⚠️ Continuando sin descargar el modelo. El asistente podría no funcionar correctamente.")
            else:
                print(f"✅ Modelo encontrado: {model_path}")
        except ImportError:
            print("⚠️ No se pudo verificar el modelo. Asegúrate de tener el módulo download_model.py")
        
        # Verificar dependencias
        try:
            import fastchat
            print(f"✅ FastChat instalado (versión: {getattr(fastchat, '__version__', 'desconocida')})")
        except ImportError:
            print("❌ FastChat no está instalado correctamente.")
            print("   Ejecuta: pip install 'fschat[model_worker,webui]'")
            return False
        
        try:
            import gradio
            print(f"✅ Gradio instalado (versión: {getattr(gradio, '__version__', 'desconocida')})")
        except ImportError:
            print("❌ Gradio no está instalado correctamente.")
            print("   Ejecuta: pip install gradio")
            return False
            
        # Importar módulos de FastChat usando las versiones alternativas
        print("📦 Cargando componentes...")
        controller_module = import_module_safely("src.fastchat.controller")
        model_worker_module = import_module_safely("src.fastchat.model_worker")
        web_ui_module = import_module_safely("src.fastchat.web_ui")
        
        if not (controller_module and model_worker_module and web_ui_module):
            print("❌ No se pudieron cargar todos los módulos necesarios.")
            return False
            
        # Inicializar componentes
        print("🚀 Iniciando componentes...")
        controller_thread = controller_module.launch_controller()
        time.sleep(2)  # Esperar a que el controlador se inicie
        
        worker_thread = model_worker_module.launch_worker()
        time.sleep(5)  # Esperar a que el worker se inicie
        
        web_thread = web_ui_module.launch_web_server()
        
        print("✨ ¡Asistente iniciado correctamente!")
        print("💬 Interfaz web disponible en http://localhost:7860")
        print("💡 Presiona Ctrl+C para detener el asistente")
        
        # Mantener el programa en ejecución
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Deteniendo el asistente...")
            
    except Exception as e:
        print(f"❌ Error al iniciar: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()