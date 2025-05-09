import os
import argparse
from huggingface_hub import snapshot_download, login
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def download_vicuna(model_name=None, output_dir=None, use_auth_token=None):
    """
    Descarga el modelo Vicuna desde Hugging Face Hub
    
    Args:
        model_name (str): Nombre del modelo en Hugging Face Hub
        output_dir (str): Directorio de salida donde se guardará el modelo
        use_auth_token (str): Token de autenticación de Hugging Face Hub
    
    Returns:
        str: Ruta donde se guardó el modelo
    """
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
    """Verifica si el modelo ya está descargado"""
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