from __future__ import annotations


def promotion_observation_order_violations(events: list[str]) -> tuple[str, ...]:
    required = ("candidate_healthy", "traffic_switched", "post_switch_healthy")
    if not isinstance(events, list):
        return ("events_must_be_a_list",)
    positions = {event: index for index, event in enumerate(events) if event in required}
    return tuple(f"{event}_is_missing_or_out_of_order" for index, event in enumerate(required) if event not in positions or (index and positions[event] < positions[required[index - 1]]))


def promotion_observation_order_is_safe(events: list[str]) -> bool:
    return not promotion_observation_order_violations(events)
