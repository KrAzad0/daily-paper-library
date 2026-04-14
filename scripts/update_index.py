#!/usr/bin/env python3
"""
update_index.py

Automatically scans all paper markdown files in papers/,
parses their YAML front matter, and updates:
  - papers/index.json  (master machine-readable index)
  - README.md          (Recent Papers & Stats sections)
  - topics/*.md        (per-topic paper tables)

Run by GitHub Actions on every push to main.
"""

import json
import os
import re
from datetime import date, datetime
from pathlib import Path

import yaml  # pip install pyyaml

ROOT = Path(__file__).parent.parent
PAPERS_DIR = ROOT / "papers"
TOPICS_DIR = ROOT / "topics"
INDEX_FILE = PAPERS_DIR / "index.json"
README_FILE = ROOT / "README.md"

TOPIC_EMOJI = {
    "physics": "⚗️",
    "quantum-computing": "⚛️",
    "machine-learning": "🤖",
    "mathematics": "∑",
    "general": "📚",
}

TOPIC_FILE_MAP = {
    "physics": TOPICS_DIR / "physics.md",
    "quantum-computing": TOPICS_DIR / "quantum-computing.md",
    "machine-learning": TOPICS_DIR / "machine-learning.md",
    "mathematics": TOPICS_DIR / "mathematics.md",
}

TOPIC_MARKER = {
    "physics": ("PHYSICS_PAPERS_START", "PHYSICS_PAPERS_END"),
    "quantum-computing": ("QC_PAPERS_START", "QC_PAPERS_END"),
    "machine-learning": ("ML_PAPERS_START", "ML_PAPERS_END"),
    "mathematics": ("MATH_PAPERS_START", "MATH_PAPERS_END"),
}


def parse_paper(filepath: Path) -> dict | None:
    """Parse YAML front matter from a paper markdown file."""
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None
    meta["filename"] = filepath.name
    meta["path"] = f"papers/{filepath.name}"
    return meta


def build_index(papers: list[dict]) -> dict:
    """Build the master index dictionary."""
    topics_count: dict[str, int] = {}
    for p in papers:
        for t in (p.get("topics") or []):
            topics_count[t] = topics_count.get(t, 0) + 1

    last_date = max((p.get("date", "") or "" for p in papers), default="")
    return {
        "total": len(papers),
        "last_updated": str(date.today()),
        "last_paper": str(last_date),
        "topics": topics_count,
        "papers": [
            {
                "title": p.get("title", "Untitled"),
                "date": str(p.get("date", "")),
                "authors": p.get("authors", []),
                "source": p.get("source", ""),
                "topics": p.get("topics", []),
                "status": p.get("status", "completed"),
                "rating": p.get("rating", ""),
                "path": p.get("path", ""),
            }
            for p in sorted(papers, key=lambda x: str(x.get("date", "")), reverse=True)
        ],
    }


def replace_between_markers(text: str, start: str, end: str, new_content: str) -> str:
    """Replace content between HTML comment markers."""
    pattern = rf"(<!-- {re.escape(start)} -->).*?(<!-- {re.escape(end)} -->)"
    replacement = rf"\1\n{new_content}\n\2"
    return re.sub(pattern, replacement, text, flags=re.DOTALL)


def update_readme(papers: list[dict]) -> None:
    """Update README.md with recent papers and stats."""
    readme = README_FILE.read_text(encoding="utf-8")

    # Recent papers table (last 10)
    recent = sorted(papers, key=lambda x: str(x.get("date", "")), reverse=True)[:10]
    if recent:
        rows = ["| Date | Title | Topics | Rating |",
                "|------|-------|--------|--------|"]
        for p in recent:
            title = p.get("title", "Untitled")
            path = p.get("path", "")
            d = str(p.get("date", ""))
            topics = " ".join(f"`{t}`" for t in (p.get("topics") or []))
            rating = p.get("rating", "")
            rows.append(f"| {d} | [{title}]({path}) | {topics} | {rating} |")
        papers_block = "\n".join(rows)
    else:
        papers_block = "*No papers added yet. Add your first paper using the template!*"

    readme = replace_between_markers(readme, "PAPERS_START", "PAPERS_END", papers_block)

    # Stats
    total = len(papers)
    last_paper = max((str(p.get("date", "")) for p in papers), default="—")
    topics_set = set(t for p in papers for t in (p.get("topics") or []))
    stats_block = (f"- **Total papers read:** {total}\n"
                   f"- **Topics covered:** {len(topics_set)}\n"
                   f"- **Last paper added:** {last_paper}")
    readme = replace_between_markers(readme, "STATS_START", "STATS_END", stats_block)

    README_FILE.write_text(readme, encoding="utf-8")
    print(f"Updated README.md ({total} papers)")


def update_topic_file(topic: str, papers: list[dict]) -> None:
    """Update a topic markdown file with papers tagged under that topic."""
    topic_file = TOPIC_FILE_MAP.get(topic)
    if not topic_file or not topic_file.exists():
        return

    topic_papers = [p for p in papers if topic in (p.get("topics") or [])]
    topic_papers.sort(key=lambda x: str(x.get("date", "")), reverse=True)

    start_marker, end_marker = TOPIC_MARKER[topic]

    if topic_papers:
        rows = []
        for i, p in enumerate(topic_papers, 1):
            title = p.get("title", "Untitled")
            path = p.get("path", "")
            authors = ", ".join(p.get("authors") or [])
            d = str(p.get("date", ""))
            rating = p.get("rating", "")
            source = p.get("source", "")
            rows.append(f"| {i} | {d} | [{title}]({path}) | {authors} | {rating} | [Link]({source}) |")
        table_block = "\n".join(rows)
    else:
        table_block = "| - | - | *No papers yet* | - | - | - |"

    text = topic_file.read_text(encoding="utf-8")
    text = replace_between_markers(text, start_marker, end_marker, table_block)
    topic_file.write_text(text, encoding="utf-8")
    print(f"Updated topics/{topic}.md ({len(topic_papers)} papers)")


def main():
    print("Scanning papers directory...")
    papers = []
    for md_file in PAPERS_DIR.glob("*.md"):
        meta = parse_paper(md_file)
        if meta:
            papers.append(meta)
            print(f"  Parsed: {md_file.name}")

    print(f"Found {len(papers)} paper(s)")

    # Update index.json
    index = build_index(papers)
    INDEX_FILE.write_text(json.dumps(index, indent=2, default=str), encoding="utf-8")
    print(f"Written papers/index.json")

    # Update README.md
    update_readme(papers)

    # Update topic files
    for topic in TOPIC_FILE_MAP:
        update_topic_file(topic, papers)

    print("Done!")


if __name__ == "__main__":
    main()
