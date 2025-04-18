import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException

# Carga las variables de entorno del archivo .env
load_dotenv()

OPENAI_API_KEY = os.getenv("")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

if not OPENAI_API_KEY:
    print("ADVERTENCIA: La variable de entorno OPENAI_API_KEY no está configurada.")
    raise ValueError("Se requiere la API Key de OpenAI en el archivo .env")

def generate_text(prompt: str, content_type: str) -> str:
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="La API Key de OpenAI no está configurada en el servidor.")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    system_prompt = f"Eres un asistente creativo. Genera el siguiente tipo de contenido: {content_type}."
    user_prompt = prompt
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 150,
        "temperature": 0.8,
    }

    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30) 
        response.raise_for_status()
        data = response.json()
        generated_content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        if not generated_content:
            print("Respuesta de la API recibida, pero sin contenido generado.")
            return "No se pudo generar contenido."

        return generated_content

    except requests.exceptions.RequestException as e:

        print(f"Error llamando a la API de OpenAI: {e}")
        if e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response Body: {e.response.text}")
            if e.response.status_code == 401:
                raise HTTPException(status_code=401, detail="Error de autenticación con la API de IA. Verifica la API Key.")
            elif e.response.status_code == 429:
                raise HTTPException(status_code=429, detail="Límite de tasa de la API de IA alcanzado.")
            else:
                raise HTTPException(status_code=503, detail=f"Error de la API de IA: {e.response.status_code}")
        else:
            raise HTTPException(status_code=503, detail=f"No se pudo conectar con la API de IA: {e}")
    except (KeyError, IndexError) as e:
        print(f"Error procesando la respuesta de la API: {e}")
        print(f"Respuesta recibida: {data if 'data' in locals() else 'No data'}")
        raise HTTPException(status_code=500, detail="Formato de respuesta inesperado de la API de IA.")