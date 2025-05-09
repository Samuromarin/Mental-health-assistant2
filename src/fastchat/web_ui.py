import threading
import time
import importlib
import os
import gradio as gr

def get_gradio_app_and_blocks():
    """Obtiene las funciones y clases necesarias de gradio y fastchat de manera dinámica"""
    # Intentar diferentes rutas de importación para compatibilidad con versiones
    possible_paths = [
        "fastchat.serve.gradio_web_server", 
        "fastchat.gradio_web_server",
        "fschat.serve.gradio_web_server",
        "fschat.gradio_web_server"
    ]
    
    for path in possible_paths:
        try:
            module = importlib.import_module(path)
            
            # Buscar la función build_single_model_ui o app
            if hasattr(module, "build_single_model_ui"):
                return module.build_single_model_ui, None
            elif hasattr(module, "app"):
                return None, module.app
        except (ImportError, AttributeError):
            continue
    
    raise ImportError("No se pudieron encontrar los componentes necesarios de FastChat para la interfaz web.")

def custom_mental_health_ui():
    """Crea una interfaz de usuario personalizada para el asistente de salud mental"""
    # Obtener la función para construir la interfaz
    build_ui_func, app = get_gradio_app_and_blocks()
    
    if build_ui_func:
        # Podemos construir una interfaz personalizada
        with gr.Blocks(title="Asistente de Salud Mental") as demo:
            with gr.Row():
                with gr.Column(scale=3):
                    gr.Markdown(
                        """# Asistente Virtual de Salud Mental
                        
                        Este chatbot está diseñado para proporcionar soporte emocional y psicoeducación.
                        No reemplaza a profesionales de salud mental. Si experimentas una crisis o emergencia,
                        contacta con servicios de emergencia locales o líneas de crisis.
                        
                        **Recursos de emergencia:**
                        - Línea de Prevención del Suicidio: 024
                        - Emergencias: 112
                        """
                    )
                    
                with gr.Column(scale=1):
                    # Aquí podrías añadir un logo si lo tienes
                    pass
            
            # Intenta obtener categorías de entorno o usa valores predeterminados
            categories = ["General", "Ansiedad", "Depresión", "Estrés", "Relaciones"]
            
            with gr.Row():
                topic = gr.Radio(
                    categories,
                    label="Selecciona un tema",
                    info="Esto ayuda al asistente a contextualizar mejor tu consulta",
                    value="General"
                )
                
            # Construir la interfaz de chat
            chat_interface = build_ui_func()
            
            with gr.Accordion("Parámetros", open=False):
                temperature = gr.Slider(0.1, 1.5, 0.7, 
                                       label="Temperatura", 
                                       info="Controla la creatividad de las respuestas")
                max_new_tokens = gr.Slider(64, 4096, 512, 
                                          label="Longitud máxima", 
                                          step=64)
                
            # Eventos
            def update_prompt(category):
                if category == "General":
                    return "Hola, me gustaría conversar contigo."
                
                prompts = {
                    "Ansiedad": "Últimamente me siento ansioso. ¿Podrías ayudarme?",
                    "Depresión": "He estado sintiéndome sin energía y con poco interés en las cosas.",
                    "Estrés": "El estrés me está afectando mucho últimamente.",
                    "Relaciones": "Estoy teniendo dificultades en mis relaciones personales."
                }
                
                return prompts.get(category, f"Me gustaría hablar sobre {category.lower()}.")
            
            if hasattr(chat_interface, "textbox"):
                topic.change(update_prompt, inputs=topic, outputs=chat_interface.textbox)
            
        return demo
    elif app:
        # Si solo tenemos acceso a la app predefinida, usamos esa
        return app
    else:
        # Fallback: crear una interfaz muy básica
        with gr.Blocks(title="Asistente de Salud Mental") as demo:
            gr.Markdown("# Asistente de Salud Mental")
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            clear = gr.Button("Limpiar")
            
            def respond(message, chat_history):
                bot_message = f"Echo: {message}"
                chat_history.append((message, bot_message))
                return "", chat_history
            
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: None, None, chatbot, queue=False)
            
        return demo

def start_web_server():
    """Inicia el servidor web de Gradio"""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "7860"))
    share = os.getenv("SHARE_GRADIO", "False").lower() == "true"
    
    try:
        ui = custom_mental_health_ui()
        ui.queue(concurrency_count=5)
        ui.launch(
            server_name=host,
            server_port=port,
            share=share
        )
    except Exception as e:
        print(f"Error al iniciar la interfaz web: {e}")
        # Intento de fallback con la interfaz básica de gradio
        print("Intentando iniciar interfaz básica...")
        with gr.Blocks(title="Asistente de Salud Mental") as demo:
            gr.Markdown("# Asistente de Salud Mental (Modo Básico)")
            gr.Markdown("⚠️ La interfaz completa no pudo iniciarse. Este es un modo básico de fallback.")
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            clear = gr.Button("Limpiar")
            
            def respond(message, chat_history):
                bot_message = "Lo siento, el modelo no está disponible en este momento."
                chat_history.append((message, bot_message))
                return "", chat_history
            
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: None, None, chatbot, queue=False)
            
        demo.launch(server_name=host, server_port=port, share=share)

def launch_web_server():
    """Lanza el servidor web como un proceso daemon"""
    web_thread = threading.Thread(target=start_web_server)
    web_thread.daemon = True
    web_thread.start()
    print(f"✅ Interfaz web iniciándose en http://localhost:7860")
    return web_thread