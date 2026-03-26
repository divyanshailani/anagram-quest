"""
╔══════════════════════════════════════════════════════════════════╗
║  ANAGRAM QUEST — SFT → GRPO Training Pipeline                   ║
║  Platform: Google Colab (T4 GPU, 15GB VRAM)                     ║
║  Model: Qwen/Qwen3-0.6B + LoRA                                  ║
║  Pipeline: SFT warm-up → GRPO reinforcement                     ║
║                                                                  ║
║  Author: Divyansh Ailani | github.com/divyanshailani            ║
╚══════════════════════════════════════════════════════════════════╝

Paste each ═══ section into a separate Colab cell.
"""

# ═══════════════════════════════════════════════════════════════
# CELL 1: Install (run once after fresh runtime)
# ═══════════════════════════════════════════════════════════════
# !pip install transformers peft bitsandbytes accelerate nltk --quiet

# ═══════════════════════════════════════════════════════════════
# CELL 2: Imports + English Dictionary
# ═══════════════════════════════════════════════════════════════
import re, random, nltk, torch, gc, time
from collections import Counter
import torch.nn.functional as F

nltk.download("words", quiet=True)
from nltk.corpus import words as nltk_words

ENGLISH_WORDS = set(
    w.upper() for w in nltk_words.words()
    if 3 <= len(w) <= 8 and w.isalpha()
)
print(f"📚 Loaded {len(ENGLISH_WORDS):,} English words")

# ═══════════════════════════════════════════════════════════════
# CELL 3: Unified Game Data (157 groups, synced with ai_player)
# ═══════════════════════════════════════════════════════════════
GAME_GROUPS = {
    # ── Level: 3-letter words ──
    "ABT": ["BAT", "TAB"],
    "ACT": ["ACT", "CAT"],
    "ADM": ["DAM", "MAD"],
    "AEL": ["ALE", "LEA"],
    "AET": ["ATE", "EAT", "ETA", "TEA"],
    "AGR": ["GAR", "RAG"],
    "AHM": ["HAM", "MAH"],
    "AJR": ["JAR", "RAJ"],
    "AMP": ["AMP", "MAP"],
    "ANP": ["NAP", "PAN"],
    "ANT": ["ANT", "TAN"],
    "APS": ["ASP", "SAP", "SPA"],
    "APT": ["APT", "PAT", "TAP"],
    "ARS": ["ARS", "SAR"],
    "ART": ["ART", "RAT", "TAR"],
    "ASW": ["SAW", "WAS"],
    "DEN": ["DEN", "END"],
    "DGO": ["DOG", "GOD"],
    "ENT": ["NET", "TEN"],
    "GIN": ["GIN", "ING"],
    "GNO": ["GON", "NOG"],
    "GNU": ["GNU", "GUN", "NUG"],
    "HOW": ["HOW", "WHO"],
    "INP": ["NIP", "PIN"],
    "IPS": ["PSI", "SIP"],
    "LOW": ["LOW", "OWL"],
    "NOS": ["NOS", "SON"],
    "NOW": ["NOW", "OWN", "WON"],
    "OPT": ["OPT", "POT", "TOP"],
    "ORT": ["ROT", "TOR"],
    "OTW": ["OWT", "TOW", "TWO", "WOT"],
    # ── Level: 4-letter words ──
    "ACRS": ["ARCS", "CARS", "SCAR"],
    "ACST": ["ACTS", "CAST", "CATS", "SCAT"],
    "ADEM": ["DAME", "MADE", "MEAD"],
    "ADER": ["DARE", "DEAR", "READ"],
    "AEGM": ["GAME", "MAGE"],
    "AHRS": ["RASH", "SHAR"],
    "AILR": ["LAIR", "LIAR", "RAIL", "RIAL"],
    "AILS": ["AILS", "SAIL"],
    "AIMS": ["AIMS", "AMIS"],
    "AIPS": ["PAIS", "PIAS"],
    "AELM": ["LAME", "MALE", "MEAL"],
    "AELP": ["LEAP", "PALE", "PEAL", "PLEA"],
    "AELR": ["EARL", "REAL"],
    "AELS": ["ALES", "LEAS", "SALE", "SEAL"],
    "AELT": ["LATE", "TALE", "TEAL"],
    "AEMN": ["AMEN", "MANE", "MEAN", "NAME"],
    "AENR": ["EARN", "NEAR", "RANE"],
    "AEPS": ["APES", "PEAS"],
    "AEPT": ["PATE", "PEAT", "TAPE"],
    "AERS": ["ARES", "EARS", "ERAS", "SEAR"],
    "AERT": ["RATE", "TARE", "TEAR"],
    "AERW": ["WARE", "WEAR"],
    "AEST": ["ETAS", "SATE", "SEAT", "TEAS"],
    "ALPS": ["ALPS", "LAPS", "PALS", "SLAP"],
    "ALMS": ["ALMS", "LAMS", "SLAM"],
    "AMOR": ["MORA", "ROAM"],
    "AMST": ["MAST", "MATS", "TAMS"],
    "ANPS": ["NAPS", "PANS", "SNAP", "SPAN"],
    "ARST": ["ARTS", "RATS", "STAR", "TARS"],
    "ADEL": ["DALE", "DEAL", "LEAD"],
    "DEIS": ["DIES", "IDES", "SIDE"],
    "DEOS": ["DOES", "DOSE", "ODES"],
    "EIKL": ["KEIL", "LIKE"],
    "EILS": ["ISLE", "LIES"],
    "EILV": ["EVIL", "LIVE", "VEIL", "VILE"],
    "EIST": ["SITE", "TIES"],
    "ELST": ["LEST", "LETS"],
    "ENOT": ["NOTE", "TONE"],
    "EORS": ["ORES", "ROSE", "SORE"],
    "GINS": ["GINS", "SIGN", "SING"],
    "ILNO": ["LION", "LOIN"],
    "OPST": ["OPTS", "POST", "POTS", "SPOT", "STOP", "TOPS"],
    "ORST": ["ROTS", "SORT", "TORS"],
    # ── Level: 5-letter words ──
    "ABENR": ["BANE", "BARN", "BEAR"],
    "ADELS": ["DALES", "DEALS", "LEADS"],
    "ADEMS": ["DAMES", "MEADS"],
    "AEGRS": ["GEARS", "RAGES", "SAGER"],
    "AELNS": ["LANES", "LEANS"],
    "AELNP": ["PANEL", "PENAL", "PLANE"],
    "AELPS": ["LEAPS", "PALES", "PEALS", "PLEAS", "SEPAL"],
    "AELRT": ["ALERT", "ALTER", "LATER"],
    "AELST": ["LEAST", "SLATE", "STALE", "STEAL", "TALES", "TESLA"],
    "AEMRS": ["MARES", "MASER", "REAMS", "SMEAR"],
    "AENRS": ["EARNS", "NEARS", "SANER", "SNARE"],
    "AENST": ["ANTES", "ETNAS", "NATES", "NEATS", "STANE"],
    "AEPRS": ["PEARS", "PARSE", "REAPS", "SPARE", "SPEAR"],
    "AILNS": ["NAILS", "SLAIN", "SNAIL"],
    "AILRT": ["TRAIL", "TRIAL"],
    "AINRT": ["INTRA", "TRAIN"],
    "DEIRS": ["DRIES", "RIDES", "SIRED"],
    "DEIST": ["DIETS", "EDITS", "SITED", "TIDES"],
    "EERST": ["RESET", "STEER", "TREES"],
    "EGNOR": ["GENRO", "GONER"],
    "EILNS": ["LIENS", "LINES"],
    "EILPS": ["PILES", "PLIES", "SPIEL"],
    "EINPS": ["PINES", "SNIPE", "SPINE"],
    "EINRS": ["REINS", "RINSE", "RISEN", "SIREN"],
    "EINRT": ["INERT", "INTER", "NITER", "TRINE"],
    "EINST": ["INSET", "STEIN", "TINES"],
    "EORST": ["ROTES", "STORE", "TORES"],
    "EPRSU": ["PURSE", "SPRUE", "SUPER"],
    "ERSTW": ["STREW", "WREST"],
    "AELPRS": ["PARLES", "PEARLS"],
    "ACLRS": ["CARLS", "CLARS"],
    # ── Level: 6-letter words ──
    "ACEIRST": ["CRISTAE", "RACIEST", "STEARIC"],
    "ACENRS": ["CANERS", "CRANES", "NACRES"],
    "ACERST": ["CASTER", "CATERS", "RECAST", "TRACES"],
    "ADEIRS": ["DARIES", "RAISED"],
    "ADEINR": ["DENARI", "RAINED"],
    "AEGINR": ["EARING", "GAINER", "REGAIN"],
    "AEGLNS": ["ANGLES", "GLEANS"],
    "AEGNRS": ["ANGERS", "RANGES", "SANGER"],
    "AEGNRT": ["ARGENT", "GARNET"],
    "AEIMNR": ["MARINE", "REMAIN"],
    "AEILNR": ["LINEAR", "NAILER"],
    "AEILNS": ["SALINE", "SILANE"],
    "AEINRS": ["ARISEN", "SARNIE"],
    "AEINST": ["INSEAT", "TISANE"],
    "AELRSV": ["LAVERS", "SALVER", "VELARS"],
    "AELRST": ["ALERTS", "ALTERS", "SLATER", "STELAR"],
    "AEMNST": ["AMENTS", "MANTES", "STAMEN"],
    "AEORST": ["OATERS", "ORATES"],
    "AEPRST": ["PASTER", "REPAST", "TAPERS", "TRAPES"],
    "AGINST": ["GIANTS", "SATING"],
    "DEGINS": ["DESIGN", "SIGNED", "SINGED"],
    "DEINRS": ["DINERS", "RINSED"],
    "DEORST": ["DOTERS", "SORTED", "STORED"],
    "DEISTU": ["DUTIES", "SUITED"],
    "EILNPS": ["PENSIL", "SPLINE"],
    "EILNST": ["ENLIST", "LISTEN", "SILENT", "TINSEL"],
    "EINORS": ["IRONES", "SENIOR"],
    "EINPRS": ["RIPENS", "SNIPER"],
    "EINRST": ["INSERT", "INTERS", "SINTER"],
    # ── Level: 7+ letter words ──
    "ACELPRS": ["CLASPER", "PARCELS", "SCALPER"],
    "ADEGNRS": ["DANGERS", "GANDERS", "GARDENS"],
    "ADEINRS": ["RANDIES", "SARDINE"],
    "ADEINST": ["DETAINS", "INSTEAD", "SAINTED"],
    "AEGINRS": ["EARINGS", "ERASING", "REGAINS", "SEARING"],
    "AEGINST": ["INGESTA", "SEATING", "TEASING"],
    "AEGNRST": ["GARNETS", "STRANGE"],
    "AEILMNS": ["MENIALS", "SEMINAL"],
    "AEILMNT": ["AILMENT", "ALIMENT"],
    "AEILNRS": ["ALINERS", "NAILERS"],
    "AEILNST": ["ELASTIN", "ENTAILS", "SALTINE"],
    "AEINPRS": ["PANIERS", "RAPINES"],
    "AEINRST": ["NASTIER", "RETAINS", "STAINER"],
    "AEIPRST": ["PARTIES", "PASTIER", "PIRATES"],
    "AELMNOT": ["OMENTAL", "TELAMON"],
    "AELPRST": ["PLASTER", "PSALTER", "STAPLER"],
    "CEINORS": ["COINERS", "CRONIES", "ORCEINS"],
    "DEGILNS": ["DINGLES", "ENGILDS", "SINGLED"],
    "DEINORS": ["DINEROS", "INDORSE", "ORDINES", "ROSINED"],
    "EGILNRS": ["LINGERS", "SLINGER"],
    "EINORST": ["ORIENTS", "STONIER"],
    "AEGILNR": ["ALIGNER", "REALIGN"],
    "AEGLNR": ["ANGLER", "LANGER"],
}

SYSTEM_MSG = (
    "You are an anagram solver. Given scrambled letters, find ALL valid "
    "English words that use every letter exactly once. "
    "Return words as uppercase CSV. No explanation."
)

def make_prompts(n=500):
    """Generate n random prompts from game groups."""
    random.seed(42)
    keys = [k for k, v in GAME_GROUPS.items() if len(set(v)) >= 2]
    prompts = []
    for _ in range(n):
        key = random.choice(keys)
        letters = list(key)
        random.shuffle(letters)
        prompts.append({
            "text": f"Unscramble: {' '.join(letters)}",
            "letters": key,
        })
    return prompts

PROMPTS = make_prompts(500)
print(f"📊 {len(GAME_GROUPS)} game groups | {len(PROMPTS)} training prompts")

# ═══════════════════════════════════════════════════════════════
# CELL 4: Load Model + LoRA
# ═══════════════════════════════════════════════════════════════
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-0.6B",
    quantization_config=bnb_config,
    device_map="auto",
)

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.eos_token_id

lora_config = LoraConfig(
    r=32,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                     "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
print("✅ Model loaded with LoRA")

# ═══════════════════════════════════════════════════════════════
# CELL 5: Reward Function
# ═══════════════════════════════════════════════════════════════

def compute_reward(response_text: str, letter_key: str) -> float:
    """Score a single model response."""
    text = response_text.strip()
    if "</think>" in text:
        text = text.split("</think>")[-1].strip()
    text = text.split("\n")[0].strip()

    words = [w.strip().upper() for w in text.split(",") if w.strip()]
    if not words or not any(w.isalpha() for w in words):
        return -2.0

    letter_counter = Counter(letter_key.upper())
    total = 0.0

    if all(w.isalpha() for w in words):
        total += 0.5

    seen = set()
    for word in words:
        if not word.isalpha():
            total -= 0.5; continue
        if word in seen:
            total -= 0.5; continue
        seen.add(word)
        if Counter(word) == letter_counter:
            if word in ENGLISH_WORDS:
                total += 2.0
            else:
                total -= 0.5
        else:
            total -= 1.0
    return total

print("🧪 Reward: 'BAT, TAB' →", compute_reward("BAT, TAB", "ABT"))

# ═══════════════════════════════════════════════════════════════
# CELL 6: SFT Warm-up (~5 min)
# ═══════════════════════════════════════════════════════════════
from torch.utils.data import Dataset, DataLoader

class AnagramDataset(Dataset):
    def __init__(self, tokenizer, n=3000):
        random.seed(42)
        self.examples = []
        keys = list(GAME_GROUPS.keys())
        for _ in range(n):
            key = random.choice(keys)
            letters = list(key)
            random.shuffle(letters)
            prompt = f"Unscramble: {' '.join(letters)}"
            answer = ", ".join(GAME_GROUPS[key])
            messages = [
                {"role": "system", "content": SYSTEM_MSG},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": answer}
            ]
            text = tokenizer.apply_chat_template(messages, tokenize=False, enable_thinking=False)
            enc = tokenizer(text, truncation=True, max_length=256, padding="max_length", return_tensors="pt")
            self.examples.append({
                "input_ids": enc["input_ids"].squeeze(),
                "attention_mask": enc["attention_mask"].squeeze(),
                "labels": enc["input_ids"].squeeze().clone()
            })
    def __len__(self): return len(self.examples)
    def __getitem__(self, i): return self.examples[i]

dataset = AnagramDataset(tokenizer, n=3000)
loader = DataLoader(dataset, batch_size=4, shuffle=True)

model.train()
sft_optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=2e-4, weight_decay=0.01)
print("📖 SFT Warm-up: Teaching the model anagram format...")
print("=" * 50)
for epoch in range(2):
    losses = []
    for i, batch in enumerate(loader):
        input_ids = batch["input_ids"].to(model.device)
        attention_mask = batch["attention_mask"].to(model.device)
        labels = batch["labels"].to(model.device)
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        sft_optimizer.step()
        sft_optimizer.zero_grad()
        losses.append(loss.item())
        if (i+1) % 50 == 0:
            print(f"  Epoch {epoch+1} | Batch {i+1}/{len(loader)} | Loss: {sum(losses[-50:])/50:.3f}")
    gc.collect(); torch.cuda.empty_cache()

# Quick test
model.eval()
test_msgs = [{"role":"system","content":SYSTEM_MSG},{"role":"user","content":"Unscramble: T B A"}]
test_input = tokenizer.apply_chat_template(test_msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
test_enc = tokenizer(test_input, return_tensors="pt").to(model.device)
with torch.no_grad():
    out = model.generate(**test_enc, max_new_tokens=64, do_sample=False, pad_token_id=tokenizer.pad_token_id)
print(f"\n✅ SFT Done! Test: 'T B A' → {tokenizer.decode(out[0][test_enc['input_ids'].shape[1]:], skip_special_tokens=True)}")

# ═══════════════════════════════════════════════════════════════
# CELL 7: GRPO Training Loop (~12 min)
# ═══════════════════════════════════════════════════════════════

@torch.no_grad()
def generate_responses(model, tokenizer, prompt_text, n=4):
    messages = [{"role":"system","content":SYSTEM_MSG},{"role":"user","content":prompt_text}]
    input_text = tokenizer.apply_chat_template(messages, tokenize=False,
        add_generation_prompt=True, enable_thinking=False)
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
    input_len = inputs["input_ids"].shape[1]
    responses = []
    for _ in range(n):
        out = model.generate(**inputs, max_new_tokens=64, do_sample=True,
            temperature=0.8, top_p=0.95, pad_token_id=tokenizer.pad_token_id)
        responses.append(tokenizer.decode(out[0][input_len:], skip_special_tokens=True))
    return responses, input_text

def grpo_step(model, tokenizer, optimizer, prompt_data):
    model.eval()
    responses, full_prompt = generate_responses(model, tokenizer, prompt_data["text"])
    rewards = [compute_reward(r, prompt_data["letters"]) for r in responses]
    rewards_t = torch.tensor(rewards, dtype=torch.float32)
    advantages = (rewards_t - rewards_t.mean()) / (rewards_t.std() + 1e-8)
    if rewards_t.std() < 1e-6:
        return rewards_t.mean().item(), responses, rewards
    model.train()
    optimizer.zero_grad()
    total_loss = torch.tensor(0.0, device=model.device, requires_grad=True)
    for response, adv in zip(responses, advantages):
        if adv.item() <= 0: continue
        full_text = full_prompt + response + tokenizer.eos_token
        enc = tokenizer(full_text, return_tensors="pt", truncation=True, max_length=256)
        input_ids = enc["input_ids"].to(model.device)
        prompt_len = tokenizer(full_prompt, return_tensors="pt")["input_ids"].shape[1]
        logits = model(input_ids=input_ids, attention_mask=enc["attention_mask"].to(model.device)).logits
        log_probs = F.log_softmax(logits[:, prompt_len-1:-1, :], dim=-1)
        token_lp = torch.gather(log_probs, 2, input_ids[:, prompt_len:].unsqueeze(-1)).squeeze(-1)
        total_loss = total_loss + (-adv.to(model.device) * token_lp.mean())
    total_loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    optimizer.step()
    return rewards_t.mean().item(), responses, rewards

NUM_STEPS = 200
optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=5e-6, weight_decay=0.01)
print("🚀 GRPO: 200 steps × 4 responses (SFT → GRPO pipeline)")
print("=" * 50)
reward_history, start_time = [], time.time()
for step in range(1, NUM_STEPS + 1):
    prompt = random.choice(PROMPTS)
    mean_r, responses, rewards = grpo_step(model, tokenizer, optimizer, prompt)
    reward_history.append(mean_r)
    if step % 5 == 0:
        avg = sum(reward_history[-5:]) / 5
        eta = (time.time()-start_time)/step*(NUM_STEPS-step)/60
        best_idx = rewards.index(max(rewards))
        print(f"Step {step:>3}/{NUM_STEPS} | R:{mean_r:>+5.1f} | Avg:{avg:>+5.1f} | ETA:{eta:.0f}m")
        print(f"  {prompt['text']} → {responses[best_idx][:60]}")
    if step % 50 == 0: gc.collect(); torch.cuda.empty_cache()
print(f"\n✅ Done! ({(time.time()-start_time)/60:.0f}min)")

# ═══════════════════════════════════════════════════════════════
# CELL 8: Evaluate
# ═══════════════════════════════════════════════════════════════
model.eval()
test_cases = [
    ("T B A", "ABT"), ("E A T", "AET"), ("O P S T", "OPST"),
    ("L V I E", "EILV"), ("I N E S T L", "EILNST"), ("S E P R A", "AEPRS"),
    ("D A L E", "ADEL"), ("G N U", "GNU"), ("E A R N", "AENR"),
    ("L E A P S", "AELPS"),
]
print("📊 GRPO Model Evaluation:")
print("=" * 60)
correct = 0
for letters, key in test_cases:
    msgs = [{"role":"system","content":SYSTEM_MSG},{"role":"user","content":f"Unscramble: {letters}"}]
    inp = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    enc = tokenizer(inp, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(**enc, max_new_tokens=64, do_sample=False, pad_token_id=tokenizer.pad_token_id)
    response = tokenizer.decode(out[0][enc["input_ids"].shape[1]:], skip_special_tokens=True)
    expected = GAME_GROUPS[key]
    words = [w.strip().upper() for w in response.split(",") if w.strip()]
    hits = sum(1 for w in words if w in expected)
    total = len(expected)
    correct += hits
    status = "✅" if hits == total else "⚠️" if hits > 0 else "❌"
    print(f"  {status} {letters} → {response[:50]}  ({hits}/{total})")
print(f"\nTotal: {correct}/{sum(len(GAME_GROUPS[k]) for _,k in test_cases)} words found")

# ═══════════════════════════════════════════════════════════════
# CELL 9: Save & Download
# ═══════════════════════════════════════════════════════════════
import shutil

save_dir = "/content/anagram_grpo_merged"
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
shutil.make_archive(save_dir, 'zip', save_dir)
print(f"✅ Saved to {save_dir}.zip")

from google.colab import files
files.download(f"{save_dir}.zip")
print("📥 Downloading...")
