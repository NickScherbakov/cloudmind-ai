"""Unit tests for core configuration module."""

import pytest
from pydantic import ValidationError
from cloudmind.core.config import Settings


def test_settings_default_values():
    """Test that settings have sensible default values."""
    settings = Settings()
    
    assert settings.app_name == "CloudMind AI"
    assert settings.app_version == "0.1.0"
    assert settings.debug is False
    assert settings.api_host == "0.0.0.0"
    assert settings.api_port == 8000
    assert settings.aws_region == "us-east-1"
    assert settings.monitoring_interval == 300
    assert settings.alert_threshold_cpu == 80.0


def test_settings_from_env(monkeypatch):
    """Test that settings can be loaded from environment variables."""
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("API_PORT", "9000")
    monkeypatch.setenv("AWS_ENABLED", "true")
    
    settings = Settings()
    
    assert settings.debug is True
    assert settings.api_port == 9000
    assert settings.aws_enabled is True


def test_settings_type_validation():
    """Test that settings validate types correctly."""
    # Test with monkeypatch for environment variables
    import os
    
    # Valid type
    os.environ["API_PORT"] = "8080"
    settings = Settings()
    assert settings.api_port == 8080
    
    # Invalid type should raise error during env parsing
    os.environ["API_PORT"] = "not_a_number"
    with pytest.raises(ValidationError):
        Settings()
    
    # Clean up
    del os.environ["API_PORT"]


def test_settings_case_insensitive(monkeypatch):
    """Test that environment variables are case insensitive."""
    monkeypatch.setenv("debug", "true")
    monkeypatch.setenv("AWS_ENABLED", "true")
    
    settings = Settings()
    
    assert settings.debug is True
    assert settings.aws_enabled is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
