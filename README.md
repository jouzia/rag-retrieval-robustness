# Evaluating Retrieval Robustness in RAG Systems Under Increasing Distractor Noise

**Author:** Shaik Jouzia Afreen H  
**Area:** Retrieval-Augmented Generation (RAG), information retrieval, NLP

This repository studies how injected distractor documents affect retrieval stability, answer-quality metrics, and latency for BM25, dense, and hybrid retrieval.

> **Scope note:** Findings apply only to the tested corpus, implementation, distractor construction, top-k setting, and noise levels. They do not establish universal robustness. See the limitations in the manuscript.

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
| Multiple comparisons | Holm correction |
| Effect size | Rank-biserial correlation |

## Main findings from supplied result artifacts

- The supplied primary summary reports zero injected-distractor contamination and baseline top-five preservation of 1.0 in all tested method/noise conditions.
- No answer-quality comparison remained significant after Holm correction.
- Dense retrieval at four distractors was the only comparison reported to remain significant after correction: baseline mean 0.405087 s, noisy mean 0.595432 s, change +46.99%, Holm-adjusted p = 0.045628, rank-biserial correlation = 0.761905 (n = 20).
- A separate hard-semantic-distractor dataset is treated as exploratory and is not pooled with the primary experiment.


## Primary experiment validation

The frozen 240-row primary CSV has been independently revalidated from the raw observations. The authoritative validation is documented in [VALIDATION.md](VALIDATION.md).

- 240 observations: 20 questions × 3 methods × 4 noise levels.
- No missing values or duplicate experiment keys.
- No injected distractor entered the final top-5 in any observation.
- All noisy top-5 rankings matched their corresponding noise-0 baseline.
- Across the 36 planned paired comparisons (3 methods × 3 metrics × 3 noise contrasts), only dense-retrieval latency at 4 distractors remained significant after joint Holm correction: 0.405087 s → 0.595432 s, +46.99%, adjusted p = 0.045628, rank-biserial correlation = 0.761905.
- No token-F1 or semantic-similarity comparison remained significant after Holm correction.
- No LLM evaluations were rerun during this validation.

## Repository map

- [Full manuscript draft](paper/manuscript.md)
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

**Artifact note:** The notebook, manuscript, and CSV artifacts are committed. The generated PNG figures and a typeset PDF are not yet committed in this revision; the Markdown manuscript is the current readable paper source.

## Reproducibility and artifact status

The notebook is the executable source; CSV summaries are derived artifacts. Before journal/conference submission, rerun the notebook from a clean environment and reconcile the generated outputs with the committed result files. Exact model identifiers, corpus provenance, package versions, hardware, and timing boundaries should be documented from the notebook/runtime.

The current repository includes a manuscript draft and transparent summary tables. Do not treat a GitHub commit or release as evidence of peer review or publication. No DOI is claimed unless a Zenodo deposit is completed.

## Citation

See [CITATION.cff](CITATION.cff). Until a DOI is assigned, cite the repository URL and access date.

## References

1. Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS.
2. Robertson & Zaragoza (2009), *The Probabilistic Relevance Framework: BM25 and Beyond*, FnTIR.
3. Karpukhin et al. (2020), *Dense Passage Retrieval for Open-Domain Question Answering*, EMNLP.
4. Wilcoxon (1945), *Individual Comparisons by Ranking Methods*, Biometrics Bulletin.
5. Holm (1979), *A Simple Sequentially Rejective Multiple Test Procedure*, Scandinavian Journal of Statistics.
