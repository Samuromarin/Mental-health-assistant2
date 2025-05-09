from src.config.settings import VICUNA_PROMPT_TEMPLATE, MENTAL_HEALTH_CATEGORIES

def format_prompt_for_vicuna(message, category="General"):
    """
    Formatea el mensaje del usuario para el modelo Vicuna,
    optimizando para el contexto de salud mental
    
    Args:
        message (str): Mensaje del usuario
        category (str): Categoría de salud mental seleccionada
    
    Returns:
        str: Prompt formateado para Vicuna
    """
    # Si el usuario seleccionó una categoría específica, la incluimos en el contexto
    if category != "General":
        context_message = f"(Contexto: El usuario quiere hablar sobre temas relacionados con {category.lower()}) {message}"
    else:
        context_message = message
    
    return VICUNA_PROMPT_TEMPLATE.format(message=context_message)

def get_category_specific_instructions(category):
    """
    Devuelve instrucciones específicas según la categoría de salud mental
    
    Args:
        category (str): Categoría de salud mental
    
    Returns:
        str: Instrucciones específicas para esa categoría
    """
    instructions = {
        "Ansiedad": """
            Para temas de ansiedad: Muestra una actitud calmada, valida sus sentimientos,
            enseña técnicas de respiración y relajación cuando sea apropiado, y explora
            desencadenantes específicos con preguntas abiertas.
        """,
        "Depresión": """
            Para temas de depresión: Utiliza un enfoque de escucha empática, valida sus
            experiencias sin minimizarlas, explora patrones de pensamiento, y pregunta
            sobre actividades que antes disfrutaban. Mantén un tono esperanzador pero realista.
        """,
        "Estrés": """
            Para manejo del estrés: Ayuda a identificar fuentes de estrés, explora estrategias
            de afrontamiento, sugiere técnicas de mindfulness cuando sea apropiado, y ayuda
            a priorizar el autocuidado.
        """,
        "Relaciones": """
            Para problemas de relaciones: Escucha sin juzgar, evita tomar partido, ayuda a
            explorar patrones de comunicación, y anima a considerar diferentes perspectivas.
        """,
        "Autoestima": """
            Para problemas de autoestima: Ayuda a identificar fortalezas personales, cuestiona
            pensamientos autocríticos, y fomenta una autoimagen más compasiva y realista.
        """,
        "Técnicas de relajación": """
            Para técnicas de relajación: Guía en respiración profunda, relajación muscular progresiva,
            visualización o mindfulness. Ofrece instrucciones paso a paso cuando sea apropiado.
        """
    }
    
    return instructions.get(category, "")