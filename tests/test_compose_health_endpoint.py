import unittest
from scripts.validate_compose_health_endpoint import compose_health_endpoint_violations
class ComposeHealthEndpointContractTests(unittest.TestCase):
    def test_public_bounded_health_endpoint_passes(self):
        endpoint={'service':'api_green','path':'/healthz','expected_status':200,'timeout_seconds':5,'authentication_required':False}
        self.assertEqual((), compose_health_endpoint_violations([endpoint]))
    def test_unsafe_endpoint_fails(self):
        endpoint={'service':'api_green','path':'health?debug=1','expected_status':204,'timeout_seconds':31,'authentication_required':True}
        violations=compose_health_endpoint_violations([endpoint])
        self.assertIn('endpoint_0:path_must_be_an_absolute_endpoint', violations); self.assertIn('endpoint_0:expected_status_must_be_200', violations); self.assertIn('endpoint_0:health_probe_must_not_require_authentication', violations)
