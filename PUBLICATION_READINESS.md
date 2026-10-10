# Publication Readiness — Research 1

**Audit reviewed:** 2026-10-10  
**Current status: NOT SUBMISSION-READY.** The statistical table has been independently recomputed from the committed 240-row CSV and matches the committed validated table. The strict checksum-enforcing CI rerun is in progress after the repository checksum was reconciled. The saved notebook itself is not a successful clean end-to-end run.

## Completed and supported

- [x] Committed primary CSV: 240 observations, 13 columns; 20 question IDs × 3 methods × 4 appended-distractor levels.
- [x] Dataset structure checked: no missing values in required analysis fields, no duplicate experiment keys, and 20 rows per method × distractor cell.
- [x] Correct inferential family: 27 paired comparisons (3 methods × 3 non-zero distractor levels × 3 metrics), Holm correction, paired rank-biserial effects.
- [x] Recomputed all 27 tests from the committed CSV in a clean GitHub Actions Linux environment; all nine numeric columns and the Holm-significance flags matched the committed validated statistical table within explicit numeric tolerances.
- [x] Latest strict hash-enforcing GitHub Actions run passed: static audit, committed-file SHA-256 check, 240-row/27-test recomputation, and full comparison against the validated statistical table all passed without LLM/API calls. [Run log](https://github.com/jouzia/rag-retrieval-robustness/actions/runs/38057455760).
- [x] Static notebook audit ran successfully in CI: 91 cells; 49 code cells with saved execution counts; package-install cells 6, 11, and 25; Groq/API-related cells 26, 27, 28, 30, and 33; no obsolete primary-result wording detected by the audit patterns; prominent warning against Run All found.
- [x] Core manuscript and README now describe appended-context effects, not retrieval-ranking robustness.
- [x] Query-selection provenance corrected: the saved primary construction cell uses `train.iloc[:20]`, and the committed CSV contains question IDs `q_0001`–`q_0020`. The queries were selected by dataset order, not random sampling, and are not held out. Seed 42 controls distractor selection.
- [x] Timing boundary and metric implementation documented from saved notebook source: Groq model ID `openai/gpt-oss-20b`, temperature 0; token-F1 normalization; semantic similarity with `sentence-transformers/all-MiniLM-L6-v2`; latency timer surrounds the generation call.
- [x] Embedding provenance recovered from the benchmark's `embedding_model_info.txt`: corpus embeddings use `sentence-transformers/all-MiniLM-L6-v2`, 384 dimensions, normalized, batch size 64, generated offline.
- [x] License checked against the [Kaggle competition data page](https://www.kaggle.com/competitions/agent-eval-part-i-grounded-rag-benchmark/data), which lists the included corpus embeddings and metadata under CC BY 4.0; the [Hugging Face model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) lists Apache-2.0 for the model.
- [x] Rendered the corrected Manuscript v1.3 into an 8-page draft PDF, verified title/scope/page count programmatically, and visually reviewed page previews. References are grouped together; the final page contains the final reference entries and the data/code availability note.
- [x] Related-work metadata checked against official ACL Anthology records for the key RAG distractor and positional-bias papers.

## Integrity and notebook caveats

### CSV checksum discrepancy

The earlier validation file recorded SHA-256 `6f52a5bc2c5b871beb9340f5c7c12d6eefdbb8bb71b41e566998271047fa1756`, which did not match the bytes currently committed in GitHub. The current committed CSV hash is `1e666b0b81608dcf3a6995f4c203dd3078a941768a38c627ae801ed0501d653b`. The discrepancy's origin could not be established. Because a clean environment recomputed the statistical table and matched all 27 committed validated rows, the canonical script has been re-anchored to the current committed file hash. See `VALIDATION.md`; this is not a claim that the current file is byte-identical to the earlier locally recovered copy.

### Saved notebook execution is incomplete

The saved notebook contains 91 cells and Papermill metadata with `exception: true`. Saved cell 39 raises `AssertionError: Expected 240 rows, found 15`. Therefore, do not claim the saved notebook runs end to end or that the original experiment is fully computationally reproducible. The clean CI workflow validates the frozen CSV and analysis script only; it intentionally does not execute notebook cells or call the LLM API.

## Confirmed interpretation

The primary experiment retrieves the original top five chunks first, then appends distractors to the generation context. Zero intrusion into the original top five and 100% top-five preservation are guaranteed by construction and do not demonstrate retrieval robustness.

The only comparison reported as significant after the 27-test Holm correction is dense-method **generation-call latency** at four appended distractors: 0.405087 s to 0.595432 s (+46.99%; adjusted p = 0.045628; rank-biserial correlation = 0.761905; n = 20). No Token F1 or semantic-similarity comparison remains significant after correction. The latency finding is near the 0.05 threshold and may reflect API/runtime variability; it requires cautious interpretation and replication.

The defensible current scope is an **exploratory appended-context pilot/technical report**, not a retrieval-robustness benchmark and not yet a peer-review-ready paper.

## Remaining blockers

- [ ] Confirm the latest strict hash-enforcing GitHub Actions run passes and archive its log/artifact. [Workflow runs](https://github.com/jouzia/rag-retrieval-robustness/actions/workflows/non-llm-reproducibility.yml)
- [ ] Record the exact Hugging Face model revision and original dependency versions if recoverable; the model name is known, but the revision/package lock is not present in the notebook.
- [ ] Recover or explicitly mark unavailable the original package versions, exact model-serving revision, and hardware/runtime details. The notebook metadata reports Python 3.12.13, but the original dependencies are not pinned.
- [ ] Verify the license terms for each separately sourced or bundled artifact, especially precomputed embeddings; the benchmark page's CC BY 4.0 listing should not automatically be assumed to cover every artifact.
- [ ] Finish source-level reference checks and make sure every citation is directly relevant to the specific claim it supports.
- [ ] Finish automated rendering of `paper/manuscript-draft.pdf` from the current manuscript source and visually inspect the generated pages. The top-level PDF still has the older title/framing and is explicitly superseded; do not use it as the current paper.
- [ ] After the manuscript/PDF and provenance checks are complete, freeze a clearly labelled draft release. A release or DOI does not imply peer review or acceptance.

## Safe verification commands

From the repository root, in a clean Python environment:

```bash
python scripts/audit_notebook_static.py
python scripts/recompute_primary_statistics.py results/retrieval_noise_results.csv --output results/statistical_analysis_recomputed.csv
python scripts/verify_recomputed_statistics.py results/statistical_analysis_recomputed.csv results/statistical_analysis_validated.csv
```

Do not run notebook “Run All” and do not execute Groq/API cells. No new LLM evaluations are required for the remaining statistical verification.

## Optional follow-up experiment (separate scope)

A genuine retrieval-ranking robustness experiment is not required to finish this narrower report. It would require injecting distractors into the searchable candidate corpus before retrieval, rerunning each retriever, and evaluating on held-out queries with ranking metrics. Keep it separately versioned rather than implying the current study answers that question.

## Submission claims to avoid

Do not claim universal RAG robustness, universal dense-retrieval latency sensitivity, superiority of one retrieval method, successful end-to-end notebook reproduction, peer review/publication acceptance, or a DOI that has not actually been minted.

**Next milestone:** decide whether to keep this as an exploratory technical report or design a stronger follow-up with held-out queries, more questions, controlled repeated latency measurements, and a genuine candidate-pool perturbation experiment. No new LLM evaluations are needed to preserve the current validated artifact package.
