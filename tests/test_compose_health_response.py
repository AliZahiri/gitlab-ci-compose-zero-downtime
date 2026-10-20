import unittest
from scripts.validate_compose_health_response import compose_health_response_violations
class ComposeHealthResponseTests(unittest.TestCase):
    def test_json_health_contract_passes(self): self.assertEqual((), compose_health_response_violations([{'service':'api_green','expected_status':200,'content_type':'application/json','required_field':'status'}]))
    def test_weak_contract_fails(self):
        violations=compose_health_response_violations([{'service':'api_green','expected_status':204,'content_type':'text/plain','required_field':'deep.status'}])
        self.assertIn('contract_0:expected_status_must_be_200', violations); self.assertIn('contract_0:content_type_must_be_json', violations); self.assertIn('contract_0:required_field_is_invalid', violations)
