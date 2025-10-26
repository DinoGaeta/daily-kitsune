def kitsune_caption(title_it: str, points_it: list[str], fonte: str) -> str:
    lines = []
    lines.append("🦊 DAILY KITSUNE\n")
    lines.append(title_it.strip())
    lines.append("")
    for p in points_it[:4]:
        lines.append(p.strip())
    lines.append("")
    lines.append(f"🌍 Fonte: {fonte}")
    return "\n".join(lines)
