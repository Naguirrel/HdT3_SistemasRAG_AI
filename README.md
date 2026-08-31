# Parachute FAQ Agent

Agente basico de preguntas frecuentes para la empresa ficticia Parachute S.A.

El programa funciona desde la terminal y demuestra una arquitectura RAG simple: lee un archivo local de FAQs y envia su contenido como contexto a un modelo compatible con la API de OpenAI usando Groq.

No utiliza embeddings, bases de datos vectoriales, LangChain, LlamaIndex, frameworks web ni frontend.

## Requisitos

- Python 3.10 o superior
- Una API Key de Groq
- El archivo `FAQs_Parachute_SA_Guatemala_2026.txt` con el contenido de FAQs

## Crear entorno virtual

```bash
python -m venv .venv
```

Activar el entorno virtual:

```bash
source .venv/bin/activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configurar variables de entorno

Crea un archivo `.env` a partir de `.env.example`:

```bash
cp .env.example .env
```

Luego coloca tu API Key real de Groq en `.env`:

```env
GROQ_API_KEY=tu_api_key_real
```

El archivo `.env` esta incluido en `.gitignore` y no debe subirse al repositorio.

## Ejecutar

```bash
python main.py
```

## Uso

Escribe preguntas en la terminal. El agente respondera exclusivamente con informacion encontrada en `FAQs_Parachute_SA_Guatemala_2026.txt`.

Si una pregunta no puede responderse con ese archivo, el agente indicara que no puede responder con la informacion disponible.

Para salir, escribe:

```text
Bye
```

Tambien puedes salir usando `Ctrl+C`.
