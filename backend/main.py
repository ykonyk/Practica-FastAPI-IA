from fastapi import FastAPI, HTTPException
from typing import List
import database
from models import PromptRequest, Creation
import ai_service
from fastapi.middleware.cors import CORSMiddleware

database.create_db_and_table()

app = FastAPI(
    title="Asistente Creativo AI API",
    description="API para generar contenido usando IA y guardar el historial.",
    version="0.1.0",
)


# --- Añadir CORS ---
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Fin de CORS ---


@app.post("/generate", response_model=Creation, status_code=201)
def create_generation_entry(request: PromptRequest):

    print(f"Recibido prompt: {request.prompt}, Tipo: {request.content_type}")

    try:
        # 1. Llama al servicio de IA para generar el texto
        generated_text = ai_service.generate_text(request.prompt, request.content_type)
        print(f"Texto generado: {generated_text[:100]}...") # Imprime los primeros 100 chars

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error inesperado llamando a la IA: {e}")
        raise HTTPException(status_code=500, detail="Error interno al contactar el servicio de IA")

    # 2. Guarda el prompt Y el texto generado en la base de datos
    creation_id = database.add_creation(
        prompt=request.prompt,
        content_type=request.content_type,
        generated_text=generated_text # Ahora guardamos el texto real
    )

    if creation_id == -1:
        raise HTTPException(status_code=500, detail="Error al guardar en la base de datos después de generar texto")

    # 3. Recupera y devuelve la entrada completa de la base de datos
    all_creations = database.get_all_creations() # Ineficiente, solo para ejemplo
    new_creation_dict = next((c for c in all_creations if c['id'] == creation_id), None)

    if not new_creation_dict:
        raise HTTPException(status_code=404, detail="Creación guardada pero no encontrada inmediatamente")

    return Creation(**new_creation_dict) # Devuelve el objeto completo

@app.get("/history", response_model=List[Creation])
def get_generation_history():

    try:
        history_data = database.get_all_creations()
        return history_data

    except Exception as e:
        print(f"Error inesperado obteniendo historial: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener el historial")