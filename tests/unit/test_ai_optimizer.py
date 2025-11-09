"""Unit tests for AI optimization service."""

import pytest
from datetime import datetime
from cloudmind.core.models import (
    CloudProvider,
    ResourceType,
    ResourceStatus,
    ComputeResource,
    MonitoringMetrics,
    OptimizationAction,
)
from cloudmind.ai import AIOptimizationService


@pytest.fixture
def ai_service():
    """Create AI service instance for testing."""
    config = {
        "api_key": "test_key",
        "model": "gpt-4",
        "enabled": False,  # Disabled for testing without real API calls
    }
    return AIOptimizationService(config)


@pytest.fixture
def sample_resource():
    """Create sample resource for testing."""
    return ComputeResource(
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


@pytest.fixture
def low_cpu_metrics():
    """Create metrics with low CPU usage."""
    return MonitoringMetrics(
        resource_id="i-1234567890",
        timestamp=datetime.utcnow(),
        cpu_percent=15.0,
        memory_percent=50.0,
    )


@pytest.fixture
def high_cpu_metrics():
    """Create metrics with high CPU usage."""
    return MonitoringMetrics(
        resource_id="i-1234567890",
        timestamp=datetime.utcnow(),
        cpu_percent=95.0,
        memory_percent=80.0,
    )


def test_analyze_resource_low_cpu(ai_service, sample_resource, low_cpu_metrics):
    """Test resource analysis with low CPU usage."""
    recommendation = ai_service.analyze_resource(
        sample_resource,
        low_cpu_metrics
    )
    
    assert recommendation.resource_id == sample_resource.id
    assert recommendation.action == OptimizationAction.DOWNSIZE
    assert recommendation.estimated_savings > 0
    assert 0 <= recommendation.confidence <= 1


def test_analyze_resource_high_cpu(ai_service, sample_resource, high_cpu_metrics):
    """Test resource analysis with high CPU usage."""
    recommendation = ai_service.analyze_resource(
        sample_resource,
        high_cpu_metrics
    )
    
    assert recommendation.resource_id == sample_resource.id
    assert recommendation.action == OptimizationAction.UPSIZE
    assert 0 <= recommendation.confidence <= 1


def test_analyze_resource_without_metrics(ai_service, sample_resource):
    """Test resource analysis without metrics."""
    recommendation = ai_service.analyze_resource(sample_resource)
    
    assert recommendation.resource_id == sample_resource.id
    assert recommendation.action == OptimizationAction.NONE


def test_analyze_resources_batch(ai_service, sample_resource, low_cpu_metrics):
    """Test batch resource analysis."""
    resources = [sample_resource]
    metrics_map = {sample_resource.id: low_cpu_metrics}
    
    recommendations = ai_service.analyze_resources_batch(
        resources,
        metrics_map
    )
    
    assert len(recommendations) == 1
    assert recommendations[0].resource_id == sample_resource.id


def test_generate_report(ai_service):
    """Test optimization report generation."""
    from cloudmind.core.models import OptimizationRecommendation
    
    recommendations = [
        OptimizationRecommendation(
            resource_id="i-1",
            resource_name="instance-1",
            provider=CloudProvider.AWS,
            action=OptimizationAction.DOWNSIZE,
            reason="Low CPU",
            estimated_savings=50.0,
            confidence=0.85,
        ),
        OptimizationRecommendation(
            resource_id="i-2",
            resource_name="instance-2",
            provider=CloudProvider.AWS,
            action=OptimizationAction.STOP,
            reason="Unused",
            estimated_savings=100.0,
            confidence=0.90,
        ),
    ]
    
    report = ai_service.generate_report(recommendations)
    
    assert "summary" in report
    assert "recommendations" in report
    assert report["summary"]["total_recommendations"] == 2
    assert report["summary"]["total_estimated_savings"] == 150.0


def test_predict_usage(ai_service):
    """Test usage prediction."""
    prediction = ai_service.predict_usage("i-1234567890", [])
    
    assert "resource_id" in prediction
    assert prediction["resource_id"] == "i-1234567890"
    assert "predicted_cpu_avg" in prediction
    assert "confidence" in prediction


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
