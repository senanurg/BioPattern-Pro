import sys

# ==============================================================================
# 1. NAIVE SEARCH (Brute Force)
# ==============================================================================
def naive_search(pattern, text):
    """
    Checks every position in the text to see if the pattern matches.
    Time Complexity: O(n*m)
    """
    # Validation: Empty strings or pattern longer than text
    if not pattern or not text or len(pattern) > len(text):
        return []

    matches = []
    n = len(text)
    m = len(pattern)

    # Loop through the text
    for i in range(n - m + 1):
        # Check for exact match
        if text[i:i+m] == pattern:
            matches.append(i)
            
    return matches

# ==============================================================================
# 2. RABIN-KARP (Rolling Hash)
# ==============================================================================
def rabin_karp_search(pattern, text):
    """
    Uses hashing to find the pattern. Efficient for multiple pattern searches.
    Time Complexity: Average O(n+m), Worst O(n*m)
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    d = 256  # Alphabet size (ASCII)
    q = 101  # A prime number to reduce hash collisions
    m = len(pattern)
    n = len(text)
    p = 0    # Hash value for pattern
    t = 0    # Hash value for text
    h = 1
    matches = []

    # Calculate h = pow(d, m-1) % q
    for i in range(m-1):
        h = (h * d) % q

    # Calculate hash value of pattern and first window of text
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    # Slide the pattern over text
    for i in range(n - m + 1):
        # If hash values match, check characters one by one
        if p == t:
            if text[i:i+m] == pattern:
                matches.append(i)

        # Calculate hash for next window
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i+m])) % q
            # Handle negative values
            if t < 0:
                t = t + q
                
    return matches

# ==============================================================================
# 3. KMP SEARCH (Knuth-Morris-Pratt)
# ==============================================================================
def kmp_search(pattern, text):
    """
    Uses a prefix table (LPS) to skip unnecessary comparisons.
    Time Complexity: O(n+m)
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    # Helper function to compute LPS array
    def compute_lps(p):
        lps = [0] * len(p)
        length = 0
        i = 1
        while i < len(p):
            if p[i] == p[length]:
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

# ==============================================================================
# 4. BOYER-MOORE (Bad Character Heuristic)
# ==============================================================================
def boyer_moore_search(pattern, text):
    """
    Skips characters using the Bad Character Heuristic. Often the fastest.
    Time Complexity: Best O(n/m), Worst O(n*m)
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    m = len(pattern)
    n = len(text)
    matches = []

    # Create Bad Character Table
    bad_char = {}
    for i in range(m):
        bad_char[pattern[i]] = i

    s = 0  # Shift of the pattern with respect to text
    while s <= n - m:
        j = m - 1
        
        # Keep reducing j while characters of pattern and text are matching
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            # Pattern occurs at shift s
            matches.append(s)
            # Shift pattern to align with next occurrence
            s += (m - bad_char.get(text[s + m], -1) if s + m < n else 1)
        else:
            # Shift pattern so that bad character in text aligns with last occurrence in pattern
            s += max(1, j - bad_char.get(text[s + j], -1))

    return matches

# ==============================================================================
# 5. SUFFIX ARRAY
# ==============================================================================
def build_suffix_array(text):
    """
    Builds a suffix array for the given text.
    """
    suffixes = range(len(text))
    return sorted(suffixes, key=lambda i: text[i:])

def suffix_array_search(pattern, text, suffix_arr):
    """
    Binary search using the suffix array.
    """
    if not pattern or not text:
        return []
        
    matches = []
    n = len(text)
    left, right = 0, n
    
    # Binary search for the starting position
    while left < right:
        mid = (left + right) // 2
        suffix = text[suffix_arr[mid]:]
        if pattern > suffix[:len(pattern)]:
            left = mid + 1
        else:
            right = mid
    
    start = left
    # Collect all matching suffixes
    while start < n:
        suffix_index = suffix_arr[start]
        suffix = text[suffix_index:]
        if suffix.startswith(pattern):
            matches.append(suffix_index)
            start += 1
        else:
            break
            
    return sorted(matches)

# ==============================================================================
# 6. BLOOM FILTER
# ==============================================================================
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
    """
    Builds a Bloom Filter from k-mers of the text.
    """
    bf = BloomFilter(bf_size, hash_count)
    if len(text) < k:
        return bf
        
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        bf.add(kmer)
    return bf