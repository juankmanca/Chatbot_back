from fastapi import FastAPI
from app.nlu.train import predict_intent

app = FastAPI(title="Chatbot Universitario - Backend")

@app.get("/")
def root():
    return {"message": "API activa"}

@app.post("/predict/")
def get_intent(user_input: dict):
    text = user_input.get("message", "")
    intent, confidence, respuesta, sugerencias = predict_intent(text)

    if confidence < 0.5:
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


