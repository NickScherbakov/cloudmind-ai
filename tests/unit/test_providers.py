"""Unit tests for provider factory."""

import pytest
from cloudmind.core.models import CloudProvider
from cloudmind.core.exceptions import ConfigurationError
from cloudmind.providers import (
    ProviderFactory,
    AWSProvider,
    AzureProvider,
    GCPProvider,
    OnPremProvider,
)


def test_provider_factory_creates_aws_provider():
    """Test that factory creates AWS provider correctly."""
    config = {
        "region": "us-east-1",
        "access_key_id": "test_key",
        "secret_access_key": "test_secret",
    }
    
    provider = ProviderFactory.create_provider(CloudProvider.AWS, config)
    
    assert isinstance(provider, AWSProvider)
    assert provider.region == "us-east-1"


def test_provider_factory_creates_azure_provider():
    """Test that factory creates Azure provider correctly."""
    config = {
        "subscription_id": "test_subscription",
        "tenant_id": "test_tenant",
        "client_id": "test_client",
        "client_secret": "test_secret",
    }
    
    provider = ProviderFactory.create_provider(CloudProvider.AZURE, config)
    
    assert isinstance(provider, AzureProvider)
    assert provider.subscription_id == "test_subscription"


def test_provider_factory_creates_gcp_provider():
    """Test that factory creates GCP provider correctly."""
    config = {
        "project_id": "test_project",
        "credentials_path": "/path/to/creds.json",
    }
    
    provider = ProviderFactory.create_provider(CloudProvider.GCP, config)
    
    assert isinstance(provider, GCPProvider)
    assert provider.project_id == "test_project"


def test_provider_factory_creates_onprem_provider():
    """Test that factory creates on-premises provider correctly."""
    config = {
        "hosts": ["host1.example.com", "host2.example.com"],
    }
    
    provider = ProviderFactory.create_provider(CloudProvider.ONPREM, config)
    
    assert isinstance(provider, OnPremProvider)
    assert len(provider.hosts) == 2


def test_provider_factory_get_supported_providers():
    """Test that factory returns list of supported providers."""
    supported = ProviderFactory.get_supported_providers()
    
    assert CloudProvider.AWS in supported
    assert CloudProvider.AZURE in supported
    assert CloudProvider.GCP in supported
    assert CloudProvider.ONPREM in supported
    assert len(supported) == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
