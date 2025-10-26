import os, json, hashlib, datetime, requests
from news_sources import SOURCES
from fetch_news import fetch_entries, score_human_weight
from translate_summarize import to_italian, summarize_3points
from kitsune_style import kitsune_caption
from graphic_card import make_card

# ✨ IMPOSTAZIONI
OUT_DIR = "out"
CACHE_FILE = "cache.json"

# 🟢 INSERISCI QUI I TUOI DATI
PAGE_ID = "853986721129027"   # <<< METTI QUI L'ID DELLA PAGINA
PAGE_ACCESS_TOKEN = "EAATTByA5EUMBP4PhWhcQ2vT3HX7GPRarWiWV5abTSNdyebXo46SLLOWGDGqucXEV03v07LIMGkfai81fguszCInKihhFVtDfOmKSc68R2zloNkkc0Vg9shA01M4c9JbLmW3HnKVZAqF2NsZBmavUQZBXfUDp4RIhoPjs5qkaMm7yX0Yy9ZC70X8XWFWnQesIsFNF"  # <<< METTI QUI IL TOKEN PAGINA

def post_image_to_facebook(image_path, caption):
    """
    Pubblica immagine + testo sulla Pagina Facebook
    """
    url = f"https://graph.facebook.com/{PAGE_ID}/photos"
    payload = {
        "caption": caption,
        "access_token": PAGE_ACCESS_TOKEN
    }
    files = {
        "source": open(image_path, "rb")
    }
    r = requests.post(url, data=payload, files=files)
    print("\n📡 Risposta Facebook:", r.text, "\n")

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
    ranked = sorted(items, key=score_human_weight, reverse=True)
    for it in ranked:
        uid = hashlib.md5((it["title"] + it["link"]).encode()).hexdigest()
        if uid not in cache:
            return it, uid
    return None, None

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    cache = load_cache()

    items = fetch_entries(SOURCES, max_per_feed=8)
    if not items:
        print("Nessuna notizia trovata.")
        return

    item, uid = pick_item(items, cache)
    if not item:
        print("Tutto già pubblicato.")
        return

    title_it = to_italian(item["title"])
    text_raw = item["summary"] or item["title"]
    text_it = to_italian(text_raw)

    points = summarize_3points(text_it, max_sentences=4)
    if not points:
        points = [text_it[:200] + "…"]

    caption = kitsune_caption(title_it, points, fonte=item["source"])
    caption += "\n\n#DailyKitsune #attualità #mondo #umanità #notizie"

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    img_path = f"{OUT_DIR}/kitsune-{timestamp}.png"

    make_card(title_it, points, img_path)

    # ✅ PUBBLICA
    post_image_to_facebook(img_path, caption)

    cache.add(uid)
    save_cache(cache)

    print("✅ Pubblicato!")

if __name__ == "__main__":
    main()
