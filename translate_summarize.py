import re
from deep_translator import GoogleTranslator
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

translator = GoogleTranslator(source="auto", target="it")

def to_italian(text: str) -> str:
    """
    Traduzione pulita, compatibile con Python 3.13,
    senza compilazioni e senza chiavi API.
    """
    # euristica: se già italiano → non toccare
    if re.search(r"\b(è|gli|della|delle|degli|nell[oa]|all[oa]|che|non)\b", text.lower()):
        return text
    try:
        return translator.translate(text)
    except:
        return text

def summarize_3points(text_it: str, max_sentences=4) -> list[str]:
    """
    Sintesi calma → 3–4 frasi chiare.
    """
    parser = PlaintextParser.from_string(text_it, Tokenizer("italian"))
    summarizer = TextRankSummarizer()
    sentences = summarizer(parser.document, max_sentences)

    cleaned = []
    for s in sentences:
        line = re.sub(r"\s+", " ", str(s)).strip()
        if line:
            cleaned.append(line)

    return cleaned

