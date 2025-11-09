"""Cloud provider factory and initialization."""

from typing import Dict, Any, List
from ..core.models import CloudProvider
from ..core.exceptions import ConfigurationError
from ..core.logger import logger
from .base import CloudProviderBase
from .aws import AWSProvider
from .azure import AzureProvider
from .gcp import GCPProvider
from .onprem import OnPremProvider


class ProviderFactory:
    """Factory for creating cloud provider instances."""
    
    _providers = {
        CloudProvider.AWS: AWSProvider,
        CloudProvider.AZURE: AzureProvider,
        CloudProvider.GCP: GCPProvider,
        CloudProvider.ONPREM: OnPremProvider,
    }
    
    @classmethod
    def create_provider(cls, provider_type: CloudProvider, config: Dict[str, Any]) -> CloudProviderBase:
        """
        Create a cloud provider instance.
        
        Args:
            provider_type: Type of cloud provider
            config: Provider configuration
        
        Returns:
            Cloud provider instance
        
        Raises:
            ConfigurationError: If provider type is not supported
        """
        provider_class = cls._providers.get(provider_type)
        if not provider_class:
            raise ConfigurationError(f"Unsupported provider: {provider_type}")
        
        logger.info(f"Creating provider instance for {provider_type}")
        return provider_class(config)
    
    @classmethod
    def get_supported_providers(cls) -> List[CloudProvider]:
        """Get list of supported providers."""
        return list(cls._providers.keys())


__all__ = [
    "CloudProviderBase",
    "AWSProvider",
    "AzureProvider",
    "GCPProvider",
    "OnPremProvider",
    "ProviderFactory"
]
