import re
from deep_translator import GoogleTranslator
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.parsers.plaintext import PlaintextParser

translator = GoogleTranslator(source="auto", target="it")

def to_italian(text: str) -> str:
    """
    Traduzione pulita e robusta.
    """
    # euristica semplice: se sembra già italiano → non tradurre
    if re.search(r"\b(è|gli|della|delle|degli|nell[oa]|all[oa]|che|non|una|un|il|la)\b", text.lower()):
        return text
    try:
        return translator.translate(text)
    except:
        return text

def _simple_sentence_split(text: str) -> list[str]:
    """
    Divider frasi senza NLTK.
    Funziona bene per italiano ed inglese.
    """
    text = text.replace("\n", " ")
    return re.split(r'(?<=[.!?])\s+', text)

def summarize_3points(text_it: str, max_sentences=4) -> list[str]:
    """
    Sintesi calma → 3–4 frasi brevi, tono chiaro.
    Nessun uso di NLTK → compatibile con Railway.
    """
    try:
        sentences = _simple_sentence_split(text_it)
        sentences = sentences[:25]  # limita lunghezza input per stabilità
        reduced = " ".join(sentences)

        parser = PlaintextParser.from_string(reduced, lambda x: sentences)
        summarizer = TextRankSummarizer()
        summary = summarizer(parser.document, max_sentences)

        cleaned = []
        for s in summary:
            line = re.sub(r"\s+", " ", str(s)).strip()
            if line:
                cleaned.append(line)

        if cleaned:
            return cleaned

        return [text_it[:200] + "…"]

    except:
        return [text_it[:200] + "…"]


