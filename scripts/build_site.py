"""
Injects data/processed/dataset.json into site/template.html
and writes the final standalone index.html at the project root.

Run: python3 scripts/build_site.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "site" / "template.html"
DATASET = ROOT / "data" / "processed" / "dataset.json"
OUT = ROOT / "index.html"


def main():
    template = TEMPLATE.read_text()
    dataset_json = DATASET.read_text()
    html = template.replace("__DATASET_JSON__", dataset_json)
    OUT.write_text(html)
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
