import unittest
from scripts.proxy_cache_bypass_contract import proxy_cache_bypass_is_safe, proxy_cache_bypass_violations

class ProxyCacheBypassContractTests(unittest.TestCase):
    def test_explicit_strategy_and_unique_paths_pass(self):
        self.assertTrue(proxy_cache_bypass_is_safe(["/health", "/version"], strategy="bypass"))
    def test_missing_strategy_and_duplicate_paths_fail(self):
        self.assertIn("cache_strategy_must_be_explicit", proxy_cache_bypass_violations(["/health"], strategy="none"))
        self.assertIn("path_1_must_be_a_unique_absolute_path", proxy_cache_bypass_violations(["/health", "/health"], strategy="bypass"))

if __name__ == "__main__":
    unittest.main()
