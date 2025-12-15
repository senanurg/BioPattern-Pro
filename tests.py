import unittest
# Assuming your algorithm functions are named like this in algorithms.py
from algorithms import kmp_search, boyer_moore_search, naive_search 

class TestPatternMatching(unittest.TestCase):

    def setUp(self):
        # Common test data used across multiple tests
        self.dna_sequence = "AGCTGAGCTATA"
        self.pattern = "AGCT"

    def test_kmp_basic_match(self):
        """Tests KMP for basic pattern matching."""
        # FIX: Arguments swapped to match algorithms.py -> (pattern, text)
        result = kmp_search(self.pattern, self.dna_sequence)
        # Expected indices for 'AGCT' in 'AGCTGAGCTATA' are 0 and 5
        self.assertEqual(result, [0, 5], "KMP failed to find all occurrences.")

    def test_boyer_moore_no_match(self):
        """Tests Boyer-Moore when the pattern is not found."""
        # FIX: Arguments swapped -> (pattern, text)
        result = boyer_moore_search("ZZZZ", self.dna_sequence)
        self.assertEqual(result, [], "Boyer-Moore found a pattern that shouldn't exist.")

    def test_naive_overlapping_patterns(self):
        """Tests Naive search with an overlapping pattern."""
        # FIX: Arguments swapped -> (pattern="AAA", text="AAAAA")
        result = naive_search("AAA", "AAAAA")
        # Expected to find at indices 0, 1, 2
        self.assertEqual(result, [0, 1, 2], "Naive search failed with overlapping patterns.")

    def test_pattern_longer_than_text(self):
        """Tests any algorithm when the pattern is longer than the text."""
        # FIX: Arguments swapped -> (pattern="ABCDE", text="ABC")
        result = kmp_search("ABCDE", "ABC")
        self.assertEqual(result, [], "Search should return empty list when pattern is too long.")

    def test_empty_pattern(self):
        """Tests case where an empty pattern is searched."""
        # FIX: Arguments swapped -> (pattern="", text=self.dna_sequence)
        result = naive_search("", self.dna_sequence)
        self.assertEqual(result, [], "Searching for an empty pattern should return [].")


if __name__ == '__main__':
    # Running the tests
    unittest.main()