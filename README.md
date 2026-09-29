# Evaluating Retrieval Robustness in RAG Systems Under Increasing Distractor Noise

Research study by **Shaik Jouzia Afreen H**. 

This repository contains the reproducible research artifacts for evaluating how increasing distractor-document noise affects retrieval stability, answer quality, and latency in Retrieval-Augmented Generation (RAG) systems.

## Research Question

**RQ1:** How does increasing distractor-document noise affect retrieval stability, generated-answer quality, and latency in BM25, dense, and hybrid retrieval systems within a RAG pipeline?

## Hypotheses

- **H1:** Increasing distractor noise will reduce retrieval stability.
- **H2:** Increasing distractor noise will negatively affect generated-answer quality.
- **H3:** Increasing distractor noise will increase computational latency.

## Experimental Design

| Parameter | Configuration |
|---|---|
| Evaluation questions | 20 |
| Retrieval methods | BM25, Dense, Hybrid |
| Noise levels | 0, 1, 2, 4 injected distractors |
| Top-k | 5 |
| Total observations | 240 |
| Distractor sampling seed | 42 |
| Baseline | 0 injected distractors |
| Statistical test | Paired Wilcoxon signed-rank |
| Multiple-comparison correction | Holm correction |
| Effect size | Rank-biserial correlation |

The study evaluates 20 questions across 3 retrieval methods and 4 noise conditions, producing 240 method-condition observations.

## Retrieval Stability

Retrieval stability is evaluated using:

1. **Distractor contamination** — proportion of final top-5 retrieved documents that are injected distractors.
2. **Baseline top-5 preservation** — proportion of the baseline top-5 document set retained under each noisy condition.

These measures avoid treating an earlier implementation artifact as conventional context recall.

## Evaluation

Answer quality is evaluated using:

- Token-level F1
- Semantic similarity

Latency is recorded for the retrieval/generation evaluation pipeline used in the experiment.

For statistical testing, each noisy condition is compared with its matched zero-noise baseline for the same question and retrieval method. Multiple comparisons are controlled using Holm correction.

## Repository Structure

```text
rag-retrieval-robustness/
├── README.md
├── paper/
│   └── Evaluating_Retrieval_Robustness.pdf
├── figures/
│   ├── fig1_contamination.png
│   ├── fig2_preservation.png
│   ├── fig3_answer_quality.png
│   └── fig4_latency.png
├── results/
│   ├── experiment_summary.csv
│   ├── retrieval_summary.csv
│   └── statistical_analysis.csv
└── notebook/
    └── rag-retrieval-robustness-study.ipynb
```

The binary research artifacts will be added from the verified experimental run. No result values are fabricated or substituted with placeholders.

## Reproducibility

The executable experiment is maintained in Kaggle:

**Kaggle Notebook:** https://www.kaggle.com/code/shaikjouziaafreenh/rag-retrieval-robustness-study

The final repository will contain the paper, generated figures, result tables, and the corresponding notebook so that the research claim can be inspected from both the written report and executable experiment.

## Scientific Scope

The term "robustness" in this study is scoped to the evaluated corpus, retrieval configuration, distractor-generation procedure, and tested noise levels. The experiment is not intended to establish universal robustness of RAG systems.

In particular, distractors are constructed outside the baseline retrieved top-k set. Therefore, if distractors do not enter the final top-k, changes in answer quality cannot be interpreted as evidence that retrieved-context contamination caused those changes.

Future extensions should evaluate larger question sets, higher noise levels, semantically harder or adversarial distractors, and conditions in which distractors directly compete with relevant documents for top-k positions.

## Status

**Research repository — experimental artifacts being finalized.**
