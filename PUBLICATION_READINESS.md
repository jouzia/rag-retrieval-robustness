# Publication Readiness — Research 1

## Current status

**Not yet publication-ready. Notebook audit found a research-design mismatch and a statistical-family count error. See [audit findings](AUDIT_FINDINGS_2026-10-08.md).**

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
- [x] Validated Results section
- [x] Statistical CSV artifacts
- [x] Publication vector figures
- [x] Manuscript reframed around appended-context effects and synchronized with validated statistics
- [x] Exploratory hard-distractor experiment kept separate
- [x] Reproducibility limitations explicitly documented
- [x] Citation metadata present
- [x] License present
- [ ] Regenerate current PDF from the revised manuscript and inspect pagination/figures

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

1. Recompute all 27 statistical comparisons from the frozen CSV with a committed canonical analysis script and compare all rows against the validated CSV.
2. Audit notebook execution/output consistency without rerunning the 240 LLM calls.
3. Finish manuscript and README terminology consistency, including figures and citation metadata.
4. Generate and inspect a fresh PDF from the revised manuscript.

A clean environment run is still required before claiming full computational reproducibility.

The clean rerun should document:

1. Exact Python/runtime version.
2. Package versions.
3. Hardware/runtime environment.
4. Exact embedding model identifier/version.
5. Corpus provenance and license.
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

The framing, 27-test family count, and timing terminology have now been corrected in the core manuscript and documentation. The next steps are a reproducible statistical-output check, a non-LLM notebook audit, figure/metadata cleanup, and a fresh PDF build. A candidate-pool perturbation experiment is a separate optional study if the original retrieval-robustness question is still a goal; it is not needed to honestly submit this narrower appended-context study.
