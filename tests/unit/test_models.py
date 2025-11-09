"""Unit tests for core models."""

import pytest
from datetime import datetime
from cloudmind.core.models import (
    CloudProvider,
    ResourceType,
    ResourceStatus,
    OptimizationAction,
    ComputeResource,
    StorageResource,
    CostData,
    OptimizationRecommendation,
)


def test_cloud_provider_enum():
    """Test CloudProvider enum values."""
    assert CloudProvider.AWS.value == "aws"
    assert CloudProvider.AZURE.value == "azure"
    assert CloudProvider.GCP.value == "gcp"
    assert CloudProvider.ONPREM.value == "onprem"


def test_resource_type_enum():
    """Test ResourceType enum values."""
    assert ResourceType.COMPUTE.value == "compute"
    assert ResourceType.STORAGE.value == "storage"
    assert ResourceType.DATABASE.value == "database"


def test_compute_resource_creation():
    """Test ComputeResource model creation."""
    resource = ComputeResource(
        id="i-1234567890",
        name="test-instance",
        provider=CloudProvider.AWS,
        resource_type=ResourceType.COMPUTE,
        status=ResourceStatus.RUNNING,
        region="us-east-1",
        created_at=datetime.utcnow(),
        instance_type="t3.medium",
        cpu_cores=2,
        memory_gb=4.0,
    )
    
    assert resource.id == "i-1234567890"
    assert resource.name == "test-instance"
    assert resource.provider == CloudProvider.AWS
    assert resource.instance_type == "t3.medium"
    assert resource.cpu_cores == 2
    assert resource.memory_gb == 4.0


def test_storage_resource_creation():
    """Test StorageResource model creation."""
    resource = StorageResource(
        id="bucket-123",
        name="my-bucket",
        provider=CloudProvider.AWS,
        resource_type=ResourceType.STORAGE,
        status=ResourceStatus.RUNNING,
        region="us-east-1",
        created_at=datetime.utcnow(),
        storage_type="s3",
        size_gb=100.0,
    )
    
    assert resource.storage_type == "s3"
    assert resource.size_gb == 100.0


def test_cost_data_creation():
    """Test CostData model creation."""
    cost = CostData(
        resource_id="i-1234567890",
        provider=CloudProvider.AWS,
        daily_cost=10.50,
        monthly_cost=315.00,
        last_updated=datetime.utcnow(),
    )
    
    assert cost.resource_id == "i-1234567890"
    assert cost.daily_cost == 10.50
    assert cost.monthly_cost == 315.00
    assert cost.currency == "USD"


def test_optimization_recommendation_creation():
    """Test OptimizationRecommendation model creation."""
    rec = OptimizationRecommendation(
        resource_id="i-1234567890",
        resource_name="test-instance",
        provider=CloudProvider.AWS,
        action=OptimizationAction.DOWNSIZE,
        reason="Low CPU usage",
        estimated_savings=50.0,
        confidence=0.85,
    )
    
    assert rec.action == OptimizationAction.DOWNSIZE
    assert rec.estimated_savings == 50.0
    assert rec.confidence == 0.85


def test_optimization_recommendation_confidence_validation():
    """Test that confidence is validated between 0 and 1."""
    # Valid confidence
    rec = OptimizationRecommendation(
        resource_id="i-1234567890",
        resource_name="test-instance",
        provider=CloudProvider.AWS,
        action=OptimizationAction.DOWNSIZE,
        reason="Test",
        estimated_savings=50.0,
        confidence=0.5,
    )
    assert rec.confidence == 0.5
    
    # Invalid confidence (too high)
    with pytest.raises(Exception):
        OptimizationRecommendation(
            resource_id="i-1234567890",
            resource_name="test-instance",
            provider=CloudProvider.AWS,
            action=OptimizationAction.DOWNSIZE,
            reason="Test",
            estimated_savings=50.0,
            confidence=1.5,
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
