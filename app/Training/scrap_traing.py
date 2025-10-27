# ===============================
#  ETAPA 1: SCRAPING PREGUNTAS Y RESPUESTAS
# ===============================

!pip install beautifulsoup4 sentence-transformers > /dev/null

from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
import json, re, random
from pathlib import Path

INPUT = "/content/page.html"
OUTPUT = "/content/itm_faq.json"

def slugify(s, maxlen=60):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "_", s)
    return s[:maxlen].strip("_")

def clean_text(text: str) -> str:
    text = re.sub(r'\s*\n\s*', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def extract_text_from_tag(tag):
    parts = []
    for child in tag.children:
        if getattr(child, "name", None) in ("p","li"):
            txt = child.get_text(" ", strip=True)
            if txt:
                parts.append(txt)
        elif getattr(child, "name", None) in ("ul","ol"):
            for li in child.find_all("li"):
                txt = li.get_text(" ", strip=True)
                if txt:
                    parts.append(txt)
        elif getattr(child, "name", None) is None:
            t = str(child).strip()
            if t:
                parts.append(t)
    text = " ".join(parts)
    return clean_text(text)

html = Path(INPUT).read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

data = {"intents": []}
seen_questions = set()

for panel in soup.select(".vc_tta-panel"):
    panel_title = None
    title_text_el = panel.select_one(".vc_tta-title-text")
    if title_text_el:
        panel_title = title_text_el.get_text(strip=True)
    panel_id = panel.get("id") or panel_title or "sin_categoria"

    for toggle in panel.select(".vc_do_toggle, .vc_toggle"):
        q_el = toggle.select_one(".vc_toggle_title h2, .vc_custom_heading")
        a_el = toggle.select_one(".vc_toggle_content")
        if not q_el or not a_el:
            q_el = toggle.find(["h2","h3","h4"]) or q_el
        if not q_el or not a_el:
            continue

        question = q_el.get_text(" ", strip=True)
        if not question or question in seen_questions:
            continue
        seen_questions.add(question)

        answer = extract_text_from_tag(a_el) or a_el.get_text(" ", strip=True)

        intent_name = f"{slugify(panel_id,30)}_{slugify(question,40)}"
        examples = [question]
        responses = [clean_text(answer)]

        data["intents"].append({
            "name": intent_name,
            "examples": examples,
            "responses": responses
        })

# ===============================
#  ETAPA 2: ENRIQUECIMIENTO AUTOMÁTICO (PARAFRASIS)
# ===============================

from transformers import pipeline

# Usa un modelo multilingüe pequeño gratuito para generar variaciones
# (modelo paraphrase de huggingface)
paraphraser = pipeline(
    "text2text-generation",
    model="Vamsi/T5_Paraphrase_Paws",  # inglés base
    tokenizer="Vamsi/T5_Paraphrase_Paws"
)

def generate_paraphrases(text, num=3):
    """
    Genera hasta `num` variaciones del texto original.
    """
    try:
        outputs = paraphraser(
            f"paraphrase: {text} </s>", 
            num_return_sequences=num, 
            num_beams=10, 
            temperature=1.5,
            max_length=128
        )
        paras = [clean_text(o['generated_text']) for o in outputs]
        # filtrar duplicados o frases idénticas
        unique_paras = []
        for p in paras:
            if p.lower() != text.lower() and p not in unique_paras:
                unique_paras.append(p)
        return unique_paras
    except Exception:
        return []

# Enriquecer ejemplos
for intent in data["intents"]:
    base_q = intent["examples"][0]
    new_examples = generate_paraphrases(base_q, num=3)
    if new_examples:
        intent["examples"].extend(new_examples)

# ===============================
#  GUARDAR JSON FINAL
# ===============================

Path(OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Archivo enriquecido guardado con {len(data['intents'])} intents en {OUTPUT}")
