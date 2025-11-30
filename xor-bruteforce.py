import itertools, random, time, math

# Ciphertext
cipher = 'Jevsdfa"[aocmickniIdsdu"xhbzoiq`nc!!FQ@E9:610/"!rq$bj_jk~{oup ttgze0|Jrmf#fo],'
ct_bytes = [ord(c) for c in cipher]

# English score
english_freq = {
    'a': .08167,'b': .01492,'c': .02782,'d': .04253,'e': .12702,'f': .02228,'g': .02015,
    'h': .06094,'i': .06966,'j': .00153,'k': .00772,'l': .04025,'m': .02406,'n': .06749,
    'o': .07507,'p': .01929,'q': .00095,'r': .05987,'s': .06327,'t': .09056,'u': .02758,
    'v': .00978,'w': .02360,'x': .00150,'y': .01974,'z': .00074,' ': .13000
}

def english_score(s):
    s = s.lower()
    score = 0.0
    for ch in s:
        if ch in english_freq:
            score += math.log(english_freq[ch])
        elif ch.isalpha():
            score += math.log(0.001)
        elif 32 <= ord(ch) <= 126:
            score += math.log(0.01)
        else:
            score += math.log(0.0001)
    return score

def xor_repeating_with_key(ct_bytes, key_bytes):
    m = len(key_bytes)
    return ''.join(chr(b ^ key_bytes[i % m]) for i, b in enumerate(ct_bytes))

# Beam search + hill-climb
def beam_hill_climb(keylen, beam_width=2000, K=16, hill_iters=50000):
    start_time = time.time()
# Top-K per column
    column_candidates = []
    for i in range(keylen):
        col = [ct_bytes[j] for j in range(i, len(ct_bytes), keylen)]
        cand = [(english_score(''.join(chr(b ^ k) for b in col)), k) for k in range(256)]
        cand.sort(reverse=True)
        column_candidates.append(cand[:K])

    # Beam search
    beam = [(0.0, b'')]
    for pos in range(keylen):
        new_beam = []
        candidates = column_candidates[pos]
        for sc_key, key_bytes in beam:
            for sc_k, kb in candidates:
                new_key = key_bytes + bytes([kb])
                pt = xor_repeating_with_key(ct_bytes, new_key)
                score = english_score(pt)
                new_beam.append((score, new_key))
        new_beam.sort(reverse=True, key=lambda x: x[0])
        beam = new_beam[:beam_width]

    # Hill-climb from best beam
    best_score, best_key = beam[0]
    best_plain = xor_repeating_with_key(ct_bytes, best_key)
    key = bytearray(best_key)
    score = best_score
    for it in range(hill_iters):
      
    # check key length>mutate count
        mutate_count = random.choice(range(1, min(3, len(key)) + 1))
        indices = random.sample(range(len(key)), mutate_count)
        old_bytes = [key[i] for i in indices]
        for i in indices:
            key[i] = random.randrange(256)
        pt = xor_repeating_with_key(ct_bytes, key)
        sc = english_score(pt)
        if sc > score or random.random() < 0.001:
            score = sc
            if sc > best_score:
                best_score = sc
                best_key = bytearray(key)
                best_plain = pt
        else:
            for i,val in zip(indices, old_bytes):
                key[i] = val
    elapsed = time.time() - start_time
    return best_key, best_plain, best_score, elapsed

# multiple key lengths
for kl in range(12, 23):
    key, plain, score, elapsed = beam_hill_climb(kl, beam_width=10000, K=16, hill_iters=50000)
    print("\n=== Key length", kl, "finished ===")
    print(f"Elapsed: {elapsed:.2f}s")
    print("Best key (hex):", key.hex())
    print("Key display:", ''.join(chr(b) if 32<=b<=126 else f"\\x{b:02x}" for b in key))
    print("Plaintext:", plain)
    print("-"*80)
