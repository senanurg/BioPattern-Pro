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
        # Expected indices for 'AGCT' in 'AGCTGAGCTATA' are 0 and 5
        result = kmp_search(self.dna_sequence, self.pattern)
        self.assertEqual(result, [0, 5], "KMP failed to find all occurrences.")

    def test_boyer_moore_no_match(self):
        """Tests Boyer-Moore when the pattern is not found."""
        result = boyer_moore_search(self.dna_sequence, "ZZZZ")
        self.assertEqual(result, [], "Boyer-Moore found a pattern that shouldn't exist.")

    def test_naive_overlapping_patterns(self):
        """Tests Naive search with an overlapping pattern."""
        result = naive_search("AAAAA", "AAA")
        # Expected to find at indices 0, 1, 2
        self.assertEqual(result, [0, 1, 2], "Naive search failed with overlapping patterns.")

    def test_pattern_longer_than_text(self):
        """Tests any algorithm when the pattern is longer than the text."""
        # We can use any search function here, the result should be an empty list
        result = kmp_search("ABC", "ABCDE")
        self.assertEqual(result, [], "Search should return empty list when pattern is too long.")

    def test_empty_pattern(self):
        """Tests case where an empty pattern is searched."""
        # Searching for an empty pattern typically returns an error or an empty list, 
        # depending on the implementation design. Here we expect an empty list.
        result = naive_search(self.dna_sequence, "")
        self.assertEqual(result, [], "Searching for an empty pattern should return [].")


if __name__ == '__main__':
    # Running the tests
    unittest.main()