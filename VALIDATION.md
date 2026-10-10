# Primary Experiment Validation — 2026-10-02

## Scope

This validation re-analyzes the frozen 240-row primary experiment:
20 questions (`q_0001`–`q_0020`) taken from the first 20 records of the benchmark training split, matching the primary construction cell (`train.iloc[:20]`), × 3 retrieval methods × 4 appended-context distractor levels (0, 1, 2, 4), original retrieval top-k = 5. The query set is neither randomly sampled nor held out. Seed 42 is used for distractor selection, not query sampling.

The committed CSV is the current analysis input. No LLM evaluations were rerun.

**Current committed-file SHA-256:** `1e666b0b81608dcf3a6995f4c203dd3078a941768a38c627ae801ed0501d653b`

**Checksum provenance note:** an earlier version of this validation recorded `6f52a5bc2c5b871beb9340f5c7c12d6eefdbb8bb71b41e566998271047fa1756`, but that digest does not match the bytes currently committed in GitHub. The reason for the discrepancy could not be established. A clean GitHub Actions run recomputed the 27 comparisons from the current committed CSV and matched the committed validated table across all nine numeric columns and the significance flags. The canonical script now anchors integrity to the current committed file hash. This is a transparent re-baselining of the repository artifact, not a claim that its bytes are identical to the earlier locally recovered file.

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

This should not be generalized to arbitrary distractor distributions, corpora, retrievers, top-k values, or RAG pipelines. The 20 questions are the first 20 training-split records (`q_0001`–`q_0020`), not a random sample or held-out test set. The answer-quality metrics also do not show a statistically significant degradation under the tested random-noise conditions after multiplicity correction.

The timer was verified in notebook code to surround `generate_rag_answer`, so this is generation-call latency, not isolated retrieval latency. It may include external model-service/runtime variability and cannot be attributed solely to retrieval.

## Version reconciliation

An earlier analysis artifact used a different latency baseline/noise-4 value. Re-analysis of the recovered raw CSV gives **0.405087 s → 0.595432 s**, not the earlier values. The repository should treat this validation and the frozen raw CSV as authoritative.


## Notebook execution-state limitation

A source-level inspection of the committed notebook JSON found 91 cells, 49 cells with saved execution counts, and Papermill metadata with `exception: true`. Saved cell 39 contains an `AssertionError`: it loaded 15 rows where it expected 240. This means the saved notebook execution is incomplete and must not be presented as a successful clean end-to-end run. The current 240-row CSV and statistical outputs were validated separately by the non-LLM recomputation workflow; that workflow deliberately does not execute notebook cells or call the LLM API.

The notebook metadata records Python 3.12.13, but package versions for the original run are not pinned. A current clean analysis environment can reproduce the statistical table from the committed CSV, but it does not reconstruct the original retrieval/generation environment or prove that the full notebook runs end to end.
