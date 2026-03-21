# Commitment Extraction Plan: 2026 SONA Transcript

This plan outlines the multi-stage, file-based pipeline used to extract, verify, and serialize commitments from the 2026 State of the Nation Address (SONA).

## Strategy Overview
The process was designed to ensure context continuity and data integrity by using overlapping chunks and intermediate verification files.

### Step 1: Decomposition & Initial Flagging
- **Input:** `SA-transcript` (804 lines)
- **Method:** Divided the transcript into 8 overlapping chunks (150 lines each with a 50-line overlap).
- **Output:** `step1_analysis.json`
- **Goal:** Identify primary themes and potential commitments with initial reasoning.

### Step 2: Structured Attribute Extraction
- **Input:** `step1_analysis.json` and `SA-transcript`
- **Method:** Systematically extracted specific attributes for each flagged commitment:
    - Description
    - Who/Organisation
    - Amount
    - Timeline
    - Exact Quotes
- **Output:** `step2_attributes.json`
- **Goal:** Create a detailed, raw list of commitments.

### Step 3: Deduplication & Global Verification
- **Input:** `step2_attributes.json` and `SA-transcript`
- **Method:** Merged overlapping entries into unique commitments. Performed a global re-scan of the full transcript using keywords (e.g., "R", "billion", "by 2030") to capture missing financial or temporal details related to each unique item.
- **Output:** `step3_verified.json`
- **Goal:** Establish a "Golden Source" of verified, unique commitments.

### Step 4: Final Serialization
- **Input:** `step3_verified.json`
- **Method:** Converted the verified JSON data into a CSV format with proper escaping for quotes and special characters.
- **Output:** `commitments_final.csv`
- **Goal:** Deliver a structured, review-ready dataset with the requested columns.

---

## Refinement Pass: Commitment Justification (Phase 2)
An additional audit was performed to improve the "Reasoning" column.

### Goal
To transition from descriptive reasoning (topic-based) to **justificatory reasoning** (commitment-based).

### Key Refinements
- **Directive Language:** Every reasoning now highlights specific verbs (e.g., "will," "directed," "committed," "embark") that indicate a formal mandate.
- **Measurability & Accountability:** Reasonings now explicitly link the commitment to specific numerical targets (e.g., "R1 trillion," "5,500 officers") and timelines (e.g., "by 2030," "within the next few days").
- **Institutional Context:** Explains why the specific phrasing (e.g., invoking the Constitution) elevates the statement to a formal state commitment.
