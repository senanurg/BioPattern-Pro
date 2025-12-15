import bisect

# --- 1. NAIVE SEARCH ---
# Brute-force approach: Checks every position in the text.
# Time Complexity: O(n*m)
def naive_search(pattern, text):
    matches = []
    n = len(text)
    m = len(pattern)
    for i in range(n - m + 1):
        if text[i:i+m] == pattern:
            matches.append(i)
    return matches

# --- 2. SUFFIX ARRAY ---
# Advanced Data Structure: Sorts all suffixes alphabetically.
# Allows binary search on the text.
# Time Complexity: O(m*log n) for search
def build_suffix_array(text):
    suffixes = range(len(text))
    # Python's timsort is used here for simplicity
    return sorted(suffixes, key=lambda i: text[i:])

def suffix_array_search(pattern, text, suffix_arr):
    matches = []
    n = len(text)
    left, right = 0, n
    
    # Binary search for the left boundary
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

# --- 3. BLOOM FILTER ---
# Probabilistic Data Structure: Space-efficient existence check.
# Can return "False Positive" but never "False Negative".
class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size
    
    def _hashes(self, item):
        item_str = str(item)
        hashes = []
        for i in range(self.hash_count):
            # Simulating multiple hash functions using salt
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

# --- 4. BOYER-MOORE (Smart Search) ---
# Skips characters using the Bad Character Heuristic.
# Best case time complexity: O(n/m)
def boyer_moore_search(pattern, text):
    m = len(pattern)
    n = len(text)
    if m > n: return []

    # Preprocessing: Bad Character Heuristic
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