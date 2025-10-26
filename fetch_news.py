import feedparser, re
from bs4 import BeautifulSoup

def fetch_entries(feeds, max_per_feed=8):
    """
    Scarica e normalizza articoli dai feed RSS selezionati.
    Restituisce una lista uniforme:
    { title, summary, link, source }
    """
    items = []
    for url in feeds:
        data = feedparser.parse(url)
        for entry in data.entries[:max_per_feed]:
            title = entry.get("title", "")
            raw_summary = entry.get("summary", entry.get("description", title))
            summary = BeautifulSoup(raw_summary, "html.parser").get_text(" ")
            link = entry.get("link", "")
            source = re.sub(r"https?://(www\.)?", "", url.split("/")[2])
            items.append({
                "title": title,
                "summary": summary,
                "link": link,
                "source": source
            })
    return items


def score_human_weight(item):
    """
    Punteggio che stima quanto una notizia abbia "peso umano".
    Più alto → più probabilità che meriti di essere pubblicata.
    """
    text = (item["title"] + " " + item["summary"]).lower()

    # parole che indicano rilevanza umana o sociale
    positive = [
        "diritt", "right", "ceasefire", "climat", "ambiente", "environment",
        "migraz", "migrant", "rifugi", "refugee", "health", "sanit", "osped",
        "tribunal", "court", "legge", "justice", "education", "school",
        "lavor", "work", "povert", "poverty"
    ]

    # parole che indicano gossip, polemica vuota, intrattenimento inutile
    negative = [
        "gossip", "celebr", "vip", "calciomercato", "trailer", "gaming",
        "tv show", "intrattenimento", "spettacolo"
    ]

    score = 0

    for w in positive:
        if w in text:
            score += 2

    for w in negative:
        if w in text:
            score -= 2

    # notizie più lunghe tendono a essere più sostanziali
    if len(item["summary"]) > 200:
        score += 1

    return score
