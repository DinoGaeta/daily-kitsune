import io, requests, textwrap
from PIL import Image, ImageDraw, ImageFont
from config import *

def load_font(url, size):
    """
    Scarica il font da URL e lo carica in memoria (niente installazioni esterne).
    """
    try:
        ttf = requests.get(url, timeout=20).content
        return ImageFont.truetype(io.BytesIO(ttf), size)
    except Exception:
        # fallback: usa font di default se richiesto
        return ImageFont.load_default()

def make_card(title: str, body_lines: list[str], outfile: str):
    """
    Genera post 1080x1350 stile Daily Kitsune:
    - sfondo panna
    - testo nero morbido
    - accento terracotta
    - ritmo spaziale (respiro)
    """
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title = load_font(FONT_TITLE_URL, TITLE_SIZE)
    font_body  = load_font(FONT_TEXT_URL, BODY_SIZE)
    font_meta  = load_font(FONT_TEXT_URL, META_SIZE)

    margin = 90
    x = margin
    y = margin

    # Header piccolissimo, identità silenziosa
    draw.text((x, y), "🦊 DAILY KITSUNE", fill=COLOR_TEXT, font=font_meta)
    y += 120

    # Titolo evocativo — va centrato leggermente "alto"
    wrapped_title = textwrap.fill(title, width=18)
    draw.text((x, y), wrapped_title, fill=COLOR_TEXT, font=font_title)
    y += (TITLE_SIZE + 25) * (1 + wrapped_title.count("\n"))

    # Respiro visivo
    y += 30
    draw.line([(x, y), (CANVAS_W - margin, y)], fill=COLOR_LINE, width=2)
    y += 70

    # Corpo — max 6 righe
    wrapped_body = textwrap.fill("\n".join(body_lines), width=32)
    draw.text((x, y), wrapped_body, fill=COLOR_TEXT, font=font_body)

    # Dettaglio identitario nell'angolo (morbido)
    draw.rectangle([CANVAS_W - 50, 0, CANVAS_W, 50], fill=COLOR_ACC)

    img.save(outfile, format="PNG", optimize=True)
