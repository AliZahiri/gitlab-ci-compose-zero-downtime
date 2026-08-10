import unittest

from compose_zero_downtime.rollback_command_contract import rollback_command_contract_is_safe, rollback_command_contract_violations


class RollbackCommandContractGateTests(unittest.TestCase):
    def test_immutable_verified_rollback_contract_passes(self):
        contract = {"command": "docker compose up -d app@sha256:" + "a" * 64, "target_color": "blue", "verification_command": "curl --fail http://blue/health"}

        self.assertTrue(rollback_command_contract_is_safe(contract, known_colors={"blue", "green"}))

    def test_missing_mutable_and_unknown_contract_fields_fail(self):
        violations = rollback_command_contract_violations({"command": "docker compose up -d app:latest", "target_color": "purple"}, known_colors={"blue", "green"})

        self.assertIn("command_must_reference_immutable_image_digest", violations)
        self.assertIn("target_color_must_be_known", violations)
        self.assertIn("verification_command_is_required", violations)

    def test_empty_color_set_is_invalid_policy(self):
        with self.assertRaises(ValueError):
            rollback_command_contract_violations({}, known_colors=set())


if __name__ == "__main__":
    unittest.main()
