from fastapi import FastAPI
from app.nlu.train import predict_intent
from fastapi.middleware.cors import CORSMiddleware
import unicodedata
import re

app = FastAPI(title="Chatbot Universitario - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API activa"}

@app.post("/predict/")
def get_intent(user_input: dict):
    text = user_input.get("message", "")
    text = normalize_text(text)
    intent, confidence, respuesta, sugerencias = predict_intent(text)
    if confidence < 0.4:
        return {
            "intent": None,
            "confidence": confidence,
            "respuesta": "No estoy completamente seguro de tu intención. ¿Quizás quisiste decir una de estas? \n" +
                         "\n".join(f"- {s}" for s in sugerencias),
        }

    return {
        "intent": intent,
        "confidence": confidence,
        "respuesta": respuesta
    }

def normalize_text(text: str) -> str:
    normaliced_text = text
    try:
        # Quitar tildes y diacríticos
        normaliced_text = unicodedata.normalize("NFKD", normaliced_text)
        normaliced_text = "".join([c for c in normaliced_text if not unicodedata.combining(c)])
        # Convertir a minúsculas
        normaliced_text = normaliced_text.lower()
        # Eliminar signos de puntuación y caracteres no alfanuméricos
        normaliced_text = re.sub(r"[^a-z0-9áéíóúñü\s]", " ", normaliced_text)
        # Reemplazar múltiples espacios por uno
        normaliced_text = re.sub(r"\s+", " ", normaliced_text)
    except Exception as e:
        print(f"Error normalizing text: {e}")
        normaliced_text = text

    return text.strip()
