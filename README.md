# 🎵 Comeback Momentum & Fandom Intensity Analysis
### South Korea Top 40 Spotify Playlist | Atlantic Recording Corporation

---

## 📌 Project Overview
This project performs an end-to-end Exploratory Data Analysis and Momentum Intelligence study
on South Korea's Top 40 Spotify daily chart data (2023–2024), commissioned by
Atlantic Recording Corporation.

The goal is to uncover **which artists dominate through fandom-driven chart re-entries**,
how strong their comeback momentum is, and how long it lasts —
insights that directly inform Atlantic's K-Pop release and promotion strategy.

---

## 🎯 Problem Statement
Despite having daily Top 40 playlist data, Atlantic lacked insights into:
- Which songs experience multiple chart re-entries
- How strong comeback momentum differs from organic popularity
- How long momentum spikes last after re-entry
- Whether singles or albums benefit more from fandom-driven pushes
- How explicit content behaves in a fandom-centric market

---

## 📁 Project Structure
atlantic-south-korea-project/
│
├── data/
│   ├── Atlantic_South_Korea.csv        ← Original raw dataset (never modified)
│   ├── cleaned_data.csv                ← After cleaning (dtype fix, dedup)
│   ├── df_with_momentum.csv            ← With momentum scores added
│   ├── reentry_analysis.csv            ← Re-entry detection results
│   ├── fandom_scores.csv               ← Fandom intensity scores
│   └── retention_analysis.csv          ← Post-comeback retention data
│
├── notebooks/
│   ├── 01_data_inspection.ipynb        ← Load, understand, document
│   ├── 02_data_cleaning.ipynb          ← Fix dtypes, nulls, duplicates
│   ├── 03_eda_analysis.ipynb           ← Core EDA + 6 analyses
│   └── 04_reentry_momentum_analysis.ipynb ← Advanced momentum + fandom
│
├── plots/                              ← All saved visualisations (8 plots)
├── reports/
│   └── Research_Paper.pdf             ← Full research paper
├── app.py                             ← Streamlit dashboard
├── requirements.txt
└── README.md

---

## 📊 Dataset
| Field | Value |
|---|---|
| Source | Atlantic Recording Corporation / Spotify API |
| Period | January 2023 – December 2024 |
| Records | 27,784 rows |
| Columns | 10 (date, position, song, artist, popularity, duration_ms, album_type, total_tracks, is_explicit, album_cover_url) |
| Chart Type | South Korea Spotify Top 40 Daily |

---

## 🔬 Methodology
### Phase 1 — Data Inspection
Loaded and documented all 10 columns, verified shape, dtypes, date range, and uniqueness.

### Phase 2 — Data Cleaning
- Converted `date` to datetime64
- Converted `duration_ms` to `duration_min`
- Dropped non-analytical `album_cover_url`
- Removed 16 duplicate rows
- Result: 27,784 clean records, 0 nulls

### Phase 3 — Exploratory Data Analysis
6 core analyses covering popularity distribution, artist dominance,
album type comparison, time trends, explicit content, and correlations.

### Phase 4 — Advanced Momentum Analysis
- Chart re-entry detection (gap > 7 days = re-entry)
- Momentum Spike Score (popularity + rank jump composite)
- Post-comeback retention measurement
- Fandom Intensity Proxy Score (re-entry + spike + recovery)

---

## 🏆 Key Findings
1. **Korean artists dominate frequency** — Lim Young Woong (4,801 appearances), Jimin (4,359)
2. **Western artists lead popularity** — Mariah Carey (99.8), Jack Harlow (99.0)
3. **Singles outperform albums** — higher chart frequency AND higher avg popularity
4. **Explicit songs score 7 points higher** — 83.14 vs 76.27 despite being only 9.5% of chart
5. **111 songs experienced re-entry** — confirming active fandom-driven comeback cycles
6. **Avg post-comeback retention: 20.2 days** — fandom momentum is real but short-lived

---

## 🚀 Live Dashboard
🔗 https://atlantic-south-korea-project-ldvckytufaupvymswvucb3.streamlit.app/

---

## ⚙️ How to Run Locally
```bash
git clone https://github.com/yourusername/atlantic-south-korea-project
cd atlantic-south-korea-project
pip install -r requirements.txt
streamlit run app.py
```

---

## 📦 Requirements
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
streamlit>=1.12.0
jupyter>=1.0.0
