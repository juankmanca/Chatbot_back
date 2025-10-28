# Chatbot Universitario - Backend

Prototipo inicial del Chatbot Inteligente para Soporte Técnico Universitario.
Desarrollado en Python con FastAPI y un modelo simple de NLU basado en Naive Bayes.

## Ejecutar localmente

1. Crear entorno virtual
   ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1
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

📊 scikit-learn
Conjunto de herramientas para Machine Learning clásico en Python.
Incluye modelos de clasificación, regresión y procesamiento de texto.
👉 En tu chatbot se usa para entrenar el modelo que clasifica las intenciones del usuario (por ejemplo, distinguir entre “problemas de conexión” o “acceso al LMS”).

🧠 BeautifulSoup
Librería para analizar y extraer información de documentos HTML o XML.
Permite navegar la estructura del DOM, seleccionar etiquetas y limpiar texto de forma sencilla.
👉 En este proyecto se usa durante la etapa de scraping, donde se extraen preguntas y respuestas desde una página HTML institucional para generar automáticamente el conjunto de datos.
Los pasos realizados con BeautifulSoup son:

Leer el archivo HTML con el contenido de las preguntas frecuentes.
Identificar las secciones, títulos y respuestas dentro del DOM.
Limpiar el texto de etiquetas y espacios innecesarios.
Generar un JSON estructurado con intents, examples y responses que luego alimenta el modelo de clasificación.
