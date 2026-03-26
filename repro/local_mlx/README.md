# Local MLX Repro Pack (No OpenEnv Needed)

This folder lets anyone test the fine-tuned Qwen anagram model locally without running the full OpenEnv/FastAPI game stack.

## Included Files

- `scripts/run_qwen_local.py` - interactive/one-shot local inference runner.
- `scripts/smoke_test.py` - quick quality sanity test against known anagrams.
- `scripts/generate_dataset_v2.py` - diverse dataset generator used for training prep.
- `scripts/grpo_colab_pipeline.py` - Colab cell-by-cell SFT -> GRPO training pipeline script.
- `notebooks/Anagram_quest_Qwen_3_0.6B_retuned.ipynb` - Qwen retuning notebook.
- `notebooks/word_guess_model_SFT_GRPO.ipynb` - SFT/GRPO notebook variant.

## Quickstart (macOS Apple Silicon)

1. Create and activate a virtual environment.

```bash
cd repro/local_mlx
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run one-shot inference.

```bash
python scripts/run_qwen_local.py \
  --model-path /absolute/path/to/anagram_grpo_mlx \
  --letters "A E T"
```

3. Run interactive mode.

```bash
python scripts/run_qwen_local.py \
  --model-path /absolute/path/to/anagram_grpo_mlx
```

4. Run smoke tests.

```bash
python scripts/smoke_test.py \
  --model-path /absolute/path/to/anagram_grpo_mlx
```

## Dataset + Training Assets

Generate diverse training data locally:

```bash
python scripts/generate_dataset_v2.py
```

Use notebook artifacts for Colab-based experimentation:

- `notebooks/Anagram_quest_Qwen_3_0.6B_retuned.ipynb`
- `notebooks/word_guess_model_SFT_GRPO.ipynb`

Use script-style Colab pipeline (copy section-by-section):

```bash
python scripts/grpo_colab_pipeline.py
```

## Publishing Rules

Keep this folder lightweight and reproducible:

- Do commit scripts, configs, and notebooks.
- Do not commit model binaries/checkpoints (`*.safetensors`, `*.pt`, `*.bin`).
- Do not commit private credentials/tokens.

Model weights can be shared separately via Hugging Face model repos or release assets.
