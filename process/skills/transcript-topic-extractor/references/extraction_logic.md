# Transcript Extraction Logic & Guidelines

This reference documents the specific logic required to maintain a "Chain of Custody" during high-accuracy transcript analysis.

## 1. Overlapping Chunk Strategy
When analyzing large transcripts (>500 lines), direct single-pass analysis often loses local context or "clips" items that span across arbitrary cut-off points.

**The Solution:**
- **Chunk Size:** 150-200 lines.
- **Overlap:** 50 lines.
- **Why:** If a commitment starts on line 148 and ends on line 152, a standard 150-line split would break it. The overlap ensures every line is analyzed twice, preserving context continuity.

## 2. Justificatory Reasoning (Commitment vs. Description)
A common failure in topic extraction is providing descriptive reasoning ("This is about water") instead of justificatory reasoning ("This is a commitment because...").

### Criteria for a "Commitment"
To qualify as a formal commitment/pledge, the text must contain at least one of:
1. **Directive Language:** Verbs like "will," "shall," "directed," "committed," "embark," or "decided."
2. **Measurability:** Specific numerical targets (e.g., "10,000 new jobs") or financial allocations (e.g., "R156 billion").
3. **Accountability:** Hard deadlines ("by 2030," "within 12 months") or named responsible entities ("I have directed the Minister of Police...").

### Reasoning Pattern
- **Weak:** "The President talks about improving the police force."
- **Strong:** "Identified as a commitment because the President uses the directive 'I have directed' paired with a specific immediate timeline ('within the next few days')."

## 3. Global Verification Pass
Step 3 of the workflow must always involve a **Global Re-scan**. 
- **Action:** Take the list of identified topics and search the *entire* transcript for keywords related to them (e.g., searching for "billion" or specific dates).
- **Goal:** Often, a commitment is mentioned on page 2, but the actual budget for it is mentioned on page 10. The global pass links these distant data points.
