---
language:
- en
license: apache-2.0
library_name: mlx-lm
base_model: Qwen/Qwen3-0.6B
tags:
- anagram
- word-game
- qwen3
- mlx
- grpo
- sft
---

# Anagram Quest Qwen3-0.6B (GRPO Retuned)

## Model Summary

A task-specialized anagram solver fine-tuned from `Qwen/Qwen3-0.6B` for the Anagram Quest project.

- Base model: `Qwen/Qwen3-0.6B`
- Training style: SFT warmup + GRPO-style reinforcement pass
- Primary use case: find all valid anagrams from a scrambled letter set

## Intended Use

- Educational demos of lightweight task-specific fine-tuning
- Local game inference for Anagram Quest-like mechanics
- Controlled experiments in small-domain lexical reasoning

## Out-of-Scope Use

- General-purpose chat assistant behavior
- High-stakes decision-making domains
- Production use without independent evaluation and guardrails

## Prompt Format

System prompt:

```text
You are an anagram solver. Given scrambled letters, find ALL valid English words that use every letter exactly once. Return words as uppercase CSV. No explanation.
```

User prompt pattern:

```text
Unscramble: A E T
```

Expected output pattern:

```text
ATE, EAT, ETA, TEA
```

## Training Data

This model was trained using synthetic anagram QA style samples derived from curated anagram groups plus expanded dictionary-driven groups.

Primary scripts/notebooks:

- `repro/local_mlx/scripts/generate_dataset_v2.py`
- `repro/local_mlx/scripts/grpo_colab_pipeline.py`
- `repro/local_mlx/notebooks/Anagram_quest_Qwen_3_0.6B_retuned.ipynb`
- `repro/local_mlx/notebooks/word_guess_model_SFT_GRPO.ipynb`

## Evaluation Snapshot

Replace this section with your real metrics before public launch.

Suggested metrics:

- Exact-set match rate on held-out anagram groups
- Top-k recall of valid words
- Invalid word rate
- Duplicate output rate
- Average latency on Apple Silicon

## Inference

### Option A: Repository helper script

```bash
python repro/local_mlx/scripts/run_qwen_local.py \
  --model-path /path/to/this/model \
  --letters "A E T"
```

### Option B: `mlx-lm` direct

```python
from mlx_lm import load, generate

model, tokenizer = load("/path/to/model")
prompt = "Unscramble: A E T"
print(generate(model, tokenizer, prompt=prompt, max_tokens=120))
```

## Limitations

- Performance degrades on letter sets out of distribution.
- May miss rare dictionary words depending on training coverage.
- Can output partial or reordered subsets if prompt deviates from expected format.

## Ethical and Safety Notes

This model is intended for game/task assistance and educational research. It should not be used for safety-critical decision support.

## Citation

```bibtex
@misc{anagramquest_qwen3_2026,
  title={Anagram Quest Qwen3-0.6B GRPO Retuned},
  author={Divyansh Ailani},
  year={2026},
  howpublished={Hugging Face Model Hub}
}
```
