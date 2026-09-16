from pathlib import Path
from urllib.parse import unquote, quote
import re

IGNORE = {".git", "__pycache__", ".venv", "venv", "node_modules"}

HASH_RE = re.compile(r"\s+[a-f0-9]{20,}(?=(_all)?(\.[a-zA-Z0-9]+)?$)", re.I)
HASH_ANYWHERE_RE = re.compile(r"\s+[a-f0-9]{20,}", re.I)

def ignored(p):
    return any(x in IGNORE for x in p.parts)

def clean_part(part):
    part = unquote(part)
    p = Path(part)

    stem = p.stem
    suffix = p.suffix

    stem = HASH_RE.sub("", stem)
    stem = HASH_ANYWHERE_RE.sub("", stem)
    stem = stem.replace("_all", "")
    stem = stem.replace("\u00a0", " ")
    stem = re.sub(r"\s+", " ", stem).strip()

    return stem + suffix.lower()

def clean_img_link(link):
    link = link.strip()

    if link.startswith(("http://", "https://", "data:")):
        return link

    decoded = unquote(link)

    parts = []
    for part in decoded.split("/"):
        if part.strip():
            parts.append(clean_part(part))

    cleaned = "/".join(parts)

    # Không cho dấu ngoặc () nằm raw trong URL vì Markdown dễ vỡ
    return quote(cleaned, safe="/.#-_")

fixed = 0

for md in Path(".").rglob("*.md"):
    if ignored(md):
        continue

    lines = md.read_text(encoding="utf-8", errors="ignore").splitlines()
    new_lines = []
    changed = False

    for line in lines:
        # Bắt nguyên dòng ảnh, dùng greedy để không bị cụt bởi dấu )
        m = re.match(r"^\\?!\[([^\]]*)\]\((.*)\)\s*$", line)

        if not m:
            new_lines.append(line)
            continue

        alt = m.group(1)
        link = m.group(2)

        new_link = clean_img_link(link)
        new_line = f"![{alt}]({new_link})"

        if new_line != line:
            changed = True

        new_lines.append(new_line)

    if changed:
        md.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print("[FIX IMAGE LINK]", md)
        fixed += 1

print("fixed md files:", fixed)
