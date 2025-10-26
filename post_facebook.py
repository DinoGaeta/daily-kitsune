import requests

PAGE_ID = "853986721129027"   # <-- QUI il tuo ID pagina
PAGE_ACCESS_TOKEN = "EAATTByA5EUMBP4PhWhcQ2vT3HX7GPRarWiWV5abTSNdyebXo46SLLOWGDGqucXEV03v07LIMGkfai81fguszCInKihhFVtDfOmKSc68R2zloNkkc0Vg9shA01M4c9JbLmW3HnKVZAqF2NsZBmavUQZBXfUDp4RIhoPjs5qkaMm7yX0Yy9ZC70X8XWFWnQesIsFNF"  # <-- QUI il tuo token pagina

def post_image_to_facebook(image_path, caption):
    url = f"https://graph.facebook.com/{PAGE_ID}/photos"
    payload = {
        "caption": caption,
        "access_token": PAGE_ACCESS_TOKEN
    }
    files = {
        "source": open(image_path, "rb")
    }
    response = requests.post(url, data=payload, files=files)
    print("Risposta Facebook:", response.text)
