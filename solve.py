import re
from pathlib import Path
from urllib.parse import unquote, quote

DRY_RUN = False
ROOT = None

IGNORE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}

HASH_RE = re.compile(r"\s+[a-f0-9]{20,}(?=(_all)?(\.[a-zA-Z0-9]+)?$)", re.I)
HASH_ANYWHERE_RE = re.compile(r"\s+[a-f0-9]{20,}", re.I)


def safe_print(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(str(msg).encode("utf-8", errors="ignore").decode("utf-8"))


def is_ignored(path):
    return any(part in IGNORE_DIRS for part in path.parts)


def clean_stem(stem):
    stem = unquote(stem)
    stem = HASH_RE.sub("", stem)
    stem = HASH_ANYWHERE_RE.sub("", stem)
    stem = stem.replace("_all", "")
    stem = stem.replace("\u00a0", " ")
    stem = re.sub(r"\s+", " ", stem).strip()
    stem = stem.replace("–", "-").replace("—", "-")
    return stem or "untitled"


def clean_name(name):
    p = Path(name)
    return clean_stem(p.stem) + p.suffix.lower()


def unique_target(base_path, planned):
    target = base_path
    i = 1

    while target.exists() or str(target).lower() in planned:
        target = base_path.with_name(f"{base_path.stem} ({i}){base_path.suffix}")
        i += 1

    planned.add(str(target).lower())
    return target


def detect_root():
    if ROOT is not None:
        return Path(ROOT)

    current = Path(".")
    dirs = [p for p in current.iterdir() if p.is_dir() and not is_ignored(p)]

    best_dir = None
    best_count = 0

    for d in dirs:
        count = len(list(d.rglob("*.md")))
        if count > best_count:
            best_count = count
            best_dir = d

    return best_dir if best_dir is not None else current


def rename_files_and_folders(root):
    items = [p for p in root.rglob("*") if not is_ignored(p)]
    items = sorted(items, key=lambda x: len(x.parts), reverse=True)

    planned = set()

    for old in items:
        new_name = clean_name(old.name)

        if new_name == old.name:
            continue

        new_path = unique_target(old.with_name(new_name), planned)
        safe_print(f"[RENAME] {old} -> {new_path}")

        if not DRY_RUN:
            old.rename(new_path)


def clean_link_path(link):
    link = link.strip()

    if link.startswith(("http://", "https://", "mailto:", "#")):
        return link

    decoded = unquote(link)

    if "#" in decoded:
        path_part, anchor = decoded.split("#", 1)
        anchor = "#" + anchor
    else:
        path_part, anchor = decoded, ""

    parts = []

    for part in path_part.split("/"):
        if part:
            parts.append(clean_name(part))

    cleaned = "/".join(parts) + anchor
    return quote(cleaned, safe="/.#-_()")


def clean_md_content(content):
    # Case: [[**Title**](https://external)]\(local hash.md)
    pattern_nested_escaped = re.compile(
        r"\[\[(.*?)\]\(https?://[^)]+\)\]\\\(([^)]+)\)"
    )

    def repl_nested_escaped(m):
        label = m.group(1)
        local_link = m.group(2)

        inner_bold = re.search(r"\*\*([^*]+)\*\*", label)
        if inner_bold:
            label = f"**{inner_bold.group(1)}**"

        return f"[{label}]({clean_link_path(local_link)})"

    content = pattern_nested_escaped.sub(repl_nested_escaped, content)

    # Case: [text]\(local hash.md)
    pattern_escaped = re.compile(r"(?<!!)\[([^\]]+)\]\\\(([^)]+)\)")

    def repl_escaped(m):
        return f"[{m.group(1)}]({clean_link_path(m.group(2))})"

    content = pattern_escaped.sub(repl_escaped, content)

    # Case: [text](local hash.md)
    pattern_normal = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")

    def repl_normal(m):
        return f"[{m.group(1)}]({clean_link_path(m.group(2))})"

    content = pattern_normal.sub(repl_normal, content)
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip() + "\n"


def clean_markdown_files(root):
    for md in root.rglob("*.md"):
        if is_ignored(md):
            continue

        safe_print(f"[CLEAN MD] {md}")

        if not DRY_RUN:
            text = md.read_text(encoding="utf-8", errors="ignore")
            md.write_text(clean_md_content(text), encoding="utf-8")


def clean_root_markdown_files():
    for md in Path(".").glob("*.md"):
        if is_ignored(md):
            continue

        safe_print(f"[CLEAN ROOT MD] {md}")

        if not DRY_RUN:
            text = md.read_text(encoding="utf-8", errors="ignore")
            md.write_text(clean_md_content(text), encoding="utf-8")


def rename_root_md_to_readme(root):
    readme = Path("README.md")

    if readme.exists():
        safe_print("[README] README.md already exists, skip.")
        return

    md_files = [p for p in Path(".").glob("*.md") if p.is_file() and not is_ignored(p)]

    if not md_files:
        safe_print("[README] No root .md file found.")
        return

    root_name = clean_name(root.name).lower()
    chosen = None

    for md in md_files:
        if clean_name(md.name).lower() == f"{root_name}.md":
            chosen = md
            break

    if chosen is None:
        chosen = md_files[0]

    safe_print(f"[README] {chosen} -> README.md")

    if not DRY_RUN:
        chosen.rename(readme)


def build_file_lookup(root):
    lookup = {}
    files = []

    if root.exists():
        files.extend([p for p in root.rglob("*") if p.is_file() and not is_ignored(p)])

    files.extend([p for p in Path(".").glob("*.md") if p.is_file() and not is_ignored(p)])

    for p in files:
        key = clean_name(p.name).lower()
        lookup.setdefault(key, []).append(p)

    return lookup


def rel_link_from_to(src_md, target):
    try:
        rel = target.resolve().relative_to(src_md.parent.resolve())
    except Exception:
        try:
            rel = target.relative_to(src_md.parent)
        except Exception:
            rel = target

    rel_str = str(rel).replace("\\", "/")
    return quote(rel_str, safe="/.#-_()")


def fix_links_by_existing_files(root):
    lookup = build_file_lookup(root)

    md_files = []
    if root.exists():
        md_files.extend([p for p in root.rglob("*.md") if not is_ignored(p)])

    md_files.extend([p for p in Path(".").glob("*.md") if p.is_file() and not is_ignored(p)])

    seen = set()

    for md in md_files:
        if md in seen:
            continue
        seen.add(md)

        if not md.exists():
            continue

        safe_print(f"[FIX LINKS BY FILES] {md}")

        if DRY_RUN:
            continue

        text = md.read_text(encoding="utf-8", errors="ignore")

        def repl(m):
            label = m.group(1)
            link = m.group(2).strip()

            if link.startswith(("http://", "https://", "mailto:", "#")):
                return m.group(0)

            cleaned_link = clean_link_path(link)
            target_name = clean_name(Path(unquote(cleaned_link)).name).lower()
            candidates = lookup.get(target_name)

            if candidates:
                final_link = rel_link_from_to(md, candidates[0])
                return f"[{label}]({final_link})"

            return f"[{label}]({cleaned_link})"

        new_text = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", repl, text)

        if new_text != text:
            md.write_text(new_text, encoding="utf-8")


def remove_empty_dirs(root):
    dirs = [p for p in root.rglob("*") if p.is_dir() and not is_ignored(p)]
    dirs = sorted(dirs, key=lambda x: len(x.parts), reverse=True)

    for d in dirs:
        try:
            if not any(d.iterdir()):
                safe_print(f"[REMOVE EMPTY DIR] {d}")
                if not DRY_RUN:
                    d.rmdir()
        except Exception as e:
            safe_print(f"[ERROR REMOVE DIR] {d}: {e}")


def check_hash_names(root):
    safe_print("\n=== CHECK HASH IN FILE/FOLDER NAMES ===")

    found = False
    paths = []

    if root.exists():
        paths.extend([p for p in root.rglob("*") if not is_ignored(p)])

    paths.extend([p for p in Path(".").glob("*") if not is_ignored(p)])

    for p in paths:
        if re.search(r"[a-f0-9]{20,}", p.name, re.I):
            safe_print(f"[HASH NAME] {p}")
            found = True

    if not found:
        safe_print("[OK] Không còn hash trong tên file/folder.")


def check_hash_links(root):
    safe_print("\n=== CHECK HASH IN MARKDOWN LINKS ===")

    found = False
    md_files = []

    if root.exists():
        md_files.extend([p for p in root.rglob("*.md") if not is_ignored(p)])

    md_files.extend([p for p in Path(".").glob("*.md") if p.is_file() and not is_ignored(p)])

    seen = set()

    for md in md_files:
        if md in seen:
            continue
        seen.add(md)

        if not md.exists():
            continue

        text = md.read_text(encoding="utf-8", errors="ignore")

        for i, line in enumerate(text.splitlines(), start=1):
            has_hash = re.search(r"[a-f0-9]{20,}", line, re.I)
            looks_like_local_md_link = (
                ".md" in line
                and ("(" in line or "\\(" in line)
                and not line.strip().startswith("http")
            )

            if has_hash and looks_like_local_md_link:
                safe_print(f"[HASH LINK] {md}:{i}: {line[:220]}")
                found = True

    if not found:
        safe_print("[OK] Không còn hash trong link Markdown.")


def main():
    root = detect_root()

    if not root.exists():
        safe_print(f"[ERROR] Không tìm thấy ROOT: {root}")
        return

    safe_print("======================================")
    safe_print(" Notion Folder Export Cleaner")
    safe_print("======================================")
    safe_print(f"ROOT    = {root}")
    safe_print(f"DRY_RUN = {DRY_RUN}")

    safe_print("\n=== STEP 1: Rename files/folders ===")
    rename_files_and_folders(root)

    safe_print("\n=== STEP 2: Rename root md to README.md ===")
    rename_root_md_to_readme(root)

    safe_print("\n=== STEP 3: Clean markdown files ===")
    clean_markdown_files(root)

    safe_print("\n=== STEP 4: Clean root markdown files ===")
    clean_root_markdown_files()

    safe_print("\n=== STEP 5: Fix links by existing files ===")
    fix_links_by_existing_files(root)

    safe_print("\n=== STEP 6: Remove empty folders ===")
    remove_empty_dirs(root)

    check_hash_names(root)
    check_hash_links(root)

    safe_print("\nDONE.")

    if DRY_RUN:
        safe_print("\nĐang chạy thử DRY_RUN=True.")
        safe_print("Nếu log ổn, đổi DRY_RUN=False rồi chạy lại.")
    else:
        safe_print("\nĐã sửa thật. Có thể kiểm tra rồi push GitHub.")


if __name__ == "__main__":
    main()
