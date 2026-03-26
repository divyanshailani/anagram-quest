#!/usr/bin/env python3
"""Quick smoke tests for local anagram model quality."""

from __future__ import annotations

import argparse
from typing import Dict, Set

from run_qwen_local import load_solver_model, normalize_letters, solve_once

TEST_CASES: Dict[str, Set[str]] = {
    "AET": {"ATE", "EAT", "ETA", "TEA"},
    "OPT": {"OPT", "POT", "TOP"},
    "ENOT": {"NOTE", "TONE"},
    "AELT": {"LATE", "TALE", "TEAL"},
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local model smoke tests")
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--max-tokens", type=int, default=120)
    args = parser.parse_args()

    model, tokenizer = load_solver_model(args.model_path)

    passed = 0
    for letters, expected in TEST_CASES.items():
        words, _ = solve_once(model, tokenizer, normalize_letters(letters), args.max_tokens)
        got = set(words)
        ok = bool(got & expected)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {letters} -> {', '.join(words) if words else '(none)'}")
        if ok:
            passed += 1

    total = len(TEST_CASES)
    print(f"\nResult: {passed}/{total} cases passed")
    if passed < total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
