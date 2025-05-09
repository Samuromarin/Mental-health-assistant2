from setuptools import setup, find_packages

setup(
    name="mental-health-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.0",
        "openai>=1.0.0",
        "anthropic>=0.5.0",
        "fschat[model_worker,webui]>=0.2.20",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "accelerate>=0.21.0",
        "sentence-transformers>=2.2.2",
        "gradio>=3.32.0",
        "fastapi>=0.95.0",
        "uvicorn>=0.22.0",
        "langchain>=0.0.200",
    ],
)