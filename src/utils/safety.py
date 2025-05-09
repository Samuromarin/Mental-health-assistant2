from src.config.settings import CRISIS_KEYWORDS, EMERGENCY_NUMBERS

def detect_crisis(message):
    """
    Detecta palabras clave de crisis en el mensaje del usuario
    
    Args:
        message (str): Mensaje del usuario
    
    Returns:
        tuple: (crisis_detected, keywords_found)
    """
    message_lower = message.lower()
    keywords_found = [word for word in CRISIS_KEYWORDS if word in message_lower]
    
    return bool(keywords_found), keywords_found

def get_crisis_response(keywords):
    """
    Genera una respuesta de protocolo de crisis basada en las palabras clave detectadas
    
    Args:
        keywords (list): Lista de palabras clave detectadas
    
    Returns:
        str: Mensaje de respuesta a la crisis
    """
    response = f"""
    **Mensaje importante de seguridad**
    
    He detectado contenido en tu mensaje que puede indicar que estás pasando por un momento difícil.
    
    Es importante que sepas que hay ayuda disponible:
    
    - Teléfono de Emergencias: {EMERGENCY_NUMBERS['general']}
    - Línea de Prevención del Suicidio: {EMERGENCY_NUMBERS['suicide_prevention']}
    
    Este asistente no está diseñado para manejar situaciones de crisis y no reemplaza 
    la ayuda profesional. Si estás en peligro inmediato, por favor contacta con los 
    servicios de emergencia.
    
    Si quieres seguir conversando sobre temas generales de salud mental, estoy aquí para ayudarte.
    """
    
    return response