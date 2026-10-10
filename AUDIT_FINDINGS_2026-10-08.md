# Reproducibility and Design Audit — Research 1

Audit updated: 2026-10-10  
Repository: https://github.com/jouzia/rag-retrieval-robustness  
Scope: committed notebook, primary CSV, validated statistics, manuscript claims, provenance, and publication readiness.

## Executive finding

The statistical table was recomputed from the currently committed 240-row CSV in a clean GitHub Actions Linux environment. The strict checksum-enforcing workflow passed: the committed-file SHA-256 check, static notebook audit, 27-test recomputation, and comparison against the validated table all succeeded. A separate workflow now renders a draft PDF from the current manuscript source.

The work is **not submission-ready**. The saved notebook's Papermill metadata records `exception: true`; cell 39 fails with `AssertionError: Expected 240 rows, found 15`. The static audit does not execute the notebook, and the new CI workflow deliberately avoids all notebook/API/LLM execution.

## Finding 1 — Correct inferential family: 27 comparisons

The primary design contains 3 retrieval methods, 3 non-zero distractor contrasts (1, 2, 4 versus baseline), and 3 metrics. The family is therefore **3 × 3 × 3 = 27 paired tests**, not 36. Holm correction is applied jointly to the 27 p-values. A clean CI diagnostic recomputation produced 27 rows, one Holm-significant contrast, and matched the committed validated table across nine numeric columns and the significance flag.

## Finding 2 — The study tests appended context, not retrieval-ranking robustness

The saved primary construction cell first retrieves five chunks from the original corpus, then appends sampled distractor chunks to the context passed to the generator. Retrieval is not rerun against a perturbed candidate corpus.

Consequently:
- Zero intrusion into the original top-five and 100% top-five preservation are construction properties, not evidence of retriever robustness.
- The experiment does not test whether distractors displace relevant chunks or change retrieval rankings.
- The timer surrounds `generate_rag_answer`, so the measured latency is generation-call latency, not isolated retrieval latency.

The appropriate title and scope are **Effects of Appended Distractor Context on RAG Answer Quality and Generation Latency**.

## Finding 3 — Query-selection provenance was misstated in earlier documentation

The saved primary construction cell uses `research_questions = train.iloc[:20].copy()`, not `train.sample(20, random_state=42)`. The committed CSV contains 20 distinct IDs, `q_0001` through `q_0020`, each repeated across the method/noise design. The primary queries are therefore the first 20 records in dataset order, not a random sample and not a held-out set. Seed 42 is used for distractor selection. README, validation, manuscript, and publication-readiness documentation have been corrected to reflect this.

This ordering-based query selection is a limitation and should be disclosed; do not describe the query sample as randomized.

## Finding 4 — CSV checksum discrepancy and resolution

An earlier validation record and the canonical script used SHA-256 `6f52a5bc2c5b871beb9340f5c7c12d6eefdbb8bb71b41e566998271047fa1756`, but that digest did not match the bytes currently committed in GitHub. The committed file's SHA-256 is `1e666b0b81608dcf3a6995f4c203dd3078a941768a38c627ae801ed0501d653b`. The mismatch was not explained by line-ending normalization; the cause of the old digest discrepancy remains unknown.

To avoid silently bypassing the integrity check, a diagnostic run recomputed the current committed CSV with hash enforcement temporarily bypassed **for investigation only**. It validated 240 rows and 27 tests, then matched the committed validated statistical table across all nine numeric fields and significance flags. The canonical script has now been anchored to the current committed-file hash, and the workflow has been restored to strict hash enforcement. The strict hash-enforcing workflow subsequently passed on commit `83729e269acf9a73fed9ab4ec6acd27e27c8d551`: https://github.com/jouzia/rag-retrieval-robustness/actions/runs/38057021489. See `VALIDATION.md` for the full disclosure.

## Finding 5 — Saved notebook is not a clean end-to-end execution

Source-level inspection found:
- 91 notebook cells;
- 39 code cells with saved execution counts in the static-audit snapshot;
- Papermill metadata with `exception: true`;
- saved cell 39 raising `AssertionError: Expected 240 rows, found 15`;
- package-install cells 6, 11, and 25;
- Groq/API-related cells 26, 27, 28, 30, and 33;
- no obsolete primary-result wording found by the static audit's specific patterns; and
- a prominent warning against “Run All”.

The static audit only identifies risks; it does not certify notebook execution. Do not run the notebook's LLM cells merely to complete the artifact audit.

## Finding 6 — Confirmed statistical result and interpretation boundary

The only comparison remaining significant after Holm correction is generation-call latency for the dense-method pipeline at four appended distractors:
- baseline mean: 0.405087 s;
- noise-4 mean: 0.595432 s;
- absolute change: +0.190345 s;
- relative change: +46.99%;
- raw p: 0.001690;
- Holm-adjusted p: 0.045628;
- paired rank-biserial correlation: 0.761905;
- n = 20.

No Token F1 or semantic-similarity comparison remains significant after correction. This single result is close to alpha = 0.05 and may reflect model-service/runtime variability. It should be described as exploratory and replicated before stronger claims.

## Method details recoverable from the notebook

- BM25: `rank_bm25`, lowercased whitespace tokenization.
- Dense retrieval: FAISS `IndexFlatIP`; query embeddings use `sentence-transformers/all-MiniLM-L6-v2` and normalized embeddings. The benchmark's `embedding_model_info.txt` identifies the supplied corpus embeddings as the same model, 384-dimensional, normalized, batch size 64, generated offline.
- Hybrid retrieval: separately min-max-normalized BM25 and dense score arrays, combined as `(1 - alpha) * bm25_norm + alpha * dense_norm`, with `alpha = 0.5`.
- Generation: Groq API model identifier `openai/gpt-oss-20b`, `temperature=0`.
- Token F1: lowercase text, replace characters outside `[a-z0-9_]` with spaces, split on whitespace, then calculate overlap-based F1.
- Semantic similarity: normalized `all-MiniLM-L6-v2` embeddings and cosine similarity via Sentence Transformers and scikit-learn.
- Latency: wall-clock `time.time()` around the `generate_rag_answer` call.

Still unresolved: exact model revision, original dependency versions, exact model-serving snapshot, precise host hardware, and warm-up/caching controls. The Kaggle data page lists the competition files (including embeddings and embedding metadata) under CC BY 4.0, and the Hugging Face model card lists Apache-2.0 for `all-MiniLM-L6-v2`; confirm there are no additional separately sourced artifacts before release.

## Literature audit

The key related-work entries were checked against official ACL Anthology records:
- Shen et al. (EMNLP 2024), “Assessing ‘Implicit’ Retrieval Robustness of Large Language Models”: https://aclanthology.org/2024.emnlp-main.507/
- Pan et al. (EMNLP 2024), “Not All Contexts Are Equal: Teaching LLMs Credibility-aware Generation”: https://aclanthology.org/2024.emnlp-main.1109/
- NoMIRACL (Findings of EMNLP 2024): https://aclanthology.org/2024.findings-emnlp.730/
- Cho et al. (Findings of EMNLP 2024), “Typos that Broke the RAG’s Back”: https://aclanthology.org/2024.findings-emnlp.161/
- Amiraz et al. (ACL 2025), “The Distracting Effect”: https://aclanthology.org/2025.acl-long.892/
- Cuconasu et al. (EMNLP 2025), “Do RAG Systems Really Suffer From Positional Bias?”: https://aclanthology.org/2025.emnlp-main.1422/

These papers establish the relevance of noisy and distracting contexts but do not validate the present experiment's results. The current experiment remains narrower because it appends distractors after retrieval.

## Remaining work before submission

1. Confirm the latest strict hash-enforcing GitHub Actions workflow passes and retain its log/artifact.
2. Verify license coverage for every bundled artifact, especially corpus embeddings; do not assume the benchmark license automatically covers separately sourced assets.
3. Complete or explicitly mark unavailable original package/model/runtime provenance.
4. Finish the automated draft-PDF render from the corrected manuscript and visually inspect it. The existing top-level PDF has an older title/framing and is superseded.
5. Freeze a clearly labelled draft release only after the above checks. Do not claim peer review, acceptance, universal retrieval robustness, or a DOI that has not been minted.

A separate candidate-pool perturbation experiment with held-out queries and ranking metrics is an optional follow-up. It is not required to report the current appended-context study honestly.
