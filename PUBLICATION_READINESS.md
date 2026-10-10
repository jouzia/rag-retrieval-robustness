# Publication Readiness — Research 1

**Audit reviewed:** 2026-10-10  
**Current status: NOT SUBMISSION-READY.** The primary statistical artifacts are reconciled, but the repository has not yet passed a clean local non-LLM verification and the methods/provenance record is incomplete.

## Completed and supported

- [x] Frozen primary dataset: 240 observations; 13 columns.
- [x] Dataset integrity checks: no missing values, duplicate rows, or duplicate experiment keys; 20 observations per method × noise cell.
- [x] Frozen CSV SHA-256 recorded in `VALIDATION.md` and checked by the canonical script.
- [x] Corrected inferential family: 27 paired comparisons (3 methods × 3 non-zero distractor levels × 3 metrics), with Holm correction and paired rank-biserial effect sizes.
- [x] Canonical recomputation script added; prior run reported 240 validated rows, 27 tests, and one comparison significant after Holm correction.
- [x] Previously reported statistical table reconciled against all 27 recomputed comparisons without numerical mismatches.
- [x] Notebook source inspected; static safety script added. Source-level inspection found 91 cells and identified package-install/API-related cells without executing them.
- [x] Manuscript, README, results, and audit findings reframed around **appended-context effects**, not retrieval-ranking robustness.
- [x] Latency correctly described as the timed `generate_rag_answer` call, not isolated retrieval latency.
- [x] The training-split origin of the 20 questions is disclosed; the sample is not held out.
- [x] Related-work citations on distracting/noisy RAG context added.
- [x] Figures, validated results, and manuscript draft exist in the repository or have been documented as local draft artifacts.

## Confirmed interpretation

The study retrieves the original top five documents first, then appends distractors to the generation context. Therefore, zero intrusion into the retrieved top five and 100% top-five preservation are consequences of the construction, not evidence of retrieval robustness.

The only comparison reported as significant after the 27-test Holm correction is dense-method **generation-call latency** at four appended distractors: 0.405087 s to 0.595432 s (+46.99%; adjusted p = 0.045628; rank-biserial correlation = 0.761905; n = 20). No answer-quality comparison remains significant after correction. This result is close to the 0.05 threshold and may reflect model-service/runtime variability; it needs cautious interpretation and replication.

The defensible current scope is an **exploratory appended-context pilot/technical report**, not a retrieval-robustness benchmark and not yet a peer-review-ready paper.

## Remaining blockers

- [ ] **Run the static audit script locally** and save its actual stdout log. A previous source-level scan is not equivalent to executing the script.
- [ ] **Run clean, non-LLM verification locally**: verify the frozen CSV hash and rerun the canonical statistical recomputation; compare the output against `results/statistical_analysis_validated.csv`. Do not execute notebook cells that call external APIs and do not rerun the 240 LLM evaluations.
- [ ] **Record exact runtime and dependency versions** for the original experiment where recoverable. The saved notebook does not pin the full environment, so some historical versions may not be recoverable exactly.
- [ ] **Complete method/provenance documentation**: corpus files and source, reference-answer provenance, embedding model/revision, corpus-embedding provenance, hybrid fusion implementation and parameters, distractor sampling details, latency controls/caching/warm-up, and metric implementations.
- [ ] **Verify license coverage for every redistributed artifact**, including separately bundled embeddings or files. The benchmark page is listed as CC BY 4.0, but do not assume that this automatically covers separately sourced artifacts; preserve attribution.
- [ ] **Finish source-level literature verification** for every reference and ensure claims match the cited primary papers.
- [ ] **Regenerate and inspect the PDF from the current manuscript source** after the final text and reference audit; the earlier inspected PDF was a draft and should not be represented as final.
- [ ] **Freeze and archive a release** only after the above checks pass. A DOI, if minted by an archive, identifies the archived artifact but does not imply peer review or acceptance.

## Safe local verification procedure

From the repository root in a clean Python environment with the script dependencies installed:

```bash
python scripts/audit_notebook_static.py
python scripts/recompute_primary_statistics.py results/retrieval_noise_results.csv --output results/statistical_analysis_recomputed.csv
```

Expected invariant checks: the static audit should parse the notebook and list potentially risky cells without executing them; the recomputation should verify the frozen CSV SHA-256, validate 240 rows, produce 27 paired tests, and report the significant comparison(s). Then compare the recomputed CSV with `results/statistical_analysis_validated.csv`. Preserve the stdout, Python version, dependency versions, and comparison result in a dated audit log. Do not use notebook “Run All” and do not call the LLM/API cells.

If the frozen CSV hash check fails, stop and investigate; do not use `--skip-hash-check` to claim reproduction of the published result.

## Optional follow-up experiment (separate scope)

A genuine retrieval-ranking robustness experiment is **not required to finish this narrower report**. It would require injecting distractors into the searchable candidate corpus before retrieval, rerunning each retriever, and evaluating on held-out queries with ranking metrics. Keep it as a separately versioned follow-up rather than implying the current study answers that question.

## Submission claims to avoid

Do not claim universal RAG robustness, universal dense-retrieval latency sensitivity, superiority of one retrieval method, full computational reproducibility before the clean check, peer review/publication acceptance, or a DOI that has not actually been minted.

**Next milestone:** complete the local non-LLM verification and provenance checklist. No new LLM evaluations are needed for this milestone.
