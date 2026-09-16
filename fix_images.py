import re
from pathlib import Path
from urllib.parse import unquote, quote

ROOT = Path(".")
IGNORE = {".git", "__pycache__", ".venv", "venv", "node_modules"}

def ignored(p: Path):
    return any(x in IGNORE for x in p.parts)

def encode_link(link: str):
    link = link.strip()

    if link.startswith(("http://", "https://", "data:")):
        return link

    decoded = unquote(link)
    return quote(decoded, safe="/.#-_")

def fix_md(path: Path):
    s = path.read_text(encoding="utf-8", errors="ignore")
    old = s

    # Sửa \![image](path) -> ![image](path)
    s = re.sub(
        r"\\!\[([^\]]*)\]\(([^)]+)\)",
        lambda m: f"![{m.group(1)}]({encode_link(m.group(2))})",
        s
    )

    # Sửa ![image](path) encode lại path cho an toàn
    s = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        lambda m: f"![{m.group(1)}]({encode_link(m.group(2))})",
        s
    )

    if s != old:
        path.write_text(s, encoding="utf-8")
        print("[FIX IMAGE MD]", path)

def check_images():
    print("\n=== CHECK BROKEN LOCAL IMAGES ===")
    broken = 0

    img_re = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")

    for md in ROOT.rglob("*.md"):
        if ignored(md):
            continue

        text = md.read_text(encoding="utf-8", errors="ignore")

        for line_no, line in enumerate(text.splitlines(), 1):
            for m in img_re.finditer(line):
                link = m.group(1).strip()

                if link.startswith(("http://", "https://", "data:")):
                    continue

                decoded = unquote(link)
                img_path = (md.parent / decoded).resolve()

                if not img_path.exists():
                    print(f"[BROKEN IMAGE] {md}:{line_no}: {link}")
                    broken += 1

    if broken == 0:
        print("[OK] Không thấy ảnh local bị hỏng.")
    else:
        print(f"[WARN] Có {broken} ảnh local bị hỏng.")

for md in ROOT.rglob("*.md"):
    if not ignored(md):
        fix_md(md)

check_images()
