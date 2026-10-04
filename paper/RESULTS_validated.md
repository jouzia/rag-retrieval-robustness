# Validated Results

## Primary experiment

The primary experiment comprised 240 observations generated from 20 questions, three retrieval methods (BM25, dense, and hybrid), and four random distractor levels (0, 1, 2, and 4 injected documents), with top-k fixed at 5. The completed raw result set contained no missing values or duplicate experiment keys, and each method-by-noise condition contained 20 observations.

### Retrieval stability

Under the tested random-distractor construction, no injected distractor appeared in the final top-5 retrieval set in any of the 240 observations. Consequently, exact top-5 retrieval preservation relative to each question's noise-free baseline was 100% for BM25, dense retrieval, and hybrid retrieval at every tested noise level. This result is specific to the tested corpus, retrievers, top-k setting, and distractor-generation procedure.

### Answer quality

Mean Token F1 and semantic-similarity scores varied across noise levels, but none of the 18 answer-quality comparisons (9 Token F1 + 9 semantic similarity) remained statistically significant after the planned multiple-comparison correction. The observed changes therefore do not provide evidence of a statistically reliable degradation in answer quality under the tested random-noise conditions.

### Latency

Dense-retrieval latency showed the only statistically significant corrected comparison. At four injected distractors, mean latency increased from 0.405087 s at baseline to 0.595432 s, an absolute increase of 0.190345 s (46.99%). A paired Wilcoxon signed-rank test gave W = 25, raw p = 0.001690; after Holm correction across all 36 planned paired comparisons, adjusted p = 0.045628. The paired rank-biserial correlation was 0.761905 (n = 20).

No other comparison remained significant after Holm correction.

## Statistical analysis

For each retrieval method, metric, and non-zero noise level, the noisy condition was compared with the same question under noise level 0 using a paired Wilcoxon signed-rank test. This produced 36 planned comparisons: 3 retrieval methods × 3 metrics × 3 non-zero noise contrasts. The p-values were corrected jointly using Holm's step-down procedure with alpha = 0.05. Effect magnitude was summarized using paired rank-biserial correlation.

## Interpretation

The primary experiment supports a narrow finding: the tested random distractors did not alter the final top-5 rankings, and they did not produce a statistically significant answer-quality degradation after correction. A statistically significant increase in dense-retrieval latency was observed at the highest tested noise level. These findings characterize the evaluated implementation and experimental conditions rather than establishing universal RAG robustness.
