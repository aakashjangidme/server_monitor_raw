from typing import Dict


def parse_unit_value(value_str: str) -> float:
    unit = value_str[-2:].lower()
    value = float(value_str[:-2])
    if unit == 'gb':
        value *= 1024  # Convert GB to MB
    return value


def gb_to_mb(value: float) -> float:
    return value * 1024  # Convert GB to MB


def parse_condition(condition_str: str) -> Dict:
    """
    Parse the condition string into a dictionary with 'metric', 'operator', and 'value'.
    Example: "memory < 5.gb" -> {'metric': 'memory', 'operator': '<', 'value': 5.0}
    """
    parts = condition_str.split()
    metric = parts[0]
    operator = parts[1]
    value = parse_unit_value(parts[2])
    return {'metric': metric, 'operator': operator, 'value': value}
