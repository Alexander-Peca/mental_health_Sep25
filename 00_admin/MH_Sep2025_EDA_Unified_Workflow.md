
# MH_Sep2025_EDA — Unified Workflow (Single Source of Truth)
**Date:** 2025-10-22  
**Owner:** Alex (Mental Health EDA Project)  
**Scope:** End‑to‑end workflow for the MH_Sep2025 project, unifying previous drafts into one concise, operational guide. This is intentionally *tool‑agnostic* with light Python guidance (no heavy code). Use it as a checklist you can run top‑to‑bottom.

---

## 0) Project Intent & Success Criteria
**Intent:** Rehearse a professional EDA on a pre/post mental‑health dataset to build portfolio evidence and a reusable pipeline for future longitudinal gigs (t0/t1/t2).  
**Primary success:** A reproducible repo with clean data, clear descriptives, pre→post inference, at least two polished plots, and a short executive summary (HTML/PDF).  
**Stretch success:** Subgroup tests + a dose–response exploratory, optional simulated t2 to validate RM‑ANOVA/LMM paths.

**Key outcomes (examples):**
- Mental Health Literacy (MHL) total + subscales (KMHP, EBS, FASHSB, SHS)
- MHSAS, SSE, SSOSH, ATSPPH, SPANE_P, SPANE_N

---

## 1) Repository Scaffold (What lives where)
- `00_admin/` – briefs, notes, meeting docs
- `01_data/`
  - `raw/` – untouched CSVs (e.g., `mental_health_data.csv`, codebook)
  - `interim/` – temporary outputs during cleaning
  - `processed/` – final analysis‑ready data (`clean.csv`, and optional `clean_sim.csv`)
- `02_notebooks/` – analysis notebooks (e.g., `01_eda_report.ipynb`)
- `03_src/` – project package (`mh/`): `paths.py`, `io.py`, `viz.py`, `stats.py`, `utils.py`
- `04_outputs/` – tables ready for reporting (csv/md)
- `05_results/`
  - `figures/` – saved PNGs
  - `tables/` – summary tables (e.g., `kpi_summary.csv`, `tests_prepost.csv`)
- `06_reports/` – intermediate write‑ups (md/mdx)
- `05_deliverables/` – weekly bundles (HTML report + images + exec summary)
- `07_deploy/` – optional app/export later
- Root: `environment.yml`, `pyproject.toml`, `.gitignore`, `README.md`, `DATA.md`

**Light Python guide:**  
- Keep paths centralized in `mh/paths.py` and always use helpers from `mh/io.py` for reading/writing.  
- Never overwrite files in `raw/`. Anything modified goes to `interim/` or `processed/`.

---

## 2) Environment & Repro
- Create/activate the conda env from `environment.yml`.  
- Register a Jupyter kernel for the env.  
- Add a `repro.log` line in `05_results/` with: Python version, main lib versions, commit hash, and data timestamps.

**Light Python guide:** print versions with `import sys, pandas as pd; print(sys.version); print(pd.__version__)` and write to file.

---

## 3) Intake & Structural Triage (A‑block)
**Goal:** Understand schema, enforce types, normalize names — *then* examine missingness.

**Checklist:**
1. **Load raw** → `df_raw`, `codebook`
2. **Head & shape** → sanity glimpse of columns/prefixes
3. **Dtypes & non‑null** → `df.info()`
4. **Describe numerics** → `df.describe()`
5. **Missingness** → `df.isna().sum()` (sorted)
6. **Unique counts** → `df.nunique()`; spot IDs/constant or high‑cardinality cols
7. **Duplicates** → `df.duplicated().sum()`

**Type enforcement:**
- `Age` → numeric; `Gender` → category  
- Likert items → numeric (coerce errors), retain original as backup if needed

**Normalization:**
- Use machine‑friendly snake_case (e.g., `pre.MHL_KMHP` → `pre_kmhp`)  
- Keep human‑readable labels in a dict from the codebook for plots/reports

**Save:** `01_data/interim/triage_snapshot/` → `raw_descriptives.csv`, `missing_summary.csv`

---

## 4) Cleaning Decisions (A‑block continued)
**Missing data policy (default):**
- **Demographics:** if few missing, drop; else impute Age (mean/median) and set Gender to ‘Unknown’
- **Paired outcomes:** for **paired t‑tests**, drop rows missing either pre or post for that outcome
- For **LMM**, you can retain partial rows (model handles some missingness)

**Outliers:** flag via IQR or z>3 (document; only winsorize if they distort summaries)

**Save cleaned:** `01_data/processed/clean.csv` and log: raw N → cleaned N, and % with complete pre/post pairs.

---

## 5) Descriptives (B‑block)
**Demographics table:** N, mean(SD) Age; Gender counts/%; add education if present.  
**Outcomes table:** For each outcome, report **pre mean (SD)**, **post mean (SD)**, and **Δ = post–pre**.

**Plots (pick 2–3 for portfolio):**
- Distribution at pre/post (hist/box/violin)
- Paired spaghetti (subset n≈30) or dumbbell plot for the primary endpoint

**Save:**  
- `05_results/tables/kpi_summary.csv`  
- `05_results/figures/…png`

---

## 6) Primary Inference (C‑block)
**Default path:** Paired t‑test per outcome (pre vs post). Report t, p, 95% CI of mean diff, and Cohen’s d_rm (or Hedges g).  
**Upgrade path:** Prepare RM‑ANOVA and LMM interfaces so the same functions work when a real `t2` exists.

**Light Python guide (concept):**
- Reshape to long if using RM‑ANOVA/LMM (`id`, `time`, `value`)  
- Model examples (no code here):  
  - RM‑ANOVA: repeated measure on `time` within `id`, GG correction  
  - LMM: `value ~ time + (1|id)`; extend with `+ age + gender`

**Save:** `05_results/tables/tests_prepost.csv` (+ compact Markdown table for reports).

---

## 7) Subgroups (D‑block)
**Define:** Age (< median vs ≥ median), Gender (if counts allow), Baseline severity (tertiles of `pre_primary`).  
**Run:** Paired tests inside each subgroup; check interaction with time via ANCOVA/LMM.

**Save:** `05_results/tables/tests_subgroups.csv` + one subgroup plot with 95% CIs.

---

## 8) Exploratory Dose–Response (E‑block)
**Idea:** Does more “usage” relate to greater improvement?  
**If usage not available:** pick a proxy (e.g., `GPT_Use` categories) to rehearse the analysis; swap for true usage later.

**Analysis:** Δ(primary) ~ usage (ANOVA/trend); also correlation if usage is numeric.  
**Save:** `05_results/tables/usage_effects.csv` + one plot.

---

## 9) Optional t2 Simulation (F‑block)
**Purpose:** Validate the 3‑timepoint pipeline before you have a real follow‑up.  
**Method:** Create a clearly labeled **synthetic** `t2 = post + ε` (maintenance/decay + noise), save as `clean_sim.csv`.  
**Run:** RM‑ANOVA/LMM over `time ∈ {pre, post, t2}`.  
**Label all outputs “SIMULATION”.**

---

## 10) Reporting & Portfolio Evidence (G‑block)
**Notebook:** `02_notebooks/01_eda_report.ipynb` with narrative sections:  
1) *Question* → 2) *Method* → 3) *Result* → 4) *Figure* → 5) *Takeaway* (one line)

**Deliverables bundle:**  
- HTML export of the notebook → `05_deliverables/weekX/eda_report.html`  
- Tables (`kpi_summary.csv`, `tests_prepost.csv`, …)  
- Figures (PNG)  
- `EXEC_SUMMARY.md` (≤1 page, 5 bullets) — also your LinkedIn post scaffold

**Versioning:** Commit, tag (`v0.1-eda`), push.

---

## 11) Quality Gates (Definition of Done)
- [ ] Cleaning log present; `clean.csv` reproducible from raw via notebook/scripts  
- [ ] Descriptives match expectations; no impossible values  
- [ ] At least **2 plots** saved and labeled with readable axes (using codebook labels)  
- [ ] Primary tests table complete with effect sizes and CIs  
- [ ] Subgroup and exploratory either completed or explicitly deferred  
- [ ] Executive summary shipped; repo tagged

---

## 12) Lightweight Operating Rhythm
- **Work blocks:** 60–90 minutes; at the end of each, save one artifact (table, figure, or commit)  
- **Daily log:** jot 3 bullets: *What I tried, What I found, What’s next*  
- **Weekly evidence:** one HTML report + 2 figures posted to `05_deliverables/weekX/`

---

## 13) Simple Python Guides (no heavy code)
- Use `display(df.info())`, `display(df.describe())`, `df.isna().sum().sort_values()` for triage.  
- Normalize names once; use a `labels = {col: "Human Label"}` dict from the codebook for plots.  
- Paired tests: same individuals, pre vs post; report mean diff + CI + effect size.  
- RM‑ANOVA/LMM require **long** format (`id`, `time`, `value`).  
- Always save artifacts with stable filenames so your report can import them directly.

---

## 14) Glossary
- **EDA:** Early diagnostics + descriptive analytics to understand structure and signal  
- **Paired test:** within‑subject comparison at two timepoints  
- **RM‑ANOVA:** repeated‑measures ANOVA across ≥2 timepoints within subjects  
- **LMM:** linear mixed model; handles correlation, missingness, covariates with random effects

---

## 15) Next Actions (for Alex, today)
1) Finish A‑block triage (types, names, missingness) and save `clean.csv`.  
2) Produce `kpi_summary.csv` + two plots (distribution + paired slope).  
3) Run paired tests; export `tests_prepost.csv`.  
4) Draft `EXEC_SUMMARY.md` (5 bullets).  
5) Export the notebook to HTML and tag release `v0.1-eda`.

---

**Notes:** Keep the synthetic t2 clearly labeled as simulation if you decide to rehearse the 3‑timepoint pipeline now.
