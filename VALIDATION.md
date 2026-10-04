# Primary Experiment Validation — 2026-10-02

## Scope

This validation re-analyzes the frozen 240-row primary experiment:
20 questions × 3 retrieval methods × 4 random distractor levels (0, 1, 2, 4), top-k = 5.

The recovered CSV is the authoritative raw dataset. No LLM evaluations were rerun.

**SHA-256:** `6f52a5bc2c5b871beb9340f5c7c12d6eefdbb8bb71b41e566998271047fa1756`

## Integrity checks

- Rows: 240
- Columns: 13
- Missing values: 0
- Duplicate rows: 0
- Duplicate experiment keys (`question_id`, method, noise): 0
- Methods: BM25, dense, hybrid
- Noise levels: 0, 1, 2, 4
- Observations per method × noise cell: 20
- Retrieval list length: 5 for every observation
- Injected distractor intrusion into final top-5: 0/240
- Baseline top-5 preservation: 100% in every method × noise condition

## Statistical procedure

For each method, metric, and noise level 1/2/4, the noisy condition was compared with the same question at noise level 0 using a paired Wilcoxon signed-rank test.

The complete family of 27 planned pairwise tests (3 methods × 3 metrics × 3 noise contrasts) was corrected jointly with Holm's step-down procedure. Alpha = 0.05.

Effect size is paired rank-biserial correlation.

## Confirmed primary result

The only comparison remaining significant after the 27-test Holm correction was dense-retrieval latency at 4 distractors:

- baseline mean: 0.405087 s
- noise-4 mean: 0.595432 s
- absolute change: +0.190345 s
- relative change: +46.99%
- Wilcoxon W: 25
- raw p: 0.001690
- Holm-adjusted p: 0.045628
- rank-biserial correlation: 0.761905
- n: 20

No token-F1 or semantic-similarity comparison remained significant after Holm correction.

## Interpretation boundary

The experiment demonstrates stability of the tested top-5 retrieval rankings under the specified random distractors, because no injected distractor entered the final top-5 and all top-5 rankings matched the corresponding noise-0 baseline.

This should not be generalized to arbitrary distractor distributions, corpora, retrievers, top-k values, or RAG pipelines. The answer-quality metrics also do not show a statistically significant degradation under the tested random-noise conditions after multiplicity correction.

The latency finding is an operational effect for the tested dense-retrieval implementation and runtime; it is not evidence that dense retrieval is universally more or less efficient.

## Version reconciliation

An earlier analysis artifact used a different latency baseline/noise-4 value. Re-analysis of the recovered raw CSV gives **0.405087 s → 0.595432 s**, not the earlier values. The repository should treat this validation and the frozen raw CSV as authoritative.
