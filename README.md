# 📚 Daily Paper Library — Kumar Azad

> A personal digital library of research papers I read daily, organized by topic, date, and key findings.

[![Papers Read](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FKrAzad0%2Fdaily-paper-library%2Fmain%2Fpapers%2Findex.json&query=%24.total&label=Papers%20Read&color=blue)](papers/index.json)
[![Last Updated](https://img.shields.io/github/last-commit/KrAzad0/daily-paper-library?label=Last%20Updated&color=green)](https://github.com/KrAzad0/daily-paper-library/commits/main)

---

## 🗂️ Repository Structure

```
daily-paper-library/
├── README.md                    # This file — overview & index
├── papers/
│   ├── index.json               # Auto-updated master index of all papers
│   ├── YYYY-MM-DD_paper-slug.md # Individual paper notes
│   └── ...
├── topics/
│   ├── physics.md               # Topic index: Physics
│   ├── quantum-computing.md     # Topic index: Quantum Computing
│   ├── machine-learning.md      # Topic index: Machine Learning
│   ├── mathematics.md           # Topic index: Mathematics
│   └── ...
├── templates/
│   └── paper-template.md        # Template for adding a new paper
├── scripts/
│   └── update_index.py          # Script to auto-update index.json
└── .github/
    └── workflows/
        └── update-index.yml     # GitHub Actions: auto-update index on push
```

---

## 📖 How to Add a Paper

1. Copy `templates/paper-template.md`
2. Save it in `papers/` as `YYYY-MM-DD_paper-slug.md`
3. Fill in the fields: title, authors, link, topic tags, summary, key findings
4. Commit & push — GitHub Actions will auto-update `papers/index.json` and topic files

---

## 🔖 Topics Index

| Topic | Papers |
|-------|--------|
| [Physics](topics/physics.md) | ![Physics](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FKrAzad0%2Fdaily-paper-library%2Fmain%2Fpapers%2Findex.json&query=%24.topics.physics&label=papers&color=orange) |
| [Quantum Computing](topics/quantum-computing.md) | ![QC](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FKrAzad0%2Fdaily-paper-library%2Fmain%2Fpapers%2Findex.json&query=%24.topics.quantum-computing&label=papers&color=purple) |
| [Machine Learning](topics/machine-learning.md) | ![ML](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FKrAzad0%2Fdaily-paper-library%2Fmain%2Fpapers%2Findex.json&query=%24.topics.machine-learning&label=papers&color=red) |
| [Mathematics](topics/mathematics.md) | ![Math](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FKrAzad0%2Fdaily-paper-library%2Fmain%2Fpapers%2Findex.json&query=%24.topics.mathematics&label=papers&color=yellow) |

---

## 📅 Recent Papers

<!-- AUTO-UPDATED by GitHub Actions — do not edit below this line -->
<!-- PAPERS_START -->
*No papers added yet. Add your first paper using the template!*
<!-- PAPERS_END -->

---

## 📊 Stats

<!-- AUTO-UPDATED by GitHub Actions -->
<!-- STATS_START -->
- **Total papers read:** 0
- **Topics covered:** 4
- **Last paper added:** —
<!-- STATS_END -->

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/KrAzad0/daily-paper-library.git
cd daily-paper-library

# Install dependencies for the update script
pip install -r requirements.txt

# Add a new paper (fill in the template)
cp templates/paper-template.md papers/$(date +%Y-%m-%d)_my-paper.md
# Edit the file, then:
git add . && git commit -m "Add paper: [title]" && git push
```

---

*Made with ❤️ by [Kumar Azad](https://github.com/KrAzad0) | Physics · Mathematics · AI · Quantum Computing*
