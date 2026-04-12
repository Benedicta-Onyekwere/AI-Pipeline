---
name: transcript-topic-extractor
description: Systematic extraction, verification, and serialization of topics, commitments, and data from large transcripts. Use when analyzing lengthy documents (speeches, hearings, reports) where 100% traceability and "Chain of Custody" are required.
---

# Transcript Topic Extractor

## Overview
This skill implements a high-fidelity staged pipeline for extracting structured data from transcripts. It avoids "context clipping" by using overlapping analysis windows and ensures every extracted point is justified by directive language or measurable targets.

## Staged Pipeline Workflow

### 1. Decomposition (Overlapping Chunks)
- **Action:** Split the transcript into overlapping segments (e.g., 150 lines with 50-line overlap).
- **Goal:** Identify potential topics/commitments and their initial themes.
- **Reference:** See [extraction_logic.md](references/extraction_logic.md) for chunking parameters.
- **Artifact:** `step1_analysis.json`

### 2. Attribute Extraction
- **Action:** For each flagged item, extract specific metadata:
    - **Who:** Entity responsible.
    - **Description:** Concise summary.
    - **Amount/Numerical:** Financial or target figures.
    - **Timeline:** Deadlines or durations.
    - **Quotes:** Exact source text.
- **Artifact:** `step2_attributes.json`

### 3. Deduplication & Global Verification
- **Action:** Merge entries from overlapping chunks. Perform a **Global Re-scan** of the *entire* transcript for keywords related to each unique item.
- **Goal:** Catch missing details (budgets, dates) mentioned in distant sections of the document.
- **Artifact:** `step3_verified.json`

### 4. Justificatory Refinement & Serialization
- **Action:** Audit the "Reasoning" for every item. Ensure it justifies **why** the item is a commitment (using directive verbs) rather than just what it is about.
- **Serialization:** Use the bundled script to generate the final CSV.
- **Command:** `python3 scripts/serialize_csv.py step3_verified.json final_output.csv`

## Quality Standards
To maintain the "Chain of Custody," every extraction must:
1. Link to an **Exact Quote**.
2. Provide **Justificatory Reasoning** (e.g., "Identified as a commitment because of the verb 'will' and the R1 trillion target").
3. Be verified against the **Full Transcript** in Step 3.

---

## Bundled Resources

- **Logic Guide:** [references/extraction_logic.md](references/extraction_logic.md) - Detailed chunking and reasoning rules.
- **CSV Script:** [scripts/serialize_csv.py](scripts/serialize_csv.py) - Automates the final conversion to a review-ready CSV.
