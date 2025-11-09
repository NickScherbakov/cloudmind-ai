"""Unit tests for utility functions."""

import pytest
from datetime import datetime
from cloudmind.utils.helpers import (
    format_timestamp,
    parse_timestamp,
    format_cost,
    calculate_percentage,
    safe_divide,
    filter_dict,
    merge_dicts,
)


def test_format_timestamp():
    """Test timestamp formatting."""
    dt = datetime(2024, 1, 15, 10, 30, 0)
    formatted = format_timestamp(dt)
    assert isinstance(formatted, str)
    assert "2024-01-15" in formatted


def test_parse_timestamp():
    """Test timestamp parsing."""
    ts_str = "2024-01-15T10:30:00"
    dt = parse_timestamp(ts_str)
    assert isinstance(dt, datetime)
    assert dt.year == 2024
    assert dt.month == 1
    assert dt.day == 15


def test_format_cost_usd():
    """Test cost formatting with USD."""
    formatted = format_cost(100.50, "USD")
    assert formatted == "$100.50"


def test_format_cost_eur():
    """Test cost formatting with EUR."""
    formatted = format_cost(100.50, "EUR")
    assert formatted == "€100.50"


def test_calculate_percentage():
    """Test percentage calculation."""
    result = calculate_percentage(25, 100)
    assert result == 25.0
    
    result = calculate_percentage(1, 4)
    assert result == 25.0


def test_calculate_percentage_zero_total():
    """Test percentage calculation with zero total."""
    result = calculate_percentage(10, 0)
    assert result == 0.0


def test_safe_divide():
    """Test safe division."""
    result = safe_divide(10, 2)
    assert result == 5.0
    
    result = safe_divide(10, 0)
    assert result == 0.0
    
    result = safe_divide(10, 0, default=999)
    assert result == 999


def test_filter_dict():
    """Test dictionary filtering."""
    data = {"a": 1, "b": 2, "c": 3, "d": 4}
    filtered = filter_dict(data, ["a", "c"])
    assert filtered == {"a": 1, "c": 3}


def test_merge_dicts():
    """Test dictionary merging."""
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    dict3 = {"e": 5}
    
    merged = merge_dicts(dict1, dict2, dict3)
    assert merged == {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}


def test_merge_dicts_overwrites():
    """Test that merge_dicts overwrites keys."""
    dict1 = {"a": 1, "b": 2}
    dict2 = {"b": 3, "c": 4}
    
    merged = merge_dicts(dict1, dict2)
    assert merged["b"] == 3  # Later dict overwrites


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
