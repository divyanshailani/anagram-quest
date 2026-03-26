#!/usr/bin/env python3
"""Run local MLX-LM anagram inference without OpenEnv/FastAPI.

Example:
  python repro/local_mlx/scripts/run_qwen_local.py \
    --model-path /absolute/path/to/anagram_grpo_mlx
"""

from __future__ import annotations

import argparse
from typing import List, Tuple

_MLX_GENERATE = None

SYSTEM_MSG = (
    "You are an anagram solver. Given scrambled letters, find ALL valid "
    "English words that use every letter exactly once. Return words as "
    "uppercase CSV. No explanation."
)


def normalize_letters(raw: str) -> str:
    """Normalize mixed input such as 't a b' or 'tab' to 'TAB'."""
    return "".join(ch for ch in raw.upper() if ch.isalpha())


def parse_words(response: str) -> List[str]:
    """Parse CSV-like model output into sorted unique uppercase words."""
    text = response.strip()
    if "</think>" in text:
        text = text.split("</think>")[-1].strip()
    first_line = text.splitlines()[0] if text else ""
    words = {w.strip().upper() for w in first_line.split(",") if w.strip()}
    return sorted(words)


def load_solver_model(model_path: str):
    """Load model + tokenizer once."""
    try:
        from mlx_lm import load as mlx_load
    except Exception as exc:  # pragma: no cover - runtime dependency guard
        raise SystemExit(
            "mlx-lm is not installed or failed to import. "
            "Install with: pip install -r repro/local_mlx/requirements.txt\n"
            f"Import error: {exc}"
        )
    print(f"Loading model from: {model_path}")
    model, tokenizer = mlx_load(model_path)
    print("Model loaded.\n")
    return model, tokenizer


def solve_once(
    model,
    tokenizer,
    letters: str,
    max_tokens: int = 120,
) -> Tuple[List[str], str]:
    """Generate one answer for a normalized letter set."""
    global _MLX_GENERATE
    if _MLX_GENERATE is None:
        from mlx_lm import generate as mlx_generate
        _MLX_GENERATE = mlx_generate

    spaced = " ".join(letters)
    messages = [
        {"role": "system", "content": SYSTEM_MSG},
        {"role": "user", "content": f"Unscramble: {spaced}"},
    ]
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    raw = _MLX_GENERATE(model, tokenizer, prompt=prompt, max_tokens=max_tokens)
    return parse_words(raw), raw


def run_interactive(model, tokenizer, max_tokens: int) -> None:
    """Interactive local test loop."""
    print("Type letters (e.g. A E T or AET). Enter 'quit' to stop.\n")
    while True:
        raw = input("letters> ").strip()
        if raw.lower() in {"q", "quit", "exit"}:
            break
        letters = normalize_letters(raw)
        if not letters:
            print("No letters detected. Try again.\n")
            continue

        words, model_raw = solve_once(model, tokenizer, letters, max_tokens)
        print(f"normalized: {letters}")
        print(f"words: {', '.join(words) if words else '(none)'}")
        print(f"raw: {model_raw.strip()}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run local MLX-LM anagram inference without OpenEnv",
    )
    parser.add_argument(
        "--model-path",
        required=True,
        help="Path to MLX model folder (e.g. anagram_grpo_mlx)",
    )
    parser.add_argument(
        "--letters",
        default="",
        help="Optional one-shot letters input (e.g. 'A E T')",
    )
    parser.add_argument("--max-tokens", type=int, default=120)
    args = parser.parse_args()

    model, tokenizer = load_solver_model(args.model_path)

    if args.letters:
        letters = normalize_letters(args.letters)
        if not letters:
            raise SystemExit("No valid letters provided in --letters")
        words, model_raw = solve_once(model, tokenizer, letters, args.max_tokens)
        print(f"normalized: {letters}")
        print(f"words: {', '.join(words) if words else '(none)'}")
        print(f"raw: {model_raw.strip()}")
        return

    run_interactive(model, tokenizer, args.max_tokens)


if __name__ == "__main__":
    main()
