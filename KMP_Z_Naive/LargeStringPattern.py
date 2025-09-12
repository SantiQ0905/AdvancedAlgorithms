# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 3
# Luis Salomón Flores Ugalde

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ LARGE STRING PATTERN - KMP, Z AND NAIVE ALGORITHMS ------

def naive_search(text: str, pattern: str):
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
    hits = []
    for i in range(n - m + 1):
        if text[i:i+m] == pattern:
            hits.append(i)
    return hits

def kmp_lps(pattern: str):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str):
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
    lps = kmp_lps(pattern)
    hits, i, j = [], 0, 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1; j += 1
            if j == m:
                hits.append(i - j)  
                j = lps[j - 1]      
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return hits

def z_array(s: str):
    n = len(s)
    Z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            Z[i] = min(r - i + 1, Z[i - l])
        while i + Z[i] < n and s[Z[i]] == s[i + Z[i]]:
            Z[i] += 1
        if i + Z[i] - 1 > r:
            l, r = i, i + Z[i] - 1
    return Z

def z_search(text: str, pattern: str):
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
    s = pattern + '\x00' + text    
    Z = z_array(s)
    return [i - (m + 1) for i in range(m + 1, len(s)) if Z[i] >= m]

texts = [
    ("Naname nanajyuunana-do no narabi de nakunaku inanaku nanahan nanadai nannaku narabete naganagame.", "nana"),
    ("Nyanyame nyanyajyuunyanya-do no nyarabi de nyakunyaku inyanyaku nyanyahan nyanyadai nyanynaku nyarabete nyaganyagame.", "nya"),
]
for idx, (T, P) in enumerate(texts, 1):
    naive_hits = naive_search(T, P)
    kmp_hits = kmp_search(T, P)
    z_hits = z_search(T, P)
    print(f"Case {idx}: '{P}' in text len {len(T)}")
    print("  Naive:", len(naive_hits), naive_hits)
    print("  KMP  :", len(kmp_hits), kmp_hits)
    print("  Z    :", len(z_hits), z_hits)
