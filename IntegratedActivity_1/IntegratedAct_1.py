# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 3
# Luis Salomón Flores Ugalde

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925
# Benjamin-Christian Blaga A01830797
# Alfredo Luce Morales A01772499

# ------ INTEGRATED ACTIVITY - TRANSMISSION ANALYSIS AND MALICIOUS CODE DETECTION ------


from typing import Tuple

FILENAMES_TRANSMISSIONS = ["transmission1.txt", "transmission2.txt"]
FILENAMES_MCODE = ["mcode1.txt", "mcode2.txt", "mcode3.txt"]

# ---------- Helpers: IO & normalization ----------

def read_stream(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    
    data = data.upper()
    
    allowed = set("0123456789ABCDEF")
    return "".join(ch for ch in data if ch in allowed)

# ---------- KMP Algorithm Implementation ----------

def kmp_lps(pattern: str) -> list:
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

def kmp_search_first(text: str, pattern: str) -> int:
    if not pattern:
        return 0  
    
    n, m = len(text), len(pattern)
    if m > n:
        return -1
    
    lps = kmp_lps(pattern)
    
    i = 0 
    j = 0 
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            
            if j == m: 
                return i - j  
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return -1  # pattern not found

# ---------- Part 1: containment (first occurrence) ----------

def first_occurrence(haystack: str, needle: str) -> int:
    if not needle:
        return 1  # Convention: empty needle found at position 1
    
    # Use KMP algorithm for efficient searching
    idx = kmp_search_first(haystack, needle)
    return idx + 1 if idx != -1 else 0

def part1(transmissions, mcodes):
    t1, t2 = transmissions
    m1, m2, m3 = mcodes

    for t in (t1, t2):
        for m in (m1, m2, m3):
            pos = first_occurrence(t, m)
            if pos > 0:
                print(f"true {pos}")
            else:
                print("false")

# ---------- Part 2: longest palindromic substring (1-based inclusive) ----------

def longest_palindrome_bounds(s: str) -> Tuple[int, int]:
    if not s:
        return (1, 0)  # empty

    t = "^#" + "#".join(s) + "#$"
    n = len(t)
    p = [0] * n
    center = right = 0
    best_len = 0
    best_center = 0

    for i in range(1, n - 1):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])
        while t[i + (1 + p[i])] == t[i - (1 + p[i])]:
            p[i] += 1
        if i + p[i] > right:
            center, right = i, i + p[i]
        if p[i] > best_len:
            best_len = p[i]
            best_center = i
        elif p[i] == best_len and best_len > 0:
            cand_start = (best_center - best_len) // 2  # old
            new_start = (i - p[i]) // 2
            if new_start < cand_start:
                best_center = i

    start0 = (best_center - best_len) // 2
    end0 = start0 + best_len - 1
    return (start0 + 1, end0 + 1)

def part2(transmissions):
    for t in transmissions:
        a, b = longest_palindrome_bounds(t)
        print(f"{a} {b}")


class SAMState:
    __slots__ = ("link", "next", "length", "first_pos")
    def __init__(self):
        self.link = -1
        self.next = {}   
        self.length = 0
        self.first_pos = -1  

class SuffixAutomaton:
    def __init__(self):
        self.states = [SAMState()]
        self.last = 0  

    def sa_extend(self, ch: str):
        cur = len(self.states)
        self.states.append(SAMState())
        self.states[cur].length = self.states[self.last].length + 1
        self.states[cur].first_pos = self.states[cur].length - 1

        p = self.last
        while p >= 0 and ch not in self.states[p].next:
            self.states[p].next[ch] = cur
            p = self.states[p].link
        if p == -1:
            self.states[cur].link = 0
        else:
            q = self.states[p].next[ch]
            if self.states[p].length + 1 == self.states[q].length:
                self.states[cur].link = q
            else:
                clone = len(self.states)
                self.states.append(SAMState())
                self.states[clone].length = self.states[p].length + 1
                self.states[clone].next = self.states[q].next.copy()
                self.states[clone].link = self.states[q].link
                self.states[clone].first_pos = self.states[q].first_pos  

                while p >= 0 and self.states[p].next.get(ch) == q:
                    self.states[p].next[ch] = clone
                    p = self.states[p].link
                self.states[q].link = self.states[cur].link = clone
        self.last = cur

    def build(self, s: str):
        for ch in s:
            self.sa_extend(ch)

def longest_common_substring_bounds_in_s1(s1: str, s2: str) -> Tuple[int, int]:
    if not s1 or not s2:
        return (1, 0)

    sam = SuffixAutomaton()
    sam.build(s1)

    v = 0       
    l = 0       
    best_len = 0
    best_end_pos_in_s1 = -1

    for ch in s2:
        if ch in sam.states[v].next:
            v = sam.states[v].next[ch]
            l += 1
        else:
            while v != -1 and ch not in sam.states[v].next:
                v = sam.states[v].link
            if v == -1:
                v = 0
                l = 0
                continue
            else:
                l = sam.states[v].length + 1
                v = sam.states[v].next[ch]

        if l > best_len:
            best_len = l
            best_end_pos_in_s1 = sam.states[v].first_pos
        elif l == best_len and l > 0:
            cand_start = best_end_pos_in_s1 - best_len + 1
            new_start = sam.states[v].first_pos - l + 1
            if new_start < cand_start:
                best_end_pos_in_s1 = sam.states[v].first_pos

    if best_len == 0:
        return (1, 0)

    start0 = best_end_pos_in_s1 - best_len + 1
    end0 = best_end_pos_in_s1
    return (start0 + 1, end0 + 1)

def part3(transmissions):
    t1, t2 = transmissions
    a, b = longest_common_substring_bounds_in_s1(t1, t2)
    print(f"{a} {b}")

# ---------- Main ----------

def main():
    transmissions = [read_stream(fn) for fn in FILENAMES_TRANSMISSIONS]
    mcodes = [read_stream(fn) for fn in FILENAMES_MCODE]

    part1(transmissions, mcodes)
    part2(transmissions)
    part3(transmissions)

if __name__ == "__main__":
    main()
