"""Utility functions for CloudMind AI."""

from typing import Dict, Any, List
from datetime import datetime
import json


def format_timestamp(dt: datetime) -> str:
    """Format datetime as ISO string."""
    return dt.isoformat()


def parse_timestamp(ts: str) -> datetime:
    """Parse ISO timestamp string."""
    return datetime.fromisoformat(ts)


def format_cost(amount: float, currency: str = "USD") -> str:
    """Format cost with currency symbol."""
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
    }
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:.2f}"


def calculate_percentage(value: float, total: float) -> float:
    """Calculate percentage safely."""
    if total == 0:
        return 0.0
    return (value / total) * 100


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers."""
    if denominator == 0:
        return default
    return numerator / denominator


def filter_dict(data: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """Filter dictionary to only include specified keys."""
    return {k: v for k, v in data.items() if k in keys}


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries."""
    result = {}
    for d in dicts:
        result.update(d)
    return result


def pretty_json(data: Any) -> str:
    """Format data as pretty JSON string."""
    return json.dumps(data, indent=2, default=str)
