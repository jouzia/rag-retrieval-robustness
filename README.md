# Effects of Appended Distractor Context on RAG Answer Quality and Generation Latency

**Author:** Shaik Jouzia Afreen H  
**Area:** Retrieval-Augmented Generation (RAG), information retrieval, NLP
**Study scope:** Exploratory appended-context evaluation; not a retrieval-ranking robustness test
**Source benchmark:** [Agent Eval Part I: Grounded RAG Benchmark](https://www.kaggle.com/competitions/agent-eval-part-i-grounded-rag-benchmark)

This repository evaluates how distractor chunks appended after original top-five retrieval affect answer-quality metrics and measured generation-call latency in BM25-, dense-, and hybrid-retrieval pipelines.

> **Scope note:** Findings apply only to the tested corpus, implementation, distractor construction, top-k setting, and noise levels. They do not establish universal robustness. See the limitations in the manuscript and validation record. The older top-level PDF titled *Evaluating Retrieval Robustness in RAG Systems Under Increasing Distractor Noise* predates the corrected study framing; do not cite it as the current manuscript. The current source of record is `paper/manuscript.md` until a replacement PDF is regenerated and reviewed.

## Research question

**RQ1:** Under a fixed original top-five retrieval result, how does appending distractor chunks affect generated-answer quality and generation-call latency across BM25-, dense-, and hybrid-retrieval pipelines?

## Primary experiment

| Parameter | Configuration |
|---|---|
| Questions | First 20 records from the benchmark training split (`q_0001`–`q_0020`); not randomly sampled or held out |
| Retrieval methods | BM25, dense, hybrid |
| Distractor levels | 0, 1, 2, 4 |
| Top-k | 5 |
| Total observations | 240 |
| Distractor-selection seed | 42 |
| Tests | Paired Wilcoxon signed-rank |
| Multiple comparisons | Holm correction across 27 planned comparisons |
| Effect size | Rank-biserial correlation |

## Main findings from validated result artifacts

- The frozen 240-row primary CSV was independently revalidated for integrity. This is an appended-context experiment: distractors are appended after the original top-five retrieval, and the measured latency surrounds answer generation rather than retrieval. The 20 questions in the committed primary CSV are `q_0001`–`q_0020`, matching the first-20-record construction in the saved notebook; they were not randomly sampled or held out. Seed 42 applies to distractor selection, not query sampling. Confirm competition data terms before redistributing source data or derived examples. Important design caveat: distractors were appended after top-five retrieval, so zero intrusion and 100% preservation are guaranteed by construction and do not demonstrate retrieval robustness.
- No Token F1 or semantic-similarity comparison remained significant after Holm correction.
- The dense-method context at four appended distractors was the only contrast with significant measured generation-call latency after correction: 0.405087 s to 0.595432 s (+46.99%), Holm-adjusted p = 0.045628, rank-biserial correlation = 0.761905 (n = 20). The timer surrounds answer generation, not isolated retrieval.
- No LLM evaluations were rerun during validation.
- A separate hard-semantic-distractor dataset is treated as exploratory and is not pooled with the primary experiment.

## Validated publication artifacts

- [Validated Results section](paper/RESULTS_validated.md)
- [Canonical 27-test recomputation script](scripts/recompute_primary_statistics.py)
- [Static notebook safety audit](scripts/audit_notebook_static.py)
- [Recomputed-vs-validated comparison check](scripts/verify_recomputed_statistics.py)
- [Automated non-LLM verification workflow](.github/workflows/non-llm-reproducibility.yml) (static audit + frozen-CSV statistical recomputation; does not run notebook cells or LLM calls)
- [Validated statistical analysis](results/statistical_analysis_validated.csv)
- [Validated descriptive summary](results/descriptive_summary_validated.csv)
- [Validated retrieval-stability summary](results/retrieval_stability_validated.csv)
- [Latency figure](figures/fig_latency.svg)
- [Token F1 figure](figures/fig_answer_quality.svg)
- [Semantic-similarity figure](figures/fig_semantic_similarity.svg)
- [Top-five construction diagnostic figure](figures/fig_retrieval_stability.svg)
- [Validation record](VALIDATION.md)

## Repository map

- [Full manuscript draft](paper/manuscript.md)
- [Validated Results source](paper/RESULTS_validated.md)
- [Saved Kaggle notebook (.ipynb)](notebook/rag-retrieval-robustness-study.ipynb)
- [Primary 240-row experiment CSV](results/retrieval_noise_results.csv)
- [Full primary statistical analysis](results/statistical_analysis.csv)
- [Descriptive summary](results/descriptive_summary.csv)
- [Latency summary](results/latency_summary.csv)
- [Retrieval stability summary](results/retrieval_stability_summary.csv)
- [Significant comparison](results/significant_result.csv)
- [Exploratory hard-distractor results (80 rows)](results/hard_noise_results.csv)
- [Hard-distractor descriptive summary](results/hard_noise_summary.csv)
- [Random-vs-hard comparison](results/random_vs_hard_comparison.csv)
- [Kaggle notebook page](https://www.kaggle.com/code/shaikjouziaafreenh/rag-retrieval-robustness-study)
- [Citation metadata](CITATION.cff)
- [License](LICENSE)

## Reproducibility and artifact status

The raw primary CSV is frozen and validated for data integrity. The statistical family contains 27 paired comparisons. The canonical script verifies the frozen CSV SHA-256 and recomputes the paired Wilcoxon tests and Holm correction without LLM/API calls. GitHub Actions now provides a clean Linux environment for the static notebook audit, recomputation, and comparison against the committed validated table; inspect the workflow result before describing this verification as passing. This check does not execute the notebook or rerun the LLM evaluation. See AUDIT_FINDINGS_2026-10-08.md for the design limitation: appended distractors do not test retrieval-ranking robustness. Until the remaining method/provenance and artifact review is complete, describe the repository as artifact-reconciled rather than fully computationally reproduced.

Example from the repository root: `python scripts/audit_notebook_static.py`, followed by `python scripts/recompute_primary_statistics.py results/retrieval_noise_results.csv --output results/statistical_analysis_recomputed.csv` and `python scripts/verify_recomputed_statistics.py results/statistical_analysis_recomputed.csv results/statistical_analysis_validated.csv`. Exact model identifiers, corpus provenance, package versions, hardware, and timing controls should be documented from the notebook/runtime. The saved timer surrounds `generate_rag_answer`; do not label the metric isolated retrieval latency. Do not treat a GitHub commit or release as evidence of peer review or publication. No DOI is claimed unless a Zenodo deposit is completed.

## Related work

A directly relevant study is Cuconasu et al. (2025), “Do RAG Systems Really Suffer From Positional Bias?”, *EMNLP 2025*. It examines distracting passages and positional effects across three benchmarks. Its findings motivate careful separation between post-retrieval context augmentation (the scope of this repository) and candidate-pool perturbation that reruns retrieval. [Official ACL Anthology record](https://aclanthology.org/2025.emnlp-main.1422/).

## Citation

See [CITATION.cff](CITATION.cff). Until a DOI is assigned, cite the repository URL and access date.

## References

1. Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS.
2. Robertson & Zaragoza (2009), *The Probabilistic Relevance Framework: BM25 and Beyond*, FnTIR.
3. Karpukhin et al. (2020), *Dense Passage Retrieval for Open-Domain Question Answering*, EMNLP.
4. Wilcoxon (1945), *Individual Comparisons by Ranking Methods*, Biometrics Bulletin.
5. Holm (1979), *A Simple Sequentially Rejective Multiple Test Procedure*, Scandinavian Journal of Statistics.
