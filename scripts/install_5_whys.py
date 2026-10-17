import os

step_base = "/Users/cattleya.c/.gemini/antigravity/brain/08b82cd2-ec1d-4762-a470-b2a1dad70e2e/.system_generated/steps"

files_map = {
    "SKILL.md": os.path.join(step_base, "85/content.md"),
    "references/toyota-origins.md": os.path.join(step_base, "86/content.md"),
    "references/software-patterns.md": os.path.join(step_base, "87/content.md"),
    "examples/production-incident.md": os.path.join(step_base, "88/content.md"),
    "examples/performance-regression.md": os.path.join(step_base, "89/content.md"),
}

targets = [
    "/Users/cattleya.c/.gemini/config/skills/5-whys",
    "/Users/cattleya.c/.gemini/antigravity/scratch/all_beauty/.agents/skills/5-whys",
]


def strip_header(text):
    # read_url_content prepends:
    # Title: Live Content\n\nDescription: Fetched live\n\nSource: ...\n\n---\n\n
    marker = "\n---\n\n"
    idx = text.find(marker)
    if idx != -1:
        return text[idx + len(marker) :]
    return text


for target_root in targets:
    for rel_path, src_file in files_map.items():
        with open(src_file, "r", encoding="utf-8") as f:
            raw = f.read()
        body = strip_header(raw)
        if rel_path == "SKILL.md":
            # Ensure lowercase hyphenated name in YAML frontmatter per Antigravity skill spec
            body = body.replace("name: 5-Whys Root Cause Analysis", "name: 5-whys", 1)
        dest_path = os.path.join(target_root, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "w", encoding="utf-8") as out:
            out.write(body)
        print(f"Installed: {dest_path} ({len(body)} bytes)")
