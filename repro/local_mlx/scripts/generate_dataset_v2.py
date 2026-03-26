"""
Diverse Anagram Dataset Generator v2 — Gemini's Approach

Uses macOS /usr/share/dict/words (235K words) to discover THOUSANDS
of real anagram groups, not just the 109 game groups.

Strategy:
  1. Load all English words from system dictionary
  2. Filter to 3-7 letters, lowercase, alpha-only
  3. Group by sorted letters → find natural anagram groups (2+ words)
  4. PRIORITIZE game groups (30 shuffles each) so the model knows them
  5. ADD diverse dictionary groups (10 shuffles each) for generalization
  6. Target: ~5,000 high-quality examples

Output: data/train.jsonl, data/valid.jsonl, data/test.jsonl
"""

import json
import random
import os
from collections import defaultdict

# ─── GAME ANAGRAM_GROUPS (the ones the model MUST know) ───
GAME_GROUPS = {
    # Level 1: 3-letter
    "ABT": ["BAT", "TAB"], "ACT": ["ACT", "CAT"],
    "AET": ["ATE", "EAT", "TEA", "ETA"], "APT": ["APT", "TAP", "PAT"],
    "ART": ["ART", "RAT", "TAR"], "ADM": ["DAM", "MAD"],
    "AMP": ["AMP", "MAP"], "ANP": ["NAP", "PAN"],
    "ANT": ["ANT", "TAN"], "APS": ["SAP", "SPA", "ASP"],
    "AEL": ["ALE", "LEA"], "DEN": ["DEN", "END"],
    "GNU": ["GNU", "GUN", "NUG"], "NOW": ["NOW", "OWN", "WON"],
    "OPT": ["OPT", "TOP", "POT"], "ORT": ["ROT", "TOR"],
    "DGO": ["DOG", "GOD"], "LOW": ["OWL", "LOW"],
    "ENT": ["NET", "TEN"], "INP": ["PIN", "NIP"],
    "IPS": ["SIP", "PSI"], "EST": ["SET"],
    # Level 2: 4-letter
    "ACRS": ["CARS", "SCAR", "ARCS"], "ACST": ["CATS", "CAST", "ACTS", "SCAT"],
    "AELP": ["PALE", "LEAP", "PLEA", "PEAL"],
    "AELR": ["REAL", "EARL"], "AELS": ["SALE", "SEAL", "ALES"],
    "AELT": ["LATE", "TALE", "TEAL"],
    "AEMN": ["NAME", "MEAN", "MANE", "AMEN"],
    "AENR": ["NEAR", "EARN"], "AEPS": ["PEAS", "APES"],
    "AEPT": ["TAPE", "PEAT", "PATE"], "AERW": ["WEAR", "WARE"],
    "ALPS": ["SLAP", "LAPS", "ALPS", "PALS"],
    "ANPS": ["SNAP", "SPAN", "NAPS", "PANS"],
    "ARST": ["STAR", "RATS", "ARTS", "TARS"],
    "DEIS": ["SIDE", "DIES", "IDES"], "EILS": ["LIES", "ISLE"],
    "EIST": ["SITE", "TIES"], "ENOT": ["NOTE", "TONE"],
    "EORS": ["ROSE", "ORES", "SORE"],
    "OPST": ["STOP", "POST", "TOPS", "SPOT", "OPTS", "POTS"],
    "ORST": ["SORT", "ROTS"], "ILNO": ["LOIN", "LION"],
    "ADEL": ["DALE", "DEAL", "LEAD"],
    "AMST": ["MAST", "MATS", "TAMS"],
    "EILV": ["VILE", "LIVE", "EVIL", "VEIL"],
    "GINS": ["SING", "SIGN", "GINS"],
    "ADEM": ["MADE", "DAME", "MEAD"],
    "ADER": ["DARE", "READ", "DEAR"],
    "AEGM": ["GAME", "MAGE"], "AELM": ["MALE", "LAME", "MEAL"],
    "AMOR": ["ROAM", "MORA"], "AGIN": ["GAIN"],
    # Level 3: 5-letter
    "AELPS": ["LEAPS", "PALES", "SEPAL", "PEALS", "PLEAS"],
    "AELRT": ["LATER", "ALTER", "ALERT"],
    "AELST": ["STEAL", "TALES", "STALE", "LEAST", "SLATE"],
    "AENRS": ["SNARE", "EARNS", "NEARS", "SANER"],
    "AEPRS": ["SPARE", "SPEAR", "PARSE", "PEARS", "REAPS"],
    "AEGRS": ["GEARS", "RAGES", "SAGER"],
    "AILNS": ["NAILS", "SNAIL", "SLAIN"],
    "AINRT": ["TRAIN", "INTRA"],
    "DEIRS": ["RIDES", "SIRED", "DRIES"],
    "AELNP": ["PENAL", "PANEL", "PLANE"],
    "EILPS": ["PILES", "PLIES", "SPIEL"],
    "EINPS": ["PINES", "SPINE", "SNIPE"],
    "EINRS": ["REINS", "RINSE", "SIREN", "RISEN"],
    "EINST": ["INSET", "STEIN", "TINES"],
    "EORST": ["STORE", "ROTES", "TORES"],
    "ERSTW": ["STREW", "WREST"],
    "AILRT": ["TRAIL", "TRIAL"],
    "ADELS": ["DEALS", "LEADS", "DALES"],
    "AELNS": ["LANES", "LEANS"],
    "DEIST": ["DIETS", "EDITS", "TIDES", "SITED"],
    "ADEMS": ["MEADS", "DAMES"],
    # Level 4: 6-letter
    "AELRST": ["STELAR", "ALERTS", "ALTERS", "SLATER"],
    "AEINRS": ["ARISEN", "SARNIE"],
    "ADEIRS": ["RAISED", "DARIES"],
    "AEGNRS": ["RANGES", "ANGERS"],
    "DEISTU": ["SUITED", "DUTIES"],
    "EINORS": ["SENIOR", "IRONES"],
    "AEGLNS": ["ANGLES", "GLEANS"],
    "AEINST": ["TISANE", "INSEAT"],
    "AEPRST": ["PASTER", "REPAST"],
    "ACENRS": ["CANERS", "CRANES", "NACRES"],
    "AEGNRT": ["GARNET", "ARGENT"],
    "AELRSV": ["SALVER", "VELARS", "LAVERS"],
    "DEGINS": ["DESIGN", "SIGNED", "SINGED"],
    "AGINST": ["GIANTS", "SATING"],
    "DEINRS": ["DINERS", "RINSED"],
    "AEMNST": ["STAMEN", "AMENTS", "MANTES"],
    "EILNST": ["LISTEN", "SILENT", "TINSEL", "ENLIST"],
    "EINPRS": ["SNIPER", "RIPENS"],
    "AEGINR": ["EARING", "GAINER", "REGAIN"],
    # Level 5: 7-letter
    "AEILNRS": ["ALINERS", "NAILERS"],
    "AEINRST": ["NASTIER", "RETAINS", "STAINER"],
    "ADEINRS": ["SARDINE", "RANDIES"],
    "AEGINRS": ["SEARING", "ERASING", "REGAINS"],
    "AELPRST": ["PLASTER", "PSALTER", "STAPLER"],
    "AEIORST": ["OARIEST"],
    "AEILNST": ["SALTINE", "ELASTIN", "ENTAILS"],
    "ACEIRST": ["RACIEST", "STEARIC", "CRISTAE"],
    "AEGINST": ["SEATING", "TEASING", "INGESTA"],
    "ADEGNRS": ["GARDENS", "GANDERS", "DANGERS"],
    "AEINPRS": ["RAPINES", "PANIERS"],
    "ACELPRS": ["CLASPER", "PARCELS", "SCALPER"],
    "EINORST": ["STONIER", "ORIENTS"],
    "AELMNOT": ["OMENTAL", "TELAMON"],
    "ADEINST": ["INSTEAD", "DETAINS", "SAINTED"],
}

SYSTEM_PROMPT = (
    "You are an anagram solver. Given scrambled letters, find ALL valid "
    "English words that use every letter exactly once. Return words as "
    "uppercase CSV. No explanation needed."
)
SEED = 42
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")

random.seed(SEED)


def load_dictionary(path="/usr/share/dict/words"):
    """Load system dictionary, filter to 3-7 letter alpha words."""
    words = set()
    with open(path) as f:
        for line in f:
            w = line.strip().upper()
            if 3 <= len(w) <= 7 and w.isalpha():
                words.add(w)
    return words


def find_anagram_groups(words):
    """Group words by their sorted letters."""
    groups = defaultdict(set)
    for w in words:
        key = "".join(sorted(w))
        groups[key].add(w)
    # Keep only groups with 2+ words
    return {k: sorted(v) for k, v in groups.items() if len(v) >= 2}


def make_example(letters: str, words: list[str]) -> dict:
    """Create one chat-format training example."""
    letter_display = " ".join(letters.upper())
    answer = ", ".join(sorted(set(words)))
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Unscramble: {letter_display}"},
            {"role": "assistant", "content": answer},
        ]
    }


def generate_shuffles(key: str, n: int) -> list[str]:
    """Generate n unique shuffled orderings of a sorted key."""
    letters = list(key)
    seen = set()
    for _ in range(n * 5):
        if len(seen) >= n:
            break
        shuffled = letters.copy()
        random.shuffle(shuffled)
        ordering = "".join(shuffled)
        if ordering not in seen:
            seen.add(ordering)
    return list(seen)


def generate_dataset():
    """Build diverse dataset: game groups + dictionary groups."""

    # ── Step 1: Game groups (HIGH PRIORITY — 30 shuffles each) ──
    game_examples = []
    game_keys_used = set()
    for key, words in GAME_GROUPS.items():
        if len(set(words)) < 2:
            continue
        game_keys_used.add(key)
        shuffles = generate_shuffles(key, 30)
        for s in shuffles:
            game_examples.append(make_example(s, words))

    print(f"  Game groups: {len(game_keys_used)} groups → {len(game_examples)} examples")

    # ── Step 2: Dictionary groups (DIVERSITY — 5 shuffles each) ──
    print("  Loading system dictionary...")
    all_words = load_dictionary()
    print(f"  Found {len(all_words)} words (3-7 letters)")

    dict_groups = find_anagram_groups(all_words)
    print(f"  Found {len(dict_groups)} anagram groups in dictionary")

    # Remove game groups (already covered)
    new_groups = {k: v for k, v in dict_groups.items() if k not in game_keys_used}
    print(f"  New (non-game) groups: {len(new_groups)}")

    # Sample up to 500 diverse groups, prioritizing common word lengths
    group_keys = list(new_groups.keys())
    random.shuffle(group_keys)

    # Balance across word lengths
    by_length = defaultdict(list)
    for k in group_keys:
        by_length[len(k)].append(k)

    selected_keys = []
    target_per_length = 100  # 100 groups per word-length = 500 total
    for length in sorted(by_length.keys()):
        pool = by_length[length]
        selected_keys.extend(pool[:target_per_length])

    print(f"  Selected {len(selected_keys)} diverse groups")

    dict_examples = []
    for key in selected_keys:
        words = new_groups[key]
        shuffles = generate_shuffles(key, 5)
        for s in shuffles:
            dict_examples.append(make_example(s, words))

    print(f"  Dictionary examples: {len(dict_examples)}")

    # ── Combine ──
    all_examples = game_examples + dict_examples
    random.shuffle(all_examples)
    print(f"\n  TOTAL: {len(all_examples)} examples")
    return all_examples


def split_and_save(examples):
    """80/10/10 split."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    n = len(examples)
    train_end = int(n * 0.8)
    valid_end = int(n * 0.9)

    splits = {
        "train.jsonl": examples[:train_end],
        "valid.jsonl": examples[train_end:valid_end],
        "test.jsonl": examples[valid_end:],
    }

    for filename, data in splits.items():
        path = os.path.join(OUTPUT_DIR, filename)
        with open(path, "w") as f:
            for ex in data:
                f.write(json.dumps(ex) + "\n")
        print(f"  {filename}: {len(data)} examples")

    return splits


if __name__ == "__main__":
    print("=== Diverse Anagram Dataset Generator v2 ===\n")
    examples = generate_dataset()
    print("\nSaving splits:")
    splits = split_and_save(examples)

    print("\n─── Sample ───")
    print(json.dumps(splits["train.jsonl"][0], indent=2))
    print(f"\nSaved to: {os.path.abspath(OUTPUT_DIR)}")
