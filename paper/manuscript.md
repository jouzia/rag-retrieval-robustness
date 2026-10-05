# Evaluating Retrieval Robustness in RAG Systems Under Increasing Distractor Noise

**Author:** Shaik Jouzia Afreen H  
**Research area:** Retrieval-Augmented Generation (RAG), information retrieval, natural language processing  
**Study type:** Controlled computational evaluation  
**Version:** Manuscript v1.0 (artifact-reconciled draft)

## Abstract

Retrieval-Augmented Generation (RAG) systems depend on retrieval to supply evidence to downstream language generation. Irrelevant documents may increase the candidate pool and potentially alter retrieved context, answer quality, or latency. This study evaluates BM25, dense, and hybrid retrieval across 20 questions and four distractor conditions (0, 1, 2, and 4 injected documents), with a fixed top-k of five. The primary experiment contains 240 method-condition observations. Retrieval stability is assessed using distractor contamination and preservation of the baseline top-five set; answer quality is assessed using token-level F1 and semantic similarity; and latency is measured in seconds. Each non-zero noise condition is compared with its matched baseline using paired Wilcoxon signed-rank tests, with Holm correction across 36 comparisons.

In the supplied primary results, no injected distractor appears in the final top-five results and baseline top-five preservation is reported as 1.0 across tested conditions. The only comparison reported as statistically significant after Holm correction is dense-retrieval latency at four distractors: mean latency rises from 0.405087 s to 0.595432 s (+0.190345 s; +46.99%; Holm-adjusted p = 0.045628; rank-biserial correlation = 0.761905; n = 20). No answer-quality comparison remains significant after correction. These findings are limited to the evaluated corpus, implementation, distractor construction, and noise range. The absence of contamination under this construction should not be interpreted as universal RAG robustness.

**Keywords:** retrieval-augmented generation, BM25, dense retrieval, hybrid retrieval, distractor noise, retrieval stability, latency, Wilcoxon signed-rank test

## 1. Introduction

Retrieval-Augmented Generation combines a retrieval component with a language model that generates responses conditioned on retrieved evidence. The retrieval stage constrains what evidence is available to the generator; changes to the selected documents can therefore affect grounding and answer quality. Retrieval systems operate against candidate collections that may include irrelevant or misleading material, making robustness to distractor documents a practical evaluation concern.

Sparse lexical retrieval such as BM25 ranks documents using term statistics. Dense retrieval ranks representations using embedding-space similarity, while hybrid retrieval combines lexical and semantic signals. These methods may respond differently to an expanded candidate environment. Noise may change the top-k context, affect generated answers, or increase computational work even when the final context remains unchanged.

This study examines these outcomes separately. It evaluates whether injected distractors enter the final top-five results, whether the baseline top-five set is preserved, whether answer-quality metrics change, and whether latency changes as distractor count increases.

## 2. Research question and hypotheses

**RQ1:** How does increasing distractor-document noise affect retrieval stability, generated-answer quality, and latency in BM25, dense, and hybrid retrieval systems within a RAG pipeline?

- **H1 — Retrieval stability:** Increasing distractor noise reduces stability of the final top-five results.
- **H2 — Answer quality:** Increasing distractor noise negatively affects generated-answer quality.
- **H3 — Latency:** Increasing distractor noise increases retrieval/processing latency.

These are empirical hypotheses evaluated within the specific experimental setup, not claims about all RAG systems.

## 3. Methods

### 3.1 Design

The primary experiment crosses 20 evaluation questions with three retrieval methods (BM25, dense, hybrid) and four noise levels (0, 1, 2, 4 distractors), yielding 20 observations per method-condition cell and 240 observations overall. The top-k retrieval limit is five. Distractor sampling uses seed 42. Each noisy result is paired with the corresponding zero-noise result for the same question and retrieval method.

The stated noise ratios are 0.0000, 0.1667, 0.2857, and 0.4444. These ratios are specific to the experiment's candidate-set construction and should not be generalized to other corpus sizes.

### 3.2 Retrieval methods

- **BM25:** sparse lexical retrieval based on term-frequency and inverse-document-frequency statistics.
- **Dense retrieval:** embedding-based semantic retrieval.
- **Hybrid retrieval:** combination of lexical and semantic retrieval signals.

The manuscript describes these method families. Exact implementation details (model identifiers, embedding model, hybrid fusion method, corpus provenance, and software versions) should be documented from the executable notebook before a camera-ready or journal submission.

### 3.3 Distractor construction

The primary experiment injects 0, 1, 2, or 4 distractor documents. Distractors are sampled from documents outside the baseline top-five set. The final retrieved context is limited to five documents. Consequently, the experiment tests whether these injected documents displace baseline top-five documents under this construction; it does not fully test adversarial or semantically confusable distractors.

### 3.4 Outcomes

- **Distractor contamination:** fraction of documents in the final top-five result that are injected distractors.
- **Baseline top-five preservation:** fraction of the baseline top-five document set retained under noise.
- **Token F1:** token-level overlap between generated and reference answers.
- **Semantic similarity:** semantic correspondence between generated and reference answers, as implemented in the notebook.
- **Latency:** elapsed time recorded by the experimental pipeline, in seconds. The exact timing boundary should be confirmed from notebook code before external publication.

### 3.5 Statistical analysis

Each non-zero noise condition is paired with the zero-noise baseline for the same question and method. The stated analysis uses paired Wilcoxon signed-rank tests, Holm correction for family-wise error across 36 comparisons (3 methods × 3 non-zero noise levels × 3 metrics), and rank-biserial correlation as an effect-size measure. The significance threshold is α = 0.05. The reported adjusted p-value is interpreted after Holm correction.

## 4. Results

The primary experiment contains 240 observations. The inferential family comprises 36 planned paired comparisons (3 methods × 3 metrics × 3 non-zero noise contrasts), corrected jointly using Holm's step-down procedure.

### 4.1 Retrieval stability

![Retrieval stability under random distractors](../figures/fig_retrieval_stability.svg)

The supplied primary experiment summary reports zero injected-distractor contamination and baseline top-five preservation of 1.0 for all three methods and all tested noise conditions. Thus, within the tested setup, none of the injected distractors entered the final top-five set and the baseline set was preserved.

This is a bounded result: it may reflect the distractor sampling strategy and retrieval configuration. It does not establish that the methods will resist semantically similar, adversarial, duplicated, or higher-volume distractors.

### 4.2 Latency

![Mean latency by distractor level](../figures/fig_latency.svg)

The supplied summary gives the following mean latency values:

| Method | 0 distractors (s) | 1 (s) | 2 (s) | 4 (s) | Change at 4 |
|---|---:|---:|---:|---:|---:|
| BM25 | 0.4628 | 0.4381 | 0.4945 | 0.4871 | +5.25% |
| Dense | 0.4051 | 0.4743 | 0.5096 | 0.5954 | +46.99% |
| Hybrid | 0.4248 | 0.4769 | 0.5090 | 0.5219 | +22.86% |

Relative changes are calculated from the displayed rounded means, so they may differ slightly from calculations using unrounded observations.

The only comparison reported as surviving Holm correction is dense retrieval at four distractors:

| Statistic | Value |
|---|---:|
| Baseline mean | 0.405087 s |
| Four-distractor mean | 0.595432 s |
| Absolute change | +0.190345 s |
| Relative change | +46.99% |
| Wilcoxon statistic | 25.0 |
| Raw p-value | 0.001690 |
| Holm-adjusted p-value | 0.045628 |
| Rank-biserial correlation | 0.761905 |
| Paired observations | 20 |

The adjusted p-value is below 0.05, but close to the threshold. The result should be interpreted with the small sample size, multiple-comparison procedure, and environment-dependent timing in mind.

### 4.3 Answer quality

![Mean Token F1 by distractor level](../figures/fig_answer_quality.svg)

![Mean semantic similarity by distractor level](../figures/fig_semantic_similarity.svg)

The supplied descriptive summary shows non-monotonic answer-quality means across noise levels. No Token F1 or semantic-similarity comparison is reported as significant after Holm correction across the complete 36-test family. The available evidence therefore does not support a systematic degradation claim for answer quality in the primary experiment.

Because the retrieved top-five sets reportedly remain unchanged, answer-quality differences cannot be attributed to distractors replacing documents in the final retrieved context under this experiment.

### 4.4 Hypothesis assessment

- **H1:** Not supported in the tested conditions; no top-five contamination or loss of baseline documents was reported.
- **H2:** Not supported by the corrected inferential results; no answer-quality comparison remained significant after Holm correction.
- **H3:** Partially supported. Mean latency at four distractors was higher for all three methods, but only the dense-retrieval comparison was reported as significant after correction.

## 5. Separate exploratory hard-distractor experiment

A separate hard-semantic-distractor results file contains 80 observations. Its descriptive answer-quality means are:

| Distractors | Token F1 | Semantic similarity |
|---:|---:|---:|
| 0 | 0.2716 | 0.5538 |
| 1 | 0.1878 | 0.4518 |
| 2 | 0.2339 | 0.4866 |
| 4 | 0.1843 | 0.4662 |

These descriptive values suggest lower means in noisy conditions than at baseline, but the pattern is not strictly monotonic. They are not pooled with the 240-observation primary experiment. Until the hard-distractor experiment's design, pairing, metrics, and corrected inferential tests are independently verified, these numbers should be treated as exploratory and not as confirmatory evidence.

## 6. Discussion

The primary experiment's clearest reported result is a latency increase for dense retrieval at the highest tested noise level. The retrieval-stability measures remained unchanged, and answer-quality comparisons did not survive multiple-comparison correction. The results therefore distinguish ranking stability from computational cost: stable top-k outputs do not imply that processing cost is unaffected.

The result is not evidence that dense retrieval is generally more sensitive than BM25 or hybrid retrieval; the analysis tests within-method changes against each method's baseline, not direct between-method differences. Further, latency is implementation- and environment-dependent. The measured increase may reflect candidate processing, embedding/search implementation, caching, or other pipeline details; attribution requires profiling and precise timing boundaries.

The hard-distractor experiment is potentially useful as a follow-up because it changes the distractor difficulty. It should remain a separately documented experiment until its notebook cells, data construction, and inferential analysis are validated.

## 7. Limitations and validity threats

1. **Small question set:** 20 questions may not represent broader query distributions.
2. **Limited noise range:** only 0, 1, 2, and 4 distractors were evaluated.
3. **Distractor difficulty:** sampling outside the baseline top-five set may yield distractors that are not sufficiently competitive.
4. **Fixed top-k:** results may differ for other context budgets.
5. **Implementation specificity:** exact models, corpus provenance, indexing settings, fusion strategy, hardware, package versions, and timing boundaries must be reported for reproducibility.
6. **Answer metrics:** token F1 and semantic similarity do not fully measure factuality, citation correctness, faithfulness, or usefulness.
7. **Multiple testing:** Holm correction controls family-wise error for the stated family, but the single significant result is near α = 0.05 and should be replicated.
8. **No between-method test:** the study does not establish that one retrieval method is better than another.
9. **Hard-noise extension:** the exploratory file requires a separate, fully documented analysis.
10. **Artifact reconciliation:** this manuscript uses the supplied corrected statistical summary; the notebook should be rerun in a clean environment and its outputs compared with committed CSVs before claiming full computational reproducibility.

## 8. Conclusion

In a controlled evaluation of 20 questions, three retrieval methods, and four distractor levels, the supplied primary results report unchanged top-five retrieval sets and no injected-distractor contamination. Answer-quality metrics did not show statistically significant changes after Holm correction. Dense-retrieval latency at four distractors increased from 0.405087 s to 0.595432 s (+46.99%) and was the only comparison reported to remain significant after correction (adjusted p = 0.045628; rank-biserial correlation = 0.761905).

The conclusion is deliberately scoped: under this particular corpus, implementation, distractor construction, and noise range, top-five ranking stability was maintained while dense-retrieval latency increased. Stronger claims require larger and more diverse datasets, harder distractors, multiple runs and environments, explicit between-method analyses, and a fully reproducible notebook-to-artifact audit.

## 9. Reproducibility checklist

Before submitting to a journal or conference, record and publish:
- dataset/corpus source and license;
- question and reference-answer provenance;
- exact sparse, dense, and hybrid implementation details;
- embedding model and model version;
- distractor selection algorithm and random seed;
- package and runtime versions;
- hardware/runtime environment;
- exact timing boundary and warm-up/caching policy;
- metric implementation and semantic-similarity model;
- all 36 paired test outputs and Holm-adjusted p-values;
- clean rerun logs and checksums for committed artifacts.

## References

1. Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *Advances in Neural Information Processing Systems*, 33.
2. Robertson, S., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. *Foundations and Trends in Information Retrieval*, 3(4), 333–389.
3. Karpukhin, V. et al. (2020). Dense Passage Retrieval for Open-Domain Question Answering. *Proceedings of EMNLP 2020*, 6769–6781.
4. Wilcoxon, F. (1945). Individual Comparisons by Ranking Methods. *Biometrics Bulletin*, 1(6), 80–83.
5. Holm, S. (1979). A Simple Sequentially Rejective Multiple Test Procedure. *Scandinavian Journal of Statistics*, 6(2), 65–70.

## Data and code availability

The executable notebook is hosted at [Kaggle](https://www.kaggle.com/code/shaikjouziaafreenh/rag-retrieval-robustness-study). The repository's results directory is intended to contain the CSV outputs used for the reported tables. The manuscript should be considered an artifact-reconciled draft until a clean notebook rerun confirms all committed outputs.
