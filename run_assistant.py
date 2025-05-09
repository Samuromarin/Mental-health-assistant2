import os
import sys
import subprocess
import time
import importlib
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def import_module_safely(name):
    """Importa un módulo de forma segura, mostrando un error claro si falla"""
    try:
        return importlib.import_module(name)
    except ImportError as e:
        print(f"❌ Error al importar {name}: {e}")
        return None

def check_environment():
    """Verifica el entorno y las dependencias"""
    print("🔍 Verificando entorno...")
    
    # Verificar Python
    print(f"Python: {sys.version}")
    
    # Verificar dependencias principales
    dependencies = ["fastchat", "gradio", "transformers", "torch", "huggingface_hub"]
    for dep in dependencies:
        try:
            module = __import__(dep)
            version = getattr(module, "__version__", "desconocida")
            print(f"✅ {dep}: {version}")
        except ImportError:
            print(f"❌ {dep} no está instalado")
            install = input(f"¿Deseas instalar {dep}? (s/n): ")
            if install.lower() == "s":
                subprocess.run([sys.executable, "-m", "pip", "install", dep])

def check_model():
    """Verifica si el modelo está descargado y lo descarga si es necesario"""
    try:
        from src.utils.download_model import is_model_downloaded, download_vicuna
        
        model_path = os.getenv("MODEL_PATH", "lmsys/vicuna-7b-v1.5")
        print(f"📦 Modelo configurado: {model_path}")
        
        if not is_model_downloaded(model_path):
            print(f"⚠️ El modelo {model_path} no está descargado.")
            print(f"🔄 Descargando automáticamente...")
            downloaded_path = download_vicuna(model_path)
            if downloaded_path:
                os.environ["MODEL_PATH"] = downloaded_path
                print(f"✅ Modelo descargado en: {downloaded_path}")
                return True
            else:
                print("❌ No se pudo descargar el modelo. El asistente podría no funcionar correctamente.")
                return False
        else:
            print(f"✅ Modelo encontrado: {model_path}")
            return True
    except ImportError as e:
        print(f"⚠️ No se pudo verificar el modelo: {e}")
        print("⚠️ Asegúrate de tener el módulo src/utils/download_model.py")
        
        create_module = input("¿Deseas crear el módulo de descarga ahora? (s/n): ")
        if create_module.lower() == "s":
            create_download_module()
            return check_model()  # Verificar nuevamente después de crear el módulo
        return False

def create_download_module():
    """Crea el módulo de descarga de modelos si no existe"""
    os.makedirs("src/utils", exist_ok=True)
    
    download_code = """
import os
import argparse
from huggingface_hub import snapshot_download, login
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def download_vicuna(model_name=None, output_dir=None, use_auth_token=None):
    \"\"\"
    Descarga el modelo Vicuna desde Hugging Face Hub
    
    Args:
        model_name (str): Nombre del modelo en Hugging Face Hub
        output_dir (str): Directorio de salida donde se guardará el modelo
        use_auth_token (str): Token de autenticación de Hugging Face Hub
    
    Returns:
        str: Ruta donde se guardó el modelo
    \"\"\"
    # Si no se especifica un modelo, usar el de las variables de entorno o el predeterminado
    if model_name is None:
        model_name = os.getenv("MODEL_PATH", "lmsys/vicuna-7b-v1.5")
    
    # Si es una ruta local y existe, simplemente devolverla
    if os.path.exists(model_name) and not model_name.startswith(('lmsys/', 'meta-llama/')):
        print(f"✅ Modelo encontrado localmente en: {model_name}")
        return model_name
    
    print(f"🔄 Descargando modelo {model_name}...")
    
    if output_dir is None:
        # Si no se especifica un directorio, usamos uno predeterminado
        output_dir = os.path.join("models", model_name.split("/")[-1])
    
    # Crear el directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Si el token no se proporciona, intentar obtenerlo del entorno
    if use_auth_token is None:
        use_auth_token = os.getenv("HUGGINGFACE_TOKEN")
    
    # Si el token está disponible, hacer login
    if use_auth_token:
        login(use_auth_token)
    
    try:
        # Descargar el modelo usando snapshot_download
        snapshot_download(
            repo_id=model_name,
            local_dir=output_dir,
            token=use_auth_token,
            ignore_patterns=["*.msgpack", "*.h5", "*.ot", "*.md"]
        )
        print(f"✅ Modelo descargado exitosamente en: {output_dir}")
        
        # Verificar si el modelo se puede cargar correctamente
        print("🔍 Verificando modelo...")
        
        # Intentar cargar el tokenizer
        try:
            tokenizer = AutoTokenizer.from_pretrained(output_dir)
            print("✅ Tokenizer cargado correctamente")
        except Exception as e:
            print(f"⚠️ Error al cargar el tokenizer: {e}")
        
        # Intentar cargar el modelo con bajo uso de memoria
        try:
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            model = AutoModelForCausalLM.from_pretrained(
                output_dir,
                torch_dtype=dtype,
                low_cpu_mem_usage=True,
                device_map="auto"
            )
            print("✅ Modelo cargado correctamente")
            # Liberar memoria
            del model
            torch.cuda.empty_cache()
        except Exception as e:
            print(f"⚠️ Error al cargar el modelo: {e}")
            print("🔔 Esto podría ser normal si no hay suficiente memoria. FastChat lo cargará después con configuraciones optimizadas.")
        
        return output_dir
        
    except Exception as e:
        print(f"❌ Error al descargar el modelo: {e}")
        print("⚠️ Si necesitas acceso a modelos como LLaMA, asegúrate de tener un token de Hugging Face con los permisos correctos.")
        print("   Puedes configurar el token en la variable de entorno HUGGINGFACE_TOKEN")
        return None

def is_model_downloaded(model_name=None):
    \"\"\"Verifica si el modelo ya está descargado\"\"\"
    if model_name is None:
        model_name = os.getenv("MODEL_PATH", "lmsys/vicuna-7b-v1.5")
    
    # Si es una ruta local
    if os.path.exists(model_name) and not model_name.startswith(('lmsys/', 'meta-llama/')):
        return True
    
    # Si es un modelo de Hugging Face
    default_path = os.path.join("models", model_name.split("/")[-1])
    return os.path.exists(default_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Descargar modelo Vicuna")
    parser.add_argument("--model", type=str, default=None, help="Nombre del modelo en Hugging Face o ruta local")
    parser.add_argument("--output", type=str, default=None, help="Directorio de salida")
    parser.add_argument("--token", type=str, default=None, help="Token de Hugging Face (si es necesario)")
    parser.add_argument("--check", action="store_true", help="Solo verificar si el modelo está descargado")
    
    args = parser.parse_args()
    
    if args.check:
        if is_model_downloaded(args.model):
            print("✅ El modelo ya está descargado")
        else:
            print("❌ El modelo no está descargado")
    else:
        download_vicuna(args.model, args.output, args.token)
"""
    
    with open("src/utils/download_model.py", "w") as f:
        f.write(download_code.strip())
    
    print("✅ Módulo de descarga creado en src/utils/download_model.py")
    
    # También crear __init__.py si no existe
    if not os.path.exists("src/utils/__init__.py"):
        with open("src/utils/__init__.py", "w") as f:
            f.write("# Este archivo permite importar el módulo\n")

def main():
    """Función principal para iniciar el asistente"""
    check_environment()
    
    # Verificar y posiblemente descargar el modelo
    print("\n🔍 Verificando modelo...")
    check_model()
    
    print("\n🚀 Iniciando asistente de salud mental...")
    
    # Ejecutar directamente el archivo main_alt.py
    try:
        # Importar módulos alternativos
        print("📦 Cargando componentes...")
        controller_module = import_module_safely("src.fastchat.controller_alt")
        model_worker_module = import_module_safely("src.fastchat.model_worker_alt")
        web_ui_module = import_module_safely("src.fastchat.web_ui_alt")
        
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