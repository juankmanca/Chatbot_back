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
    intent = clf.predict(X_test)[0]
    confidence = max(clf.predict_proba(X_test)[0])
    
    # Buscar respuestas del intent detectado
    for i in data["intents"]:
        if i["name"] == intent:
            respuesta = random.choice(i["responses"])
            break
    else:
        respuesta = "Lo siento, no entiendo bien tu consulta. ¿Podrías reformularla?"

    return intent, round(confidence, 3), respuesta
