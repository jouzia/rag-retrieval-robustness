# Evaluating Retrieval Robustness in RAG Systems Under Increasing Distractor Noise

**Author:** Shaik Jouzia Afreen H  
**Area:** Retrieval-Augmented Generation (RAG), information retrieval, NLP

This repository studies how injected distractor documents affect retrieval stability, answer-quality metrics, and latency for BM25, dense, and hybrid retrieval.

> **Scope note:** Findings apply only to the tested corpus, implementation, distractor construction, top-k setting, and noise levels. They do not establish universal robustness. See the limitations in the manuscript and validation record.

## Research question

**RQ1:** How does increasing distractor-document noise affect retrieval stability, generated-answer quality, and latency in BM25, dense, and hybrid retrieval systems within a RAG pipeline?

## Primary experiment

| Parameter | Configuration |
|---|---|
| Questions | 20 |
| Retrieval methods | BM25, dense, hybrid |
| Distractor levels | 0, 1, 2, 4 |
| Top-k | 5 |
| Total observations | 240 |
| Sampling seed | 42 |
| Tests | Paired Wilcoxon signed-rank |
| Multiple comparisons | Holm correction across 36 planned comparisons |
| Effect size | Rank-biserial correlation |

## Main findings from validated result artifacts

- The frozen 240-row primary CSV was independently revalidated: no missing values, no duplicate experiment keys, zero distractor intrusion, and 100% exact top-5 preservation relative to the corresponding noise-free baseline.
- No Token F1 or semantic-similarity comparison remained significant after Holm correction.
- Dense retrieval at four distractors was the only comparison that remained significant after correction: mean latency increased from 0.405087 s to 0.595432 s (+46.99%), Holm-adjusted p = 0.045628, rank-biserial correlation = 0.761905 (n = 20).
- No LLM evaluations were rerun during validation.
- A separate hard-semantic-distractor dataset is treated as exploratory and is not pooled with the primary experiment.

## Validated publication artifacts

- [Validated Results section](paper/RESULTS_validated.md)
- [Validated statistical analysis](results/statistical_analysis_validated.csv)
- [Validated descriptive summary](results/descriptive_summary_validated.csv)
- [Validated retrieval-stability summary](results/retrieval_stability_validated.csv)
- [Latency figure](figures/fig_latency.svg)
- [Token F1 figure](figures/fig_answer_quality.svg)
- [Semantic-similarity figure](figures/fig_semantic_similarity.svg)
- [Retrieval-stability figure](figures/fig_retrieval_stability.svg)
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

The raw primary CSV is frozen and validated. The validated Results section, statistical tables, and vector publication figures are committed and reconciled with the 36-test statistical family. The manuscript remains an artifact-reconciled draft and should be synchronized with the validated 36-comparison statistical family before camera-ready submission. A clean notebook rerun is still required for a full computational-reproducibility claim.

Exact model identifiers, corpus provenance, package versions, hardware, and timing boundaries should be documented from the notebook/runtime. Do not treat a GitHub commit or release as evidence of peer review or publication. No DOI is claimed unless a Zenodo deposit is completed.

## Citation

See [CITATION.cff](CITATION.cff). Until a DOI is assigned, cite the repository URL and access date.

## References

1. Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS.
2. Robertson & Zaragoza (2009), *The Probabilistic Relevance Framework: BM25 and Beyond*, FnTIR.
3. Karpukhin et al. (2020), *Dense Passage Retrieval for Open-Domain Question Answering*, EMNLP.
4. Wilcoxon (1945), *Individual Comparisons by Ranking Methods*, Biometrics Bulletin.
5. Holm (1979), *A Simple Sequentially Rejective Multiple Test Procedure*, Scandinavian Journal of Statistics.
