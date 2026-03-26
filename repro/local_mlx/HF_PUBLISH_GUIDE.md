# Hugging Face Weights Publish Guide

Use this guide to publish local model weights cleanly without bloating this GitHub repo.

## Recommended Model Repos

Use clear names, for example:

- `divyanshailani/anagram-quest-qwen3-0.6b-grpo-mlx`
- `divyanshailani/anagram-quest-qwen3-0.6b-grpo-hf`

## 1) Prerequisites

```bash
pip install -U huggingface_hub
huggingface-cli login
git lfs install
```

## 2) Create a Model Repo

```bash
huggingface-cli repo create anagram-quest-qwen3-0.6b-grpo-mlx --type model
```

## 3) Clone the HF Model Repo

```bash
git clone https://huggingface.co/divyanshailani/anagram-quest-qwen3-0.6b-grpo-mlx
cd anagram-quest-qwen3-0.6b-grpo-mlx
```

## 4) Copy Weights + Tokenizer Files

```bash
cp -R /absolute/path/to/anagram_grpo_mlx/* .
```

Do not include random local artifacts like logs or temp files.

## 5) Add Model Card

```bash
cp /absolute/path/to/anagram-quest/repro/local_mlx/HF_MODEL_CARD_TEMPLATE.md README.md
```

Then edit `README.md` and fill real metrics, intended use details, and limitations.

## 6) Commit and Push

```bash
git add .
git commit -m "Release Anagram Quest Qwen3-0.6B GRPO weights"
git push
```

## 7) Link Back to Master Repo

After push, add your final HF model URL to:

- `repro/local_mlx/README.md`
- top-level `README.md` in this repo

## Security Checklist

- Never commit API tokens.
- Never commit private datasets unless licensed and scrubbed.
- Keep personal paths out of the final model card.
