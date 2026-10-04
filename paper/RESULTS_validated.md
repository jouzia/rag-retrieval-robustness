# Results

## Primary experiment

The primary experiment comprised 240 observations generated from 20 questions, three retrieval methods (BM25, dense, and hybrid), and four random distractor levels (0, 1, 2, and 4 injected documents), with top-k fixed at 5. The completed raw result set contained no missing values or duplicate experiment keys, and each method-by-noise condition contained 20 observations.

### Retrieval stability

Under the tested random-distractor construction, no injected distractor appeared in the final top-5 retrieval set in any of the 240 observations. Consequently, exact top-5 retrieval preservation relative to each question's noise-free baseline was 100% for BM25, dense retrieval, and hybrid retrieval at every tested noise level. This result describes the tested corpus, retrievers, top-k setting, and distractor-generation procedure; it should not be generalized to other distractor distributions or retrieval systems.

### Answer quality

Mean Token F1 and semantic-similarity scores varied across noise levels, but none of the 18 method-by-noise comparisons for the two answer-quality metrics remained statistically significant after the planned multiple-comparison correction. The observed changes therefore do not provide evidence of a statistically reliable degradation in answer quality under the tested random-noise conditions.

### Latency

Latency showed a different pattern for dense retrieval. At four injected distractors, mean dense-retrieval latency increased from 0.405087 s at baseline to 0.595432 s, an absolute increase of 0.190345 s (46.99%). A paired Wilcoxon signed-rank test gave W = 25, p = 0.001690; after Holm correction across the 36 planned paired comparisons, p = 0.045628. The paired rank-biserial correlation was 0.761905 (n = 20). This was the only comparison that remained significant after correction.

Dense-retrieval latency at two distractors also increased descriptively, but it did not remain significant after Holm correction. BM25 and hybrid latency comparisons likewise did not remain significant after correction.

## Statistical analysis

For each retrieval method, metric, and non-zero noise level, the noisy condition was compared with the same question under noise level 0 using a paired Wilcoxon signed-rank test. The resulting 36 p-values (3 methods × 3 metrics × 3 noise contrasts) were corrected jointly using Holm's step-down procedure with α = 0.05. Effect magnitude was summarized using paired rank-biserial correlation.

## Interpretation

The primary experiment supports a narrow finding: the tested random distractors did not alter the final top-5 rankings, and they did not produce a statistically significant answer-quality degradation after correction. A statistically significant increase in dense-retrieval latency was observed at the highest tested noise level. These findings characterize the evaluated implementation and experimental conditions rather than establishing universal RAG robustness.
