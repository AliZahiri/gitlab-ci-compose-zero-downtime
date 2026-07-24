from __future__ import annotations


_FORWARD = ("prepared", "candidate_started", "candidate_healthy", "proxy_validated", "promoted")


def transition_journal_violations(states: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    if not states:
        return ("deployment_transition_journal_is_required",)
    normalized = tuple(str(state).strip().lower() for state in states)
    if len(set(normalized)) != len(normalized):
        return ("deployment_transition_states_must_be_unique",)
    if normalized[-1] == "rolled_back":
        normalized = normalized[:-1]
        if not normalized:
            return ("rollback_requires_a_started_deployment",)
    unknown = tuple(state for state in normalized if state not in _FORWARD)
    if unknown:
        return ("unknown_deployment_transition_state:" + ",".join(unknown),)
    expected = _FORWARD[: len(normalized)]
    if normalized != expected:
        return ("deployment_transition_order_is_invalid",)
    return ()


def transition_journal_is_valid(states: list[str] | tuple[str, ...]) -> bool:
    return not transition_journal_violations(states)
