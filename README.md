# Chatbot Universitario - Backend

Prototipo inicial del Chatbot Inteligente para Soporte Técnico Universitario.
Desarrollado en Python con FastAPI y un modelo simple de NLU basado en Naive Bayes.

## Ejecutar localmente

1. Crear entorno virtual
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Instalar dependencias
   ```bash
   pip install -r requirements.txt
   python -m spacy download es_core_news_md
   ```

3. Iniciar servidor
   ```bash
   uvicorn app.main:app --reload
   ```

4. Probar API en: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Documentación de las librerias utilizadas

🧩 fastapi

Framework moderno y rápido para construir APIs web en Python.
Permite crear endpoints REST de forma sencilla, con validación automática de datos y una interfaz interactiva (/docs).
👉 En tu chatbot, se usa para exponer el servicio que recibe los mensajes del usuario y devuelve la respuesta del bot.

⚡ uvicorn

Servidor web ligero y asíncrono compatible con FastAPI.
Se encarga de ejecutar la API y manejar las peticiones HTTP.
👉 Es el motor que “levanta” tu backend y permite acceder a él desde el navegador o el frontend (por ejemplo, http://127.0.0.1:8000).

🧠 spacy

Librería avanzada de Procesamiento de Lenguaje Natural (PLN).
Permite analizar texto en español, identificar sustantivos, verbos, entidades (como nombres o lugares), y mucho más.
👉 En tu proyecto puede ayudar al modelo NLU a comprender mejor el lenguaje humano y extraer información relevante de las consultas.

📊 scikit-learn

Conjunto de herramientas para Machine Learning clásico en Python.
Incluye modelos de clasificación, regresión y procesamiento de texto.
👉 En tu chatbot se usa para entrenar el modelo que clasifica las intenciones del usuario (por ejemplo, distinguir entre “problemas de conexión” o “acceso al LMS”).

🧾 pandas

Librería para el manejo y análisis de datos estructurados (tablas).
Permite leer, limpiar, transformar y analizar datos fácilmente.
👉 En tu proyecto puede servir para gestionar datasets de entrenamiento (por ejemplo, históricos de tickets de soporte o logs de conversación).