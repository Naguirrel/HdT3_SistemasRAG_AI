import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


PROJECT_ROOT = Path(__file__).resolve().parent
FAQ_FILE = "FAQs_Parachute_SA_Guatemala_2026.txt"
FAQ_PATH = PROJECT_ROOT / FAQ_FILE
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "openai/gpt-oss-20b"
MISSING_INFORMATION_RESPONSE = (
    "No puedo responder con la informacion disponible en el archivo de FAQs."
)


def load_faq_context(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"No se encontro el archivo requerido: {path.name}")
    if not path.is_file():
        raise ValueError(f"La ruta configurada para las FAQs no es un archivo: {path}")

    try:
        content = path.read_text(encoding="utf-8").strip()
    except OSError as error:
        raise OSError(f"No se pudo leer el archivo de FAQs: {error}") from error

    if not content:
        raise ValueError(f"El archivo {path.name} esta vacio.")

    return content


def create_client() -> OpenAI:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "No se encontro GROQ_API_KEY. Configurala en el archivo .env antes de ejecutar el agente."
        )

    return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)


def build_system_prompt(faq_context: str) -> str:
    return f"""
Eres el agente oficial de preguntas frecuentes de Parachute S.A.

Reglas obligatorias:
- Responde utilizando exclusivamente la informacion contenida en las FAQs proporcionadas abajo.
- No utilices conocimiento externo.
- No inventes, completes ni deduzcas datos que no esten respaldados directamente por las FAQs.
- Puedes redactar respuestas naturales y resumir informacion, pero cada afirmacion factual debe estar respaldada por las FAQs.
- El historial de conversacion solo sirve para entender referencias de seguimiento, como "y donde"; no convierte datos del usuario en fuente de conocimiento.
- Si las FAQs no contienen informacion suficiente para responder, di exactamente: "{MISSING_INFORMATION_RESPONSE}"

FAQs proporcionadas:
--------------------
{faq_context}
""".strip()


def ask_faq_agent(client: OpenAI, messages: list[dict[str, str]], question: str) -> str:
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )

    answer = response.choices[0].message.content
    if not answer:
        answer = MISSING_INFORMATION_RESPONSE
    else:
        answer = answer.strip()

    messages.append({"role": "assistant", "content": answer})
    return answer


def print_banner() -> None:
    print("=" * 40)
    print("     PARACHUTE S.A. - FAQ AGENT")
    print("=" * 40)
    print("Pregunta sobre el evento.")
    print('Escribe "Bye" para salir.')


def run_chat() -> int:
    load_dotenv(PROJECT_ROOT / ".env")

    try:
        faq_context = load_faq_context(FAQ_PATH)
        client = create_client()
    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"Error: {error}")
        return 1

    messages = [{"role": "system", "content": build_system_prompt(faq_context)}]

    print_banner()

    while True:
        try:
            question = input("\nTu: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nHasta luego.")
            return 0

        if question.lower() == "bye":
            print("Hasta luego.")
            return 0

        if not question:
            continue

        try:
            answer = ask_faq_agent(client, messages, question)
        except KeyboardInterrupt:
            print("\nHasta luego.")
            return 0
        except OpenAIError as error:
            messages.pop()
            print(f"\nError al consultar la API de Groq: {error}")
            continue
        except Exception as error:
            messages.pop()
            print(f"\nError inesperado al consultar el modelo: {error}")
            continue

        print(f"\nAgente: {answer}")


if __name__ == "__main__":
    sys.exit(run_chat())
