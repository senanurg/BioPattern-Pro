import bisect

# --- 1. NAIVE SEARCH (Brute Force) ---
# Time Complexity: O(n*m)
# Description: The simplest method that checks every position in the text.
def naive_search(pattern, text):
    matches = []
    n = len(text)
    m = len(pattern)
    for i in range(n - m + 1):
        if text[i:i+m] == pattern:
            matches.append(i)
    return matches

# --- 2. RABIN-KARP (Rolling Hash) ---
# Time Complexity: Average O(n+m), Worst O(n*m)
# Description: Uses hashing to find the pattern. Effective for multiple pattern searches.
def rabin_karp_search(pattern, text):
    d = 256 # Alphabet size (ASCII)
    q = 101 # A prime number to reduce hash collisions
    M = len(pattern)
    N = len(text)
    p = 0    # Hash value for pattern
    t = 0    # Hash value for text
    h = 1
    matches = []

    if M > N: return matches

    # The value of h would be "pow(d, M-1)%q"
    for i in range(M-1):
        h = (h * d) % q

    # Calculate the hash value of pattern and first window of text
    for i in range(M):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    # Slide the pattern over text one by one
    for i in range(N - M + 1):
        # If the hash values match, then only check for characters one by one
        if p == t:
            if text[i:i+M] == pattern:
                matches.append(i)
        
        # Calculate hash value for next window of text: Remove leading digit, add trailing digit
        if i < N - M:
            t = (d*(t - ord(text[i])*h) + ord(text[i+M])) % q
            # We might get negative value of t, converting it to positive
            if t < 0:
                t = t + q
    return matches

# --- 3. KMP SEARCH (Knuth-Morris-Pratt) ---
# Time Complexity: O(n+m)
# Description: Uses a prefix table (LPS) to skip unnecessary comparisons.
def kmp_search(pattern, text):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
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

    matches = []
    n = len(text)
    m = len(pattern)
    if m == 0: return []
    
    lps = compute_lps(pattern)
    i = 0  # index for text
    j = 0  # index for pattern
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches

# --- 4. BOYER-MOORE (Smart Search) ---
# Time Complexity: Best O(n/m), Worst O(n*m)
# Description: Skips characters using the Bad Character Heuristic.
def boyer_moore_search(pattern, text):
    m = len(pattern)
    n = len(text)
    if m > n: return []

    bad_char = {}
    for i in range(m):
        bad_char[pattern[i]] = i

    matches = []
    s = 0 
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        
        if j < 0:
            matches.append(s)
            s += (m - bad_char.get(text[s + m], -1)) if s + m < n else 1
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))
            
    return matches

# --- 5. SUFFIX ARRAY (Indexing) ---
# Time Complexity: Search is O(m * log n)
# Description: Sorts all suffixes to allow binary search. Excellent for repeated queries on static data.
def build_suffix_array(text):
    suffixes = range(len(text))
    return sorted(suffixes, key=lambda i: text[i:])

def suffix_array_search(pattern, text, suffix_arr):
    matches = []
    n = len(text)
    left, right = 0, n
    
    while left < right:
        mid = (left + right) // 2
        suffix = text[suffix_arr[mid]:]
        if pattern > suffix[:len(pattern)]:
            left = mid + 1
        else:
            right = mid
    
    start = left
    while start < n:
        suffix_index = suffix_arr[start]
        suffix = text[suffix_index:]
        if suffix.startswith(pattern):
            matches.append(suffix_index)
            start += 1
        else:
            break
            
    return sorted(matches)

# --- 6. BLOOM FILTER (Probabilistic) ---
# Description: Space-efficient structure to check existence.
class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size
    
    def _hashes(self, item):
        item_str = str(item)
        hashes = []
        for i in range(self.hash_count):
            h = hash(item_str + str(i)) % self.size
            hashes.append(h)
        return hashes

    def add(self, item):
        for h in self._hashes(item):
            self.bit_array[h] = 1

    def check(self, item):
        for h in self._hashes(item):
            if self.bit_array[h] == 0:
                return False
        return True

def build_bloom_filter(text, k, bf_size=200000, hash_count=3):
    bf = BloomFilter(bf_size, hash_count)
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        bf.add(kmer)
    return bf