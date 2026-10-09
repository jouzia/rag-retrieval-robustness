# Primary Experiment Validation — 2026-10-02

## Scope

This validation re-analyzes the frozen 240-row primary experiment:
20 questions sampled from the benchmark training split (`train.sample(20, random_state=42)`) × 3 retrieval methods × 4 appended-context distractor levels (0, 1, 2, 4), original retrieval top-k = 5. The 20-question sample is not a held-out test set.

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

The only comparison remaining significant after the 27-test Holm correction was generation-call latency for the dense-method pipeline at 4 appended distractors:

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

Important design qualification: the notebook retrieves the original top-five first and appends distractor chunks afterward. Therefore, zero intrusion and 100% preservation are guaranteed by construction and do not demonstrate retrieval robustness. The current experiment evaluates appended context, not perturbed retrieval ranking.

This should not be generalized to arbitrary distractor distributions, corpora, retrievers, top-k values, or RAG pipelines. The 20 questions were sampled from the training split rather than a held-out test set. The answer-quality metrics also do not show a statistically significant degradation under the tested random-noise conditions after multiplicity correction.

The timer was verified in notebook code to surround `generate_rag_answer`, so this is generation-call latency, not isolated retrieval latency. It may include external model-service/runtime variability and cannot be attributed solely to retrieval.

## Version reconciliation

An earlier analysis artifact used a different latency baseline/noise-4 value. Re-analysis of the recovered raw CSV gives **0.405087 s → 0.595432 s**, not the earlier values. The repository should treat this validation and the frozen raw CSV as authoritative.
