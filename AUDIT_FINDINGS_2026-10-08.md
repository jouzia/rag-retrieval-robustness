# Reproducibility and Design Audit — Research 1

Audit date: 2026-10-08  
Repository: https://github.com/jouzia/rag-retrieval-robustness  
Scope: saved notebook, frozen 240-row CSV, validated statistics, manuscript claims.

## Executive finding

**The core manuscript and notebook wording have now been corrected to describe the actual appended-context experiment.** The frozen data and statistical recomputation are available, but publication preparation is still blocked by full artifact-to-artifact comparison, clean non-LLM notebook verification, incomplete method/provenance reporting, literature coverage, and the need for a fresh inspected PDF.

## Finding 1 — Statistical family is 27 comparisons, not 36

The design described in the notebook and result CSV contains 3 retrieval methods, 3 non-zero noise contrasts (1, 2, 4 versus baseline), and 3 metrics (Token F1, semantic similarity, latency). Therefore the family contains **3 × 3 × 3 = 27 paired tests**, not 36. The validated statistical CSV contains 27 rows. The manuscript, README, validation record, citation metadata, and notebook have since been revised to use the corrected scope and count. A canonical script now recomputes the 27 tests from the frozen CSV without making LLM/API calls.

## Finding 2 — The construction does not test whether distractors displace retrieved top-k documents

In the saved notebook's experiment-construction cell, each retrieval method first obtains its top five results from the original corpus. The code then creates context_ids by appending noise_ids to retrieved_ids. The generation experiment therefore tests the effect of adding distractor chunks to downstream context; it does not add distractors to the retrieval candidate corpus and rerun retrieval.

Consequently:
- Zero distractor intrusion into the original top-five and 100% preservation of that top-five are guaranteed by construction rather than empirical evidence of retriever robustness.
- These statistics cannot support the manuscript's claim that BM25, dense, and hybrid rankings resisted distractor noise.
- The existing experiment is better described as RAG answer-quality and generation-call latency under appended context distractors. The notebook code confirms that the timer starts immediately before and stops immediately after `generate_rag_answer`, so it measures the answer-generation function call, not isolated retrieval.

## What remains valid

- The frozen CSV has 240 rows; previous integrity checks report no missing values or duplicate experiment keys.
- Paired descriptive and inferential calculations can be reported for the 27-test family, provided the analysis script and outputs are reconciled.
- The dense latency contrast in the frozen artifact is 0.405087 s versus 0.595432 s (+46.99%), raw p = 0.0016899, Holm-adjusted p = 0.0456276, rank-biserial correlation = 0.761905, n = 20. The timer was subsequently verified to surround `generate_rag_answer`; therefore this is generation-call latency, not isolated retrieval latency, and it may reflect model-service variability.

## Corrective work status

### Completed in the repository

- [x] Corrected the comparison family to 27 tests.
- [x] Reframed the manuscript, README, validated results, and notebook around appended-context effects.
- [x] Relabeled latency as generation-call latency and documented the verified timer boundary.
- [x] Reclassified zero intrusion / 100% top-five preservation as construction diagnostics.
- [x] Updated the citation title and figure labels.
- [x] Added `scripts/recompute_primary_statistics.py`, which verifies the frozen CSV checksum and recomputes the 27 paired tests without LLM/API calls.
- [x] Executed the canonical script against the frozen CSV: 240 rows validated, 27 tests produced, one comparison remained significant after Holm correction.
- [x] Cross-checked all 27 rows for baseline/noisy means, absolute changes, Wilcoxon statistics, and rank-biserial effects; no mismatches found.
- [x] Recomputed Holm-adjusted p-values from the stored 27 raw p-values; all 27 adjusted values and significance flags match the validated artifact.

### Still required before submission

1. Complete a final raw p-value row-by-row comparison between the canonical script output and `results/statistical_analysis_validated.csv`. All other checked numerical fields and the Holm correction match.
2. Run a clean, non-LLM notebook audit; do not rerun the 240 LLM evaluations.
3. Complete the methods record: corpus/question provenance and license, exact retriever and hybrid-fusion implementation, package/runtime versions, embedding and semantic-similarity model details, and timing controls. The notebook samples 20 questions from the Kaggle benchmark training split, not the held-out test set; verify the competition's redistribution terms before any wider data release.
4. Verify the related-work section against the cited primary papers and expand the literature review as needed. A preliminary set of directly relevant 2024–2025 papers has now been added.
5. Generate a fresh PDF from the revised manuscript and inspect figures, references, page breaks, and metadata.
6. Optionally, if the original retrieval-ranking robustness question remains a goal, design a separate candidate-pool perturbation experiment. It is not required to describe the existing experiment honestly and must not be conflated with these frozen results.

## Publication status

**Not yet publication-ready.** The original framing/count errors have been corrected in the core artifacts, and the frozen-data analysis script has been run. Submission remains blocked by the validation tasks listed above. The current result must not be submitted as evidence that the retrievers themselves are robust to distractors. No claim of peer review, acceptance, or DOI is warranted.
