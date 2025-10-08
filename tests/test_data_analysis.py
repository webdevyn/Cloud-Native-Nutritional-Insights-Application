import unittest
import data_analysis  # this imports your actual file

class TestDataAnalysis(unittest.TestCase):
    def test_module_import(self):
        """Check that the module imports successfully"""
        self.assertIsNotNone(data_analysis)

    def test_some_function(self):
        """Replace with an actual test from your code"""
        if hasattr(data_analysis, "analyze_data"):
            result = data_analysis.analyze_data([1, 2, 3])
            self.assertIsInstance(result, dict)  # Example check
        else:
            self.skipTest("No analyze_data function found yet")

if __name__ == "__main__":
    unittest.main()
