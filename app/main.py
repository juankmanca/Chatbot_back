from fastapi import FastAPI
from app.nlu.train import predict_intent

app = FastAPI(title="Chatbot Universitario - Backend")

# Diccionario de respuestas según la intención
RESPUESTAS = {
    "acceso_lms": "Parece que tienes problemas para acceder al LMS. Verifica que tu usuario y contraseña estén correctos. Si el problema persiste, intenta restablecer la contraseña desde la opción '¿Olvidaste tu clave?' en el portal.",
    "wifi_conexion": "Para problemas de conexión Wi-Fi, asegúrate de estar dentro del rango de cobertura y de usar las credenciales institucionales. Si aún no conecta, prueba olvidar la red y reconectarte.",
    "correo_institucional": "Si tienes problemas con el correo institucional, intenta acceder desde Outlook Web (https://outlook.office.com). Si olvidaste la contraseña, puedes restablecerla en el portal de cuentas.",
    "default": "No estoy completamente seguro de lo que necesitas. ¿Podrías darme más detalles o reformular tu consulta?"
}

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

