# Reproducibility and Design Audit — Research 1

Audit date: 2026-10-08  
Repository: https://github.com/jouzia/rag-retrieval-robustness  
Scope: saved notebook, frozen 240-row CSV, validated statistics, manuscript claims.

## Executive finding

**The data-integrity checks and numerical latency analysis are available from the committed artifacts, but the research is not yet ready for submission under its current retrieval-robustness framing.** Two material inconsistencies were found during notebook-level inspection.

## Finding 1 — Statistical family is 27 comparisons, not 36

The design described in the notebook and result CSV contains 3 retrieval methods, 3 non-zero noise contrasts (1, 2, 4 versus baseline), and 3 metrics (Token F1, semantic similarity, latency). Therefore the family contains **3 × 3 × 3 = 27 paired tests**, not 36. The validated statistical CSV contains 27 rows. The paper and validation documents incorrectly state 36. These references must be corrected to 27 throughout.

## Finding 2 — The construction does not test whether distractors displace retrieved top-k documents

In the saved notebook's experiment-construction cell, each retrieval method first obtains its top five results from the original corpus. The code then creates context_ids by appending noise_ids to retrieved_ids. The generation experiment therefore tests the effect of adding distractor chunks to downstream context; it does not add distractors to the retrieval candidate corpus and rerun retrieval.

Consequently:
- Zero distractor intrusion into the original top-five and 100% preservation of that top-five are guaranteed by construction rather than empirical evidence of retriever robustness.
- These statistics cannot support the manuscript's claim that BM25, dense, and hybrid rankings resisted distractor noise.
- The existing experiment is better described as RAG answer-quality and runtime behavior under appended context distractors, subject to confirming the timing boundary from the generation cell.

## What remains valid

- The frozen CSV has 240 rows; previous integrity checks report no missing values or duplicate experiment keys.
- Paired descriptive and inferential calculations can be reported for the 27-test family, provided the analysis script and outputs are reconciled.
- The dense latency contrast in the frozen artifact is 0.405087 s versus 0.595432 s (+46.99%), raw p = 0.0016899, Holm-adjusted p = 0.0456276, rank-biserial correlation = 0.761905, n = 20. **Do not label this retrieval latency until the timer boundaries are verified.** If the timer surrounds the LLM request, it is generation/API latency and may reflect model-service variability.

## Required corrective work before submission

1. Correct the planned comparison count from 36 to 27 in the manuscript, validated results, README, validation record, and notebook markdown.
2. Reframe the existing experiment around appended distractor context, not retrieval-ranking robustness.
3. Inspect the timing code and explicitly name the measured latency (retrieval, generation/API, or end-to-end).
4. State that top-five contamination/preservation measures are tautological under the current construction; do not present them as a positive empirical result.
5. If retaining the original retrieval-robustness question, design a new experiment that adds distractors to the candidate corpus before retrieval and then reruns each retriever. This would be a new experiment and should be separately versioned; the frozen LLM dataset need not be rerun merely to correct the existing paper.
6. Recompute analysis outputs from the frozen CSV using a single canonical script and confirm agreement with committed tables.
7. After these corrections, run a clean, non-LLM notebook analysis audit and prepare the submission package.

## Publication status

**Not yet publication-ready.** The 240-row experiment and initial analysis exist, but the framing/design mismatch and comparison-count error are material. The current result should not be submitted as evidence that the retrievers themselves are robust to distractors. No claim of peer review, acceptance, or DOI is warranted.
