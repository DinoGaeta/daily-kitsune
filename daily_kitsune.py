import os, json, hashlib, datetime
from news_sources import SOURCES
from fetch_news import fetch_entries, score_human_weight
from translate_summarize import to_italian, summarize_3points
from kitsune_style import kitsune_caption
from graphic_card import make_card

OUT_DIR = "out"
CACHE_FILE = "cache.json"

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return set()
    try:
        return set(json.load(open(CACHE_FILE, "r", encoding="utf-8")))
    except:
        return set()

def save_cache(cache_set):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(cache_set), f)

def pick_item(items, cache):
    """
    Ordina le notizie per 'peso umano' e prende la prima non già pubblicata.
    """
    ranked = sorted(items, key=score_human_weight, reverse=True)
    for it in ranked:
        uid = hashlib.md5((it["title"] + it["link"]).encode()).hexdigest()
        if uid not in cache:
            return it, uid
    return None, None

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    cache = load_cache()

    # Scarica notizie
    items = fetch_entries(SOURCES, max_per_feed=8)
    if not items:
        print("Nessuna notizia trovata.")
        return

    # Scegli la più 'umana'
    item, uid = pick_item(items, cache)
    if not item:
        print("Tutto già pubblicato.")
        return

    # Traduci titolo + contenuto
    title_it = to_italian(item["title"])
    text_raw = item["summary"] or item["title"]
    text_it = to_italian(text_raw)

    # Sintesi calma (voce Kitsune)
    points = summarize_3points(text_it, max_sentences=4)
    if not points:
        points = [text_it[:200] + "…"]

    caption = kitsune_caption(title_it, points, fonte=item["source"])

    # Genera filename
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    img_path = f"{OUT_DIR}/kitsune-{timestamp}.png"
    cap_path = f"{OUT_DIR}/kitsune-{timestamp}.txt"

    # Crea immagine
    make_card(title_it, points, img_path)

    # Salva caption
    with open(cap_path, "w", encoding="utf-8") as f:
        f.write(caption + "\n\n#DailyKitsune #attualità #mondo #umanità #notizie")

    # Aggiorna cache
    cache.add(uid)
    save_cache(cache)

    # Output percorso per automazione
    print(f"IMAGE_PATH={img_path}")
    print(f"CAPTION_PATH={cap_path}")

if __name__ == "__main__":
    main()
