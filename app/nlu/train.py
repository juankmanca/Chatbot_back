import json
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def load_data():
    with open("app/data/itm_faq_V2.json", encoding="utf-8") as f:
        return json.load(f)

data = load_data()
vectorizer = CountVectorizer()
clf = MultinomialNB()

texts, labels = [], []
for intent in data["intents"]:
    for example in intent["examples"]:
        texts.append(example)
        labels.append(intent["name"])

X = vectorizer.fit_transform(texts)
clf.fit(X, labels)

def predict_intent(text):
    X_test = vectorizer.transform([text])
    proba = clf.predict_proba(X_test)[0]
    intent_idx = proba.argmax()
    intent = clf.classes_[intent_idx]
    confidence = proba[intent_idx]

    sugerencias = []
    if confidence < 0.5:
        # Obtiene los 3 intents más probables
        top_indices = proba.argsort()[::-1][:3]
        top_intents = [clf.classes_[i] for i in top_indices]

        # Busca los primeros ejemplos de cada intent
        for intent_name in top_intents:
            for i in data["intents"]:
                if i["name"] == intent_name:
                    ejemplo = i["examples"][0] if i["examples"] else intent_name
                    sugerencias.append(ejemplo)
                    break

    # Buscar respuesta normal del intent detectado
    respuesta = "Lo siento, no entiendo bien tu consulta. ¿Podrías reformularla?"
    for i in data["intents"]:
        if i["name"] == intent:
            respuesta = random.choice(i["responses"])
            break

    return intent, round(confidence, 3), respuesta, sugerencias
