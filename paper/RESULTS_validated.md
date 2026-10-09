# Validated Results

## Primary experiment: appended-context evaluation

The primary experiment comprised 240 observations generated from 20 questions, three retrieval methods (BM25, dense, and hybrid), and four random distractor levels (0, 1, 2, and 4 injected documents), with top-k fixed at 5. The completed raw result set contained no missing values or duplicate experiment keys, and each method-by-noise condition contained 20 observations.

### Retrieval construction diagnostic

The notebook retrieves the original top-five first, then appends distractors to the context sent to the answer generator. Therefore, zero distractor intrusion into the original retrieved top-five and 100% top-five preservation are guaranteed by construction, not empirical evidence of retrieval robustness. This experiment does not test whether distractors displace documents during retrieval.

### Answer quality

Mean Token F1 and semantic-similarity scores varied across noise levels, but none of the 18 answer-quality comparisons (9 Token F1 + 9 semantic similarity) remained statistically significant after the planned multiple-comparison correction. The observed changes therefore do not provide evidence of a statistically reliable degradation in answer quality under the tested random-noise conditions.

### Generation-call latency

The measured generation-call latency (the timer surrounds `generate_rag_answer`, not isolated retrieval) showed one statistically significant corrected comparison for the dense-method pipeline. At four appended distractors, mean latency increased from 0.405087 s at baseline to 0.595432 s, an absolute increase of 0.190345 s (46.99%). A paired Wilcoxon signed-rank test gave W = 25, raw p = 0.001690; after Holm correction across all 27 planned paired comparisons, adjusted p = 0.045628. The paired rank-biserial correlation was 0.761905 (n = 20).

No other comparison remained significant after Holm correction.

## Statistical analysis

For each retrieval method, metric, and non-zero noise level, the noisy condition was compared with the same question under noise level 0 using a paired Wilcoxon signed-rank test. This produced 27 planned comparisons: 3 retrieval methods × 3 metrics × 3 non-zero noise contrasts. The p-values were corrected jointly using Holm's step-down procedure with alpha = 0.05. Effect magnitude was summarized using paired rank-biserial correlation.

## Interpretation

The primary experiment supports a narrow finding about appended-context distractors: no answer-quality comparison remained significant after correction, while one generation-call latency contrast for the dense-method context was significant. It does not support a retrieval-ranking robustness claim because distractors were added after top-five retrieval. These findings characterize the evaluated implementation and experimental conditions rather than establishing universal RAG robustness.
