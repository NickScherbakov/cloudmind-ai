"""Base cloud provider interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..core.models import CloudResource, ComputeResource, StorageResource, DatabaseResource, CostData


class CloudProviderBase(ABC):
    """Abstract base class for cloud providers."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize cloud provider.
        
        Args:
            config: Provider-specific configuration
        """
        self.config = config
        self._client = None
    
    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the cloud provider.
        
        Returns:
            True if authentication successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_compute_resources(self, region: Optional[str] = None) -> List[ComputeResource]:
        """
        List all compute resources.
        
        Args:
            region: Optional region filter
        
        Returns:
            List of compute resources
        """
        pass
    
    @abstractmethod
    def list_storage_resources(self, region: Optional[str] = None) -> List[StorageResource]:
        """
        List all storage resources.
        
        Args:
            region: Optional region filter
        
        Returns:
            List of storage resources
        """
        pass
    
    @abstractmethod
    def list_database_resources(self, region: Optional[str] = None) -> List[DatabaseResource]:
        """
        List all database resources.
        
        Args:
            region: Optional region filter
        
        Returns:
            List of database resources
        """
        pass
    
    @abstractmethod
    def get_resource_metrics(self, resource_id: str) -> Dict[str, Any]:
        """
        Get metrics for a specific resource.
        
        Args:
            resource_id: Resource identifier
        
        Returns:
            Dictionary of metrics
        """
        pass
    
    @abstractmethod
    def get_cost_data(self, resource_id: Optional[str] = None) -> List[CostData]:
        """
        Get cost data for resources.
        
        Args:
            resource_id: Optional resource ID filter
        
        Returns:
            List of cost data
        """
        pass
    
    @abstractmethod
    def stop_resource(self, resource_id: str) -> bool:
        """
        Stop a resource.
        
        Args:
            resource_id: Resource identifier
        
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def start_resource(self, resource_id: str) -> bool:
        """
        Start a resource.
        
        Args:
            resource_id: Resource identifier
        
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_resource(self, resource_id: str) -> bool:
        """
        Delete a resource.
        
        Args:
            resource_id: Resource identifier
        
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def resize_resource(self, resource_id: str, new_size: str) -> bool:
        """
        Resize a resource.
        
        Args:
            resource_id: Resource identifier
            new_size: New instance/resource size
        
        Returns:
            True if successful, False otherwise
        """
        pass
