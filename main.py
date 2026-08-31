import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


FAQ_FILE = "FAQs_Parachute_SA_Guatemala_2026.txt"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "openai/gpt-oss-20b"


def load_faq_context(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontro el archivo requerido: {file_path}")

    return path.read_text(encoding="utf-8").strip()


def create_client() -> OpenAI:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "No se encontro GROQ_API_KEY. Configurala en tu archivo .env o como variable de entorno."
        )

    return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)


def ask_faq_agent(client: OpenAI, faq_context: str, question: str) -> str:
    system_prompt = (
        "Eres un agente de preguntas frecuentes para Parachute S.A. "
        "Responde exclusivamente usando la informacion incluida en el contexto de FAQs. "
        "No uses conocimiento externo, no inventes datos y no completes informacion faltante. "
        "Si la respuesta no aparece claramente en el contexto, responde: "
        "'No puedo responder con la informacion disponible en el archivo de FAQs.'"
    )

    user_prompt = f"""
Contexto de FAQs:
{faq_context}

Pregunta del usuario:
{question}
""".strip()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


def run_chat() -> None:
    load_dotenv()

    try:
        faq_context = load_faq_context(FAQ_FILE)
        client = create_client()
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        sys.exit(1)

    if not faq_context:
        print(f"Advertencia: el archivo {FAQ_FILE} esta vacio.")

    print("Agente FAQ de Parachute S.A.")
    print("Escribe tus preguntas. Para salir, escribe Bye.")

    while True:
        try:
            question = input("\nPregunta: ").strip()
        except KeyboardInterrupt:
            print("\nSesion finalizada.")
            break

        if question.lower() == "bye":
            print("Sesion finalizada.")
            break

        if not question:
            continue

        try:
            answer = ask_faq_agent(client, faq_context, question)
            print(f"\nRespuesta: {answer}")
        except Exception as error:
            print(f"\nError al consultar el modelo: {error}")


if __name__ == "__main__":
    run_chat()
