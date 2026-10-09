# Publication Readiness — Research 1

## Current status

**Not yet publication-ready.** The original scope/count errors have been corrected in the core manuscript and notebook text. Remaining blockers are source-data terms, final raw p-value comparison, clean non-LLM reproducibility verification, and a fresh inspected PDF. See [audit findings](AUDIT_FINDINGS_2026-10-08.md).

### Completed

- [x] Frozen primary dataset: 240 observations
- [x] Dataset integrity validation
- [x] No missing values
- [x] No duplicate experiment keys
- [x] 20 observations per method × noise cell
- [x] Confirmed zero intrusion / 100% preservation are construction artifacts and documented them as such (not evidence of robustness)
- [x] 27 planned paired statistical comparisons
- [x] Holm correction across the 27-test family
- [x] Paired rank-biserial effect sizes
- [x] Validated primary result reconciled with raw CSV
- [x] Canonical Python script added to recompute all 27 tests without LLM/API calls
- [x] Canonical script executed against frozen CSV: 240 rows, 27 tests, one Holm-significant comparison
- [x] Validated Results section
- [x] Statistical CSV artifacts
- [x] Publication vector figures
- [x] Manuscript reframed around appended-context effects and synchronized with validated statistics
- [x] Exploratory hard-distractor experiment kept separate
- [x] Reproducibility limitations explicitly documented
- [x] Citation metadata present
- [x] Repository license present
- [ ] Confirm source benchmark data redistribution terms
- [ ] Regenerate current PDF from the revised manuscript and inspect pagination/figures

## Contribution and publication-strength assessment

The current dataset is best positioned as an **exploratory technical report/pilot**, not yet a strong peer-reviewed contribution. The 20 questions were sampled from the benchmark training split, the sample is small, the answer-quality findings are null after correction, and directly related work on distracting/noisy RAG context already exists. A credible paper targeting retrieval robustness needs a separately versioned candidate-pool perturbation experiment with a held-out query set, explicit distractor construction, retrieval-ranking metrics, and a clearly articulated contribution beyond prior noisy-context evaluations.

## Confirmed primary finding

Generation-call latency for the dense-method pipeline at four appended distractors is the only comparison that remains significant after Holm correction:

- 0 distractors: 0.405087 s
- 4 distractors: 0.595432 s
- Absolute increase: 0.190345 s
- Relative increase: 46.99%
- Wilcoxon W: 25
- Raw p: 0.001690
- Holm-adjusted p: 0.045628
- Paired rank-biserial correlation: 0.761905
- n = 20

No answer-quality comparison remains significant after correction.

## Remaining blockers before a submission-ready package

1. [x] Compare all 27 raw p-values and Holm-adjusted p-values against the committed validated CSV; no mismatches. The 27-row count, descriptive means, absolute changes, Wilcoxon statistics, effect sizes, Holm-adjusted values, and significance flags have been checked without mismatches.
2. Perform a clean, non-LLM notebook audit and confirm the analysis path is consistent with the canonical script; do not rerun LLM cells.
3. Confirm the Kaggle benchmark's data-use/redistribution terms and document the fact that the 20 questions came from the training split, not a held-out test set.
4. Finish exact package/runtime and metric-model documentation; review the newly added related-work section against the primary sources.
5. Generate and inspect a fresh PDF from the revised manuscript.

A clean environment run is still required before claiming full computational reproducibility.

The clean rerun should document:

1. Exact Python/runtime version.
2. Package versions.
3. Hardware/runtime environment.
4. Exact embedding model identifier/version.
5. Corpus provenance and license (source dataset terms are still unconfirmed).
6. Question/reference-answer provenance.
7. BM25, dense, and hybrid implementation details.
8. Hybrid fusion method and parameters.
9. Distractor generation algorithm and seed.
10. Exact latency timing boundary, warm-up, and caching policy.
11. Metric implementation and semantic-similarity model.
12. Output checksums and comparison against the frozen CSV.

**Important:** Do not rerun the LLM evaluation merely to satisfy this checklist. The completed 240-row raw result set is frozen and was independently validated. A clean reproducibility run should reuse the saved raw outputs where appropriate and verify the analysis pipeline without generating new LLM observations.

## Publication claims

Until the clean rerun is completed, describe the repository as **artifact-reconciled** rather than fully computationally reproduced.

Do not claim:
- universal RAG robustness;
- universal dense-retrieval latency sensitivity;
- superiority of one retrieval method over another;
- peer review or publication;
- a DOI unless a repository such as Zenodo has actually minted one.

## Recommended next stage

The framing, 27-test family count, and timing terminology have now been corrected in the core manuscript and documentation. The current study remains an exploratory appended-context evaluation, not evidence of retriever robustness. A canonical script has been run against the frozen CSV (240 rows, 27 tests, one Holm-significant result). Cross-artifact checks found no mismatches in baseline/noisy means, absolute changes, Wilcoxon statistics, rank-biserial effects, or the Holm correction applied to the stored p-values. The remaining steps are a clean non-LLM notebook/runtime audit, confirmation of data-use terms, completion of methods/provenance details, final review of related-work coverage, and a fresh PDF build. A candidate-pool perturbation experiment is a separate optional study if the original retrieval-robustness question is still a goal; it is not needed to honestly submit this narrower appended-context study.
