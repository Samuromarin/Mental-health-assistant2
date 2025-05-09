import threading
import time
import os
import importlib
from src.config.settings import FASTCHAT_CONFIG

def get_model_worker_class():
    """Obtiene la clase ModelWorker de fastchat de manera dinámica"""
    # Intentar diferentes rutas de importación para compatibilidad con versiones
    possible_paths = [
        "fastchat.serve.model_worker", 
        "fastchat.model_worker",
        "fschat.serve.model_worker",
        "fschat.model_worker"
    ]
    
    for path in possible_paths:
        try:
            module = importlib.import_module(path)
            if hasattr(module, "ModelWorker"):
                return module.ModelWorker
            elif hasattr(module, "model_worker"):
                return module.model_worker.ModelWorker
        except (ImportError, AttributeError):
            continue
    
    raise ImportError("No se pudo encontrar la clase ModelWorker en el paquete FastChat. Verifica tu instalación.")

def start_worker():
    """Inicia el trabajador del modelo de FastChat para Vicuna"""
    # Obtener configuración desde settings
    cfg = FASTCHAT_CONFIG["model_worker"]
    
    # Configuración básica
    model_path = cfg.get("model_path", os.getenv("MODEL_PATH", "lmsys/vicuna-7b-v1.5"))
    device = cfg.get("device", os.getenv("DEVICE", "cpu"))
    controller_addr = f"http://{FASTCHAT_CONFIG['controller']['host']}:{FASTCHAT_CONFIG['controller']['port']}"
    worker_addr = f"http://{cfg.get('host', 'localhost')}:{cfg.get('port', 21002)}"
    worker_id = cfg.get("worker_id", "mental_health_worker")
    
    # Configuración avanzada
    load_8bit = cfg.get("load_8bit", False)
    cpu_offloading = cfg.get("cpu_offloading", False)
    gpus = os.getenv("GPUS", "")
    num_gpus = int(cfg.get("num_gpus", os.getenv("NUM_GPUS", "1")))
    max_gpu_memory = cfg.get("max_gpu_memory", None)
    
    # Configurar GPUs visibles
    if gpus:
        os.environ["CUDA_VISIBLE_DEVICES"] = gpus
    
    try:
        # Intentar obtener la clase ModelWorker
        ModelWorker = get_model_worker_class()
        
        print(f"🔄 Iniciando trabajador para el modelo: {model_path}...")
        worker = ModelWorker(
            controller_addr=controller_addr,
            worker_addr=worker_addr,
            worker_id=worker_id,
            model_path=model_path,
            model_names=cfg.get("model_names", ["vicuna", "mental_health_assistant"]),
            device=device,
            num_gpus=num_gpus,
            max_gpu_memory=max_gpu_memory,
            load_8bit=load_8bit,
            cpu_offloading=cpu_offloading,
            max_context_len=2048
        )
        worker.start()
        return worker
    except Exception as e:
        print(f"Error al iniciar el trabajador: {e}")
        return None

def launch_worker():
    """Lanza el trabajador del modelo como un proceso daemon"""
    worker_thread = threading.Thread(target=start_worker)
    worker_thread.daemon = True
    worker_thread.start()
    # Esperar a que el worker se inicie
    time.sleep(8)  # Vicuna puede tardar un poco en cargar
    print(f"✅ Trabajador del modelo iniciado en {FASTCHAT_CONFIG['model_worker'].get('host', 'localhost')}:{FASTCHAT_CONFIG['model_worker'].get('port', 21002)}")
    return worker_thread
