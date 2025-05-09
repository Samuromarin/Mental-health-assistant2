import threading
import time
import importlib
import sys

def get_controller_class():
    """Obtiene la clase Controller de fastchat de manera dinámica"""
    # Intentar diferentes rutas de importación para compatibilidad con versiones
    possible_paths = [
        "fastchat.serve.controller", 
        "fastchat.controller",
        "fschat.serve.controller",
        "fschat.controller"
    ]
    
    for path in possible_paths:
        try:
            module = importlib.import_module(path)
            if hasattr(module, "Controller"):
                return module.Controller
            elif hasattr(module, "controller"):
                return module.controller.Controller
        except (ImportError, AttributeError):
            continue
    
    raise ImportError("No se pudo encontrar la clase Controller en el paquete FastChat. Verifica tu instalación.")

def start_controller():
    """Inicia el controlador de FastChat en un hilo separado"""
    try:
        # Intentar obtener la clase Controller
        Controller = get_controller_class()
        
        # Iniciar el controlador
        controller = Controller(
            host="localhost",
            port=21001
        )
        controller.start()
        return controller
    except Exception as e:
        print(f"Error al iniciar el controlador: {e}")
        return None

def launch_controller():
    """Lanza el controlador como un proceso daemon"""
    controller_thread = threading.Thread(target=start_controller)
    controller_thread.daemon = True
    controller_thread.start()
    # Esperar a que el controlador se inicie
    time.sleep(2)
    print(f"✅ Controlador iniciado en localhost:21001")
    return controller_thread
