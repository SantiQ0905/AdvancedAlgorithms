# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 3
# Luis Salomón Flores Ugalde

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ HUFFMAN CODE COMPRESSION ------

class BitWriter:
    def __init__(self):
        self.buf = bytearray()
        self.cur = 0
        self.nbits = 0
    def write_bits_from_str(self, bits: str):
        for ch in bits:
            self.write_bit(1 if ch == '1' else 0)
    def write_bit(self, b: int):
        self.cur = (self.cur << 1) | (1 if b else 0)
        self.nbits += 1
        if self.nbits == 8:
            self.buf.append(self.cur & 0xFF)
            self.cur = 0
            self.nbits = 0
    def bytes(self) -> bytes:
        if self.nbits != 0:
            self.buf.append((self.cur << (8 - self.nbits)) & 0xFF) 
            self.cur = 0
            self.nbits = 0
        return bytes(self.buf)

class BitReader:
    def __init__(self, data: bytes):
        self.data = data
        self.i = 0
        self.mask = 0
        self.cur = 0
    def read_bit(self) -> int:
        if self.mask == 0:
            if self.i >= len(self.data):
                raise EOFError("No more data")
            self.cur = self.data[self.i]
            self.i += 1
            self.mask = 0x80 
        b = 1 if (self.cur & self.mask) else 0
        self.mask >>= 1
        return b

# ---------- MTF ----------
def mtf_encode_bytes(data: bytes):
    table = list(range(256))
    out = []
    for b in data:
        idx = table.index(b)
        out.append(idx)
        del table[idx]
        table.insert(0, b)
    return out

def mtf_decode_to_bytes(idxs):
    table = list(range(256))
    out = bytearray()
    for idx in idxs:
        b = table[idx]
        out.append(b)
        del table[idx]
        table.insert(0, b)
    return bytes(out)

# ---------- Suffix Array ----------
def suffix_array(data: bytes):
    n = len(data)
    rank = list(data)
    k = 1
    sa = list(range(n))
    tmp = [0]*n
    def rank_at(i: int) -> int:
        return rank[i] if i < n else -1
    while True:
        sa.sort(key=lambda i: (rank_at(i), rank_at(i+k)))
        tmp[sa[0]] = 0
        for i in range(1, n):
            a, b = sa[i-1], sa[i]
            tmp[b] = tmp[a] + (rank_at(a) != rank_at(b) or rank_at(a+k) != rank_at(b+k))
        rank = tmp[:]
        if rank[sa[-1]] == n-1:
            break
        k <<= 1
    return sa

# ---------- BWT ----------
def bwt_from_sa(T: bytes, SA):
    n = len(T)
    out = bytearray(n)
    p = -1
    for i in range(n):
        j = SA[i]
        out[i] = T[(j - 1) % n]
        if j == 0:
            p = i
    return bytes(out), p

def inverse_bwt(bwt: bytes, p: int) -> bytes:
    n = len(bwt)
    counts = [0]*256
    ranks = [0]*n
    for i, c in enumerate(bwt):
        ranks[i] = counts[c]
        counts[c] += 1
    total = 0
    first = [0]*256
    for c in range(256):
        first[c] = total
        total += counts[c]
    T = bytearray(n)
    idx = p
    for i in range(n-1, -1, -1):
        c = bwt[idx]
        T[i] = c
        idx = first[c] + ranks[idx]
    return bytes(T)

# ---------- Huffman ----------
import heapq

class _HNode:
    __slots__ = ("freq","sym","left","right")
    def __init__(self, freq, sym=None, left=None, right=None):
        self.freq=freq; self.sym=sym; self.left=left; self.right=right
    def __lt__(self, other):
        a = self.sym if self.sym is not None else 1_000_000_000
        b = other.sym if other.sym is not None else 1_000_000_000
        if self.freq != other.freq: return self.freq < other.freq
        return a < b

def _build_tree_from_freqs(freqs):
    heap = [_HNode(f,s) for s,f in enumerate(freqs) if f>0]
    if not heap: return None
    if len(heap)==1: return heap[0]
    heapq.heapify(heap)
    while len(heap)>1:
        a = heapq.heappop(heap); b = heapq.heappop(heap)
        heapq.heappush(heap, _HNode(a.freq+b.freq, None, a, b))
    return heap[0]

def _assign_codes(root):
    if root is None: return {}
    codes = {}
    if root.sym is not None:
        codes[root.sym] = "0"; return codes
    def dfs(node, pref):
        if node.sym is not None:
            codes[node.sym] = pref if pref else "0"; return
        dfs(node.left,  pref+"0")
        dfs(node.right, pref+"1")
    dfs(root, "")
    return codes

def _freqs_256_from_list(xs):
    f = [0]*256
    for x in xs: f[x]+=1
    return f

def _freqs_256_from_bytes(bs):
    f = [0]*256
    for b in bs: f[b]+=1
    return f

# ---------- File format helpers ----------
import struct
MAGIC_SBM1 = b"SBM1"   
MAGIC_HFN1 = b"HFN1"   
LE = "<I"
def _u32(x): return struct.pack(LE, x)
def _u32_at(buf, off): return struct.unpack_from(LE, buf, off)[0]

# ---------- Codec logic ----------
def _pick_sentinel(data: bytes) -> int:
    present = [False]*256
    for b in data: present[b] = True
    for v in range(256):
        if not present[v]: return v
    raise ValueError("Input uses all 256 byte values; cannot pick a unique sentinel.")

def compress_sbm1(raw: bytes) -> bytes:
    sentinel = _pick_sentinel(raw)
    T = raw + bytes([sentinel])
    SA = suffix_array(T)
    bwt, p = bwt_from_sa(T, SA)
    mtf = mtf_encode_bytes(bwt)
    freqs = _freqs_256_from_list(mtf)
    root = _build_tree_from_freqs(freqs)
    codes = _assign_codes(root)
    bw = BitWriter()
    for s in mtf: bw.write_bits_from_str(codes[s])
    payload = bw.bytes()
    parts = [MAGIC_SBM1, _u32(len(mtf)), _u32(p)]
    for f in freqs: parts.append(_u32(f))
    parts.append(payload)
    return b"".join(parts)

def decompress_sbm1(blob: bytes) -> bytes:
    if blob[:4] != MAGIC_SBM1: raise ValueError("Bad magic for SBM1")
    off = 4
    n = _u32_at(blob, off); off += 4
    p = _u32_at(blob, off); off += 4
    freqs = [0]*256
    for i in range(256):
        freqs[i] = _u32_at(blob, off); off += 4
    root = _build_tree_from_freqs(freqs)
    if root is None: return b""
    if root.sym is not None:
        mtf = [root.sym]*n
    else:
        br = BitReader(blob[off:])
        mtf = []
        node = root
        while len(mtf) < n:
            bit = br.read_bit()
            node = node.left if bit == 0 else node.right
            if node.sym is not None:
                mtf.append(node.sym); node = root
    bwt = mtf_decode_to_bytes(mtf)
    T = inverse_bwt(bwt, p)
    return T[:-1]  

def compress_hfn1(raw: bytes) -> bytes:
    freqs = _freqs_256_from_bytes(raw)
    root = _build_tree_from_freqs(freqs)
    codes = _assign_codes(root)
    bw = BitWriter()
    for b in raw: bw.write_bits_from_str(codes[b])
    payload = bw.bytes()
    parts = [MAGIC_HFN1, _u32(len(raw))]
    for f in freqs: parts.append(_u32(f))
    parts.append(payload)
    return b"".join(parts)

def decompress_hfn1(blob: bytes) -> bytes:
    if blob[:4] != MAGIC_HFN1: raise ValueError("Bad magic for HFN1")
    off = 4
    n = _u32_at(blob, off); off += 4
    freqs = [0]*256
    for i in range(256):
        freqs[i] = _u32_at(blob, off); off += 4
    root = _build_tree_from_freqs(freqs)
    if root is None: return b""
    if root.sym is not None:
        return bytes([root.sym])*n
    br = BitReader(blob[off:])
    out = bytearray(); node = root
    while len(out) < n:
        bit = br.read_bit()
        node = node.left if bit == 0 else node.right
        if node.sym is not None:
            out.append(node.sym); node = root
    return bytes(out)

# ---------- CLI ----------
def _run_cli(inp_path: str):
    import os
    with open(inp_path, "rb") as f: raw = f.read()
    base, _ = os.path.splitext(inp_path)
    sbm_bin = base + "_sbm1.bin"
    sbm_rec = base + "_sbm1_recovered.txt"
    hfn_bin = base + "_hfn1.bin"
    hfn_rec = base + "_hfn1_recovered.txt"

    sbm_blob = compress_sbm1(raw); open(sbm_bin, "wb").write(sbm_blob)
    rec1 = decompress_sbm1(sbm_blob); open(sbm_rec, "wb").write(rec1)

    hfn_blob = compress_hfn1(raw); open(hfn_bin, "wb").write(hfn_blob)
    rec2 = decompress_hfn1(hfn_blob); open(hfn_rec, "wb").write(rec2)

    def sz(p): return os.path.getsize(p)
    print("Sizes (bytes) — SA+BWT+MTF+Huffman:")
    print(f"  original : {len(raw)}")
    print(f"  compressed: {sz(sbm_bin)}")
    print(f"  recovered : {sz(sbm_rec)}")
    ratio = (sz(sbm_bin)/len(raw)) if len(raw) else 0.0
    print(f"  ratio   : {ratio:.4f} (compressed/original)")
    print("  OK: files match." if raw==rec1 else "  ERROR: mismatch!")
    print()
    print("Sizes (bytes) — Huffman-only:")
    print(f"  original : {len(raw)}")
    print(f"  compressed: {sz(hfn_bin)}")
    print(f"  recovered : {sz(hfn_rec)}")
    ratio2 = (sz(hfn_bin)/len(raw)) if len(raw) else 0.0
    print(f"  ratio   : {ratio2:.4f} (compressed/original)")
    print("  OK: files match." if raw==rec2 else "  ERROR: mismatch!")

if __name__ == "__main__":
    import sys, os

    ABS_PATH = r"D:\1.SQM\1.UNIVERSIDAD\5. QUINTO SEMESTRE\2.Advanced Algorithms\Homework8\raven.txt"
    REL_PATH = os.path.join("Homework8", "raven.txt")


    candidate_paths = []
    if len(sys.argv) == 2:
        candidate_paths.append(sys.argv[1]) 
    candidate_paths.extend([ABS_PATH, REL_PATH])

    chosen = None
    for p in candidate_paths:
        if os.path.isfile(p):
            chosen = p
            break

    if chosen is None:
        print("Could not find 'raven.txt'. Tried:")
        for p in candidate_paths:
            print("  -", p)
        print("\nFix the path(s) above or pass a file path as an argument.")
        sys.exit(1)

    _run_cli(chosen)

