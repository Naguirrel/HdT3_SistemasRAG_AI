# Parachute S.A. - FAQ Agent

Agente de preguntas frecuentes para el evento de paracaidismo de Parachute S.A. en Guatemala. El programa se ejecuta desde terminal y responde preguntas usando solamente el archivo local `FAQs_Parachute_SA_Guatemala_2026.txt`.

## Arquitectura RAG simple

Este proyecto demuestra una arquitectura RAG deliberadamente sencilla:

1. El programa lee el archivo local de FAQs desde el filesystem.
2. Inyecta todo el contenido del TXT en las instrucciones del agente.
3. Envia la pregunta del usuario al modelo mediante Groq.
4. El modelo responde exclusivamente con informacion respaldada por ese TXT.

No se utilizan embeddings, busqueda vectorial, bases de datos vectoriales, LangChain, LlamaIndex, frameworks web, frontend, Docker ni bases de datos. La unica fuente de conocimiento permitida es `FAQs_Parachute_SA_Guatemala_2026.txt`.

Si la respuesta no esta en las FAQs, el agente debe admitirlo claramente con este mensaje:

```text
No puedo responder con la informacion disponible en el archivo de FAQs.
```

## Tecnologias

- Python
- OpenAI Python SDK
- Groq mediante endpoint compatible con OpenAI
- python-dotenv

## Estructura del proyecto

```text
.
|-- FAQs_Parachute_SA_Guatemala_2026.txt
|-- main.py
|-- requirements.txt
|-- .env.example
|-- .gitignore
`-- README.md
```

`main.py` carga las FAQs, configura el cliente de Groq con el SDK oficial `openai`, mantiene una sesion interactiva por terminal y conserva historial conversacional para preguntas de seguimiento.

## Instalacion

Crear un entorno virtual:

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuracion de la API Key

Crear el archivo `.env` a partir de `.env.example`:

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

Editar `.env` y colocar la API Key real de Groq:

```env
GROQ_API_KEY=
```

La variable debe llamarse exactamente `GROQ_API_KEY`. El programa termina de forma limpia si esa variable no existe o esta vacia.

## Ejecucion

Windows:

```powershell
python main.py
```

Linux/macOS:

```bash
python3 main.py
```

Interfaz esperada:

```text
========================================
     PARACHUTE S.A. - FAQ AGENT
========================================
Pregunta sobre el evento.
Escribe "Bye" para salir.

Tu: ¿Cuando es el evento?
Agente: ...

Tu: ¿Y donde?
Agente: ...
```

Para salir, escribe `Bye` con cualquier combinacion de mayusculas/minusculas y espacios, o presiona `Ctrl+C`.

## Ejemplos de preguntas

- ¿Cuando y donde sera el evento?
- ¿Cual es el limite de peso?
- ¿Que metodos de pago aceptan?
- ¿Puedo llevar mi propia camara?
- ¿Que pasa si hay mal clima?

## Seguridad

El archivo `.env` contiene secretos locales y no debe subirse al repositorio. `.gitignore` incluye `.env`, entornos virtuales, cache de Python y archivos compilados.

No escribas una API Key real en `README.md`, `.env.example`, `main.py` ni ningun otro archivo del proyecto.
