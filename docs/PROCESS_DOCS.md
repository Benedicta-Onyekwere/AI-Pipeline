# SONA 2026 Commitment Extraction: Process & Traceability Documentation

This document provides a technical overview of the methodology, execution, and verification steps used to extract formal commitments from the 2026 State of the Nation Address (SONA). It is designed to ensure full auditability and data integrity for any stakeholder reviewing the final dataset.

---

## 1. Project Objective, Goal, and Target Output
*   **Objective:** To systematically identify and document every formal commitment, target, and policy mandate issued by the President during the 2026 SONA.
*   **Goal:** To establish a "Golden Source" of verified data with 100% traceability to the original 804-line transcript, ensuring no context was lost through "clipping" during analysis.
*   **Target Output:** A comprehensive CSV file (`commitments_final.csv`) containing 33 unique, verified commitments, each structured with six audit columns:
    1.  **Description:** A concise summary of the pledge.
    2.  **Who/Organisation:** The entity responsible for delivery (e.g., Presidency, SAPS, DHA).
    3.  **Amount:** Specific financial or numerical targets (e.g., R1 trillion, 10,000 inspectors).
    4.  **Timeline:** Clear deadlines or durations (e.g., "by mid-2026," "next three years").
    5.  **Exact Quotes:** Direct evidence from the transcript for verification.
    6.  **Reasoning:** Justificatory logic explaining why the content qualifies as a commitment.

## 2. Source Material
The extraction process utilized two versions of the 2026 SONA for different purposes:
*   **Primary Input (`SA-SONA-2026.md`):** A formatted, human-readable Markdown conversion of the speech used for theme identification and structural analysis.
*   **Reference Source (`SA-transcript`):** The raw 804-line document used for precise line-level indexing and keyword-based global verification.

## 3. Methodology: Staged Pipeline Architecture
To ensure maximum precision, the extraction followed a **Staged Pipeline Architecture**:
*   **Sequential Handoff:** The output of each phase was saved as an immutable JSON file, which then served as the sole input for the next phase.
*   **Chain of Custody:** This "chain" allows any row in the final CSV to be traced back through three levels of verification to its exact position in the transcript.
*   **AI Orchestration:** The process utilized the Gemini CLI and parallel sub-agents to process high volumes of data without losing the local context of the speech.

## 4. Detailed Step-by-Step Execution

### Step 1: Decomposition & Overlapping Chunk Analysis
The transcript was divided into 8 overlapping chunks (150 lines each with a 50-line overlap).
*   **Logic:** Overlaps prevent commitments from being "cut" between analysis windows.
*   **Output:** `step1_analysis.json` (Initial flagging of themes and potential commitments).

### Step 2: Structured Attribute Extraction
Each flagged commitment was analyzed locally within its chunk to extract metadata.
*   **Attributes:** Description, Who, Amount, Timeline, and Exact Quotes.
*   **Output:** `step2_attributes.json` (A detailed but raw list of commitments).

### Step 3: Deduplication & Global Verification
Chunk-level findings were merged into unique entries. A **Global Re-scan** of the full 804 lines was performed using a regex keyword search (e.g., *"R", "billion", "by 2030"*) to find data points (like an amount or a deadline) that might have been mentioned in different parts of the speech from the primary commitment statement.
*   **Output:** `step3_verified.json` (The "Golden Source").

### Step 4: Justificatory Refinement & Serialization
A final "Justification Pass" was conducted to ensure the "Reasoning" column focused on **why** a statement is a commitment (e.g., citing directive language or measurable targets) rather than just describing the topic.
*   **Serialization:** A Python-based conversion script generated the final CSV with proper character escaping for all fields.
*   **Output:** `commitments_final.csv`.

## 5. Quality Control: Commitment Identification Markers
To be included in the final dataset, a statement had to meet at least one of these criteria:
*   **Directive Language:** Use of verbs like *"will," "directed," "committed,"* or *"shall."*
*   **Measurability:** Inclusion of specific numerical or monetary targets (e.g., **R156 billion**, **5,500 additional police officers**).
*   **Accountability:** Inclusion of a hard deadline (e.g., **"by 2030"**, **"within the next few days"**).

## 6. Final Artifacts Catalog
All files produced during this process are available in the repository for audit:
*   **`PLAN.md`**: The technical strategy used for the extraction.
*   **`step1_analysis.json`**: Initial chunk-level findings.
*   **`step2_attributes.json`**: Raw extracted metadata.
*   **`step3_verified.json`**: The deduplicated and globally verified "Golden Source."
*   **`commitments_final.csv`**: The final delivery file.
*   **`docs/PROCESS_DOCS.md`**: This documentation file.

---
**Document Status:** Final  
**Date:** March 21, 2026
