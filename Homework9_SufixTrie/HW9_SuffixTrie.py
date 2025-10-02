# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 3
# Luis Salomón Flores Ugalde

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ SUFFIX TIRE ------

class TrieNode:
    __slots__ = ("children", "is_end")
    def __init__(self):
        self.children = {}     
        self.is_end = False   

class Trie:
    def __init__(self, words=None):
        self.root = TrieNode()
        if words:
            for w in words:
                self.insert(w)

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


class SuffixTrieNode:
    __slots__ = ("children", "indices")
    def __init__(self):
        self.children = {}      
        self.indices = []       


class SuffixTrie:
    def __init__(self, text: str):
        self.text = text
        self.root = SuffixTrieNode()
        self._build()

    def _build(self):
        t = self.text
        n = len(t)
        for i in range(n):
            node = self.root
            node.indices.append(i)
            for ch in t[i:]:
                if ch not in node.children:
                    node.children[ch] = SuffixTrieNode()
                node = node.children[ch]
                node.indices.append(i)

    def occurrences(self, pattern: str):
        if not pattern:
            return []
        node = self.root
        for ch in pattern:
            if ch not in node.children:
                return []
            node = node.children[ch]
        m = len(pattern)
        return sorted(i for i in node.indices if i + m <= len(self.text) and self.text[i:i+m] == pattern)



if __name__ == "__main__":
    words = ["Fire", "Fira", "Firaga", "Firaja"]
    trie = Trie(words)
    tests = ["Fire", "Fira", "Firaga", "Firaja", "Firas", "Fi"]
    print("Dictionary Trie tests:")
    for w in tests:
        print(f"  {w!r}: {'FOUND' if trie.search(w) else 'NOT FOUND'}")

    text = "anabanana"
    st = SuffixTrie(text)
    patterns = ["ana", "nana", "ban", "x", "a", "anabanana"]
    print("\nSuffix Trie pattern searches in text:", text)
    for p in patterns:
        print(f"  {p!r} -> indices {st.occurrences(p)}")
