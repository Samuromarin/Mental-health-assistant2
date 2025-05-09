import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de APIs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Configuración del modelo
DEFAULT_MODEL = "gpt-4"  # o "claude-3-opus-20240229" si usas Anthropic
TEMPERATURE = 0.7
MAX_TOKENS = 500

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "src", "data")

# Configuración de seguridad
CRISIS_KEYWORDS = [
    "suicidio", "matarme", "quitarme la vida", "no quiero vivir", 
    "autolesión", "cortarme", "hacerme daño"
]

# Números de emergencia (ejemplo para España)
EMERGENCY_NUMBERS = {
    "general": "112",
    "suicide_prevention": "024"
}

# Configuración de FastChat
FASTCHAT_CONFIG = {
    "controller": {
        "host": "localhost",
        "port": 21001
    },
    "model_worker": {
        "host": "localhost",
        "port": 21002,
        "model_path": os.getenv("MODEL_PATH", "lmsys/vicuna-7b-v1.5"),  # Modelo Vicuna por defecto
        "device": os.getenv("DEVICE", "cpu"),
        "worker_id": "vicuna_mental_health_worker",
        "model_names": ["vicuna-7b", "mental-health-assistant"],  # Nombres amigables para la interfaz
        # Parámetros específicos para Vicuna
        "load_8bit": os.getenv("LOAD_8BIT", "False").lower() == "true",  # Cuantización de 8-bit para ahorrar memoria
        "cpu_offloading": os.getenv("CPU_OFFLOADING", "False").lower() == "true",  # Offloading a CPU si es necesario
        "gpus": os.getenv("GPUS", ""),  # GPUs específicas, ej: "0,1" para usar GPU 0 y 1
        "num_gpus": int(os.getenv("NUM_GPUS", "1")),  # Número de GPUs a usar
        "max_gpu_memory": os.getenv("MAX_GPU_MEMORY", None),  # Límite de memoria GPU, ej: "13GiB"
    },
    "api_server": {
        "host": "localhost",
        "port": 8000
    },
    "web_server": {
        "host": "0.0.0.0",
        "port": 7860,
        "share": os.getenv("SHARE_GRADIO", "False").lower() == "true"
    }
}

# Configuración específica de generación para Vicuna
VICUNA_GENERATION_CONFIG = {
    "temperature": float(os.getenv("TEMPERATURE", "0.7")),
    "top_p": float(os.getenv("TOP_P", "0.9")),
    "max_new_tokens": int(os.getenv("MAX_NEW_TOKENS", "512")), 
    "repetition_penalty": float(os.getenv("REPETITION_PENALTY", "1.1")),
}

# Template de prompt optimizado para Vicuna en el contexto de salud mental
VICUNA_PROMPT_TEMPLATE = """
A continuación hay una conversación entre un usuario y un Asistente Virtual de Salud Mental. El asistente está basado en el modelo Vicuna y está diseñado para proporcionar apoyo emocional, escucha empática y recursos psicoeducativos. El asistente es empático, respetuoso, utiliza preguntas abiertas para explorar las emociones del usuario, y evita dar consejos directivos cuando no es apropiado. No diagnostica ni reemplaza a profesionales de la salud mental.

USER: {message}
ASSISTANT:
"""

# Configuración de categorías de salud mental
MENTAL_HEALTH_CATEGORIES = [
    "General",
    "Ansiedad",
    "Depresión",
    "Estrés",
    "Relaciones",
    "Autoestima",
    "Técnicas de relajación"
]

# Recursos adicionales
RESOURCES = {
    "General": [
        {"name": "OMS - Salud Mental", "url": "https://www.who.int/es/health-topics/mental-health"},
        {"name": "Teléfono de la Esperanza", "url": "https://telefonodelaesperanza.org/"}
    ],
    "Ansiedad": [
        {"name": "Asociación TOC España", "url": "https://asociaciontoc.org/"},
        {"name": "Mind (Inglés)", "url": "https://www.mind.org.uk/information-support/types-of-mental-health-problems/anxiety-and-panic-attacks/"}
    ],
    "Depresión": [
        {"name": "Asociación Española de Psiquiatría", "url": "https://www.sepsiq.org/"},
        {"name": "Depression Alliance (Inglés)", "url": "https://www.depressionalliance.org/"}
    ]
}