"""Data models and schemas for CloudMind AI."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from pydantic import BaseModel, Field


class CloudProvider(str, Enum):
    """Supported cloud providers."""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ONPREM = "onprem"


class ResourceType(str, Enum):
    """Cloud resource types."""
    COMPUTE = "compute"
    STORAGE = "storage"
    DATABASE = "database"
    NETWORK = "network"
    SERVERLESS = "serverless"
    OTHER = "other"


class ResourceStatus(str, Enum):
    """Resource status."""
    RUNNING = "running"
    STOPPED = "stopped"
    TERMINATED = "terminated"
    PENDING = "pending"
    UNKNOWN = "unknown"


class OptimizationAction(str, Enum):
    """Optimization action types."""
    DOWNSIZE = "downsize"
    UPSIZE = "upsize"
    STOP = "stop"
    START = "start"
    MIGRATE = "migrate"
    DELETE = "delete"
    NONE = "none"


class CloudResource(BaseModel):
    """Base model for cloud resources."""
    id: str
    name: str
    provider: CloudProvider
    resource_type: ResourceType
    status: ResourceStatus
    region: str
    created_at: datetime
    tags: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ComputeResource(CloudResource):
    """Compute resource (VM, instance, etc.)."""
    instance_type: str
    cpu_cores: int
    memory_gb: float
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    disk_usage: Optional[float] = None


class StorageResource(CloudResource):
    """Storage resource (bucket, blob, etc.)."""
    storage_type: str
    size_gb: float
    used_gb: Optional[float] = None


class DatabaseResource(CloudResource):
    """Database resource."""
    database_type: str
    engine: str
    version: str
    size_gb: float
    connections: Optional[int] = None


class CostData(BaseModel):
    """Cost information for resources."""
    resource_id: str
    provider: CloudProvider
    daily_cost: float
    monthly_cost: float
    currency: str = "USD"
    last_updated: datetime


class OptimizationRecommendation(BaseModel):
    """Optimization recommendation."""
    resource_id: str
    resource_name: str
    provider: CloudProvider
    action: OptimizationAction
    reason: str
    estimated_savings: float
    confidence: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AlertConfig(BaseModel):
    """Alert configuration."""
    name: str
    resource_id: Optional[str] = None
    metric: str
    threshold: float
    enabled: bool = True


class MonitoringMetrics(BaseModel):
    """Monitoring metrics for a resource."""
    resource_id: str
    timestamp: datetime
    cpu_percent: Optional[float] = None
    memory_percent: Optional[float] = None
    disk_percent: Optional[float] = None
    network_in_mbps: Optional[float] = None
    network_out_mbps: Optional[float] = None
    custom_metrics: Dict[str, float] = Field(default_factory=dict)
