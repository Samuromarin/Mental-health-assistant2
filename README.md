# Asistente de Salud Mental con FastChat

Este proyecto implementa un asistente virtual para salud mental utilizando FastChat y modelos de lenguaje de gran tamaño (LLMs).

## Requisitos

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- Opcional: GPU compatible con CUDA para mejor rendimiento

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo
   ```

2. Crea y activa un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```
   pip install -e .
   ```

4. Configura las variables de entorno:
   ```
   cp .env.example .env
   ```
   Edita el archivo `.env` con tus configuraciones.

## Uso

Para iniciar el asistente, ejecuta:

```
python src/main.py
```

El asistente iniciará los siguientes componentes:
- Controlador de FastChat
- Trabajador del modelo
- Servidor API compatible con OpenAI
- Interfaz web Gradio

Accede a la interfaz web en tu navegador en la dirección `http://localhost:7860`.

## Configuración

Puedes configurar el asistente modificando:

1. El archivo `.env` para cambiar claves API y rutas de modelos
2. `src/config/settings.py` para ajustar categorías, recursos y parámetros del chatbot


Para una inicialización más robusta, sigue este orden:

Verifica dependencias y entorno
Verifica/descarga el modelo
Inicia el controlador
Inicia el trabajador del modelo (con suficiente tiempo de espera)
Inicia el servidor API (opcional)
Inicia la interfaz web

Si alguno de estos componentes falla, proporciona un mensaje claro y opciones para continuar o salir.




## Modelos compatibles

Puedes usar cualquiera de estos tipos de modelos:

- Modelos locales (LLaMA, Vicuna, Falcon, etc.)
- OpenAI API (GPT-3.5, GPT-4)
- Anthropic API (Claude)

## Licencia

[Especifica tu licencia aquí]


## Modelos

Este asistente utiliza el modelo Vicuna para generar respuestas. Por defecto, descargará automáticamente el modelo `lmsys/vicuna-7b-v1.5` desde Hugging Face durante el primer inicio.

### Opciones de modelos

Puedes configurar qué modelo usar en el archivo `.env`:

- `MODEL_PATH=lmsys/vicuna-7b-v1.5` - Modelo de 7B parámetros, buena calidad y requisitos moderados
- `MODEL_PATH=lmsys/vicuna-13b-v1.5` - Modelo de 13B parámetros, mejor calidad pero requiere más VRAM
- `MODEL_PATH=ruta/local/al/modelo` - Si ya tienes el modelo descargado

### Requisitos de hardware

- **Recomendado**: GPU NVIDIA con al menos 12GB de VRAM
- **Mínimo**: 8GB de VRAM con cuantización de 8 bits habilitada (`LOAD_8BIT=True`)
- **CPU solamente**: Funcionará pero será extremadamente lento

### Descarga manual (opcional)

Si prefieres descargar el modelo manualmente:

```bash
python src/utils/download_model.py --model lmsys/vicuna-7b-v1.5 --output models/vicuna-7b-v1.5
