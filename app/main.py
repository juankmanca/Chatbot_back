from fastapi import FastAPI
from app.nlu.train import predict_intent

app = FastAPI(title="Chatbot Universitario - Backend")

@app.get("/")
def root():
    return {"message": "API del Chatbot Universitario activa"}

@app.post("/predict/")
def get_intent(user_input: dict):
    text = user_input.get("message", "")
    intent, confidence, respuesta = predict_intent(text)
    return {
        "intent": intent,
        "confidence": confidence,
        "respuesta": respuesta
    }

