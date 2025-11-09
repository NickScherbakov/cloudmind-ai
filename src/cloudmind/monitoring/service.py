"""Resource monitoring service."""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from ..core.models import (
    CloudResource, MonitoringMetrics, AlertConfig
)
from ..core.logger import logger
from ..providers.base import CloudProviderBase


class MonitoringService:
    """Service for monitoring cloud resources."""
    
    def __init__(self, providers: Dict[str, CloudProviderBase]):
        """
        Initialize monitoring service.
        
        Args:
            providers: Dictionary mapping provider names to provider instances
        """
        self.providers = providers
        self.alerts: List[AlertConfig] = []
        self.metrics_history: Dict[str, List[MonitoringMetrics]] = {}
    
    def collect_metrics(self, resource: CloudResource) -> MonitoringMetrics:
        """
        Collect current metrics for a resource.
        
        Args:
            resource: Cloud resource to monitor
        
        Returns:
            Current monitoring metrics
        """
        logger.debug(f"Collecting metrics for resource {resource.id}")
        
        provider = self.providers.get(resource.provider.value)
        if not provider:
            logger.warning(f"No provider found for {resource.provider}")
            return MonitoringMetrics(
                resource_id=resource.id,
                timestamp=datetime.utcnow()
            )
        
        try:
            raw_metrics = provider.get_resource_metrics(resource.id)
            
            metrics = MonitoringMetrics(
                resource_id=resource.id,
                timestamp=datetime.utcnow(),
                cpu_percent=raw_metrics.get("cpu_usage"),
                memory_percent=raw_metrics.get("memory_usage"),
                disk_percent=raw_metrics.get("disk_usage"),
                network_in_mbps=raw_metrics.get("network_in"),
                network_out_mbps=raw_metrics.get("network_out"),
                custom_metrics=raw_metrics.get("custom_metrics", {})
            )
            
            # Store in history
            if resource.id not in self.metrics_history:
                self.metrics_history[resource.id] = []
            self.metrics_history[resource.id].append(metrics)
            
            # Keep only last 1000 metrics per resource
            if len(self.metrics_history[resource.id]) > 1000:
                self.metrics_history[resource.id] = self.metrics_history[resource.id][-1000:]
            
            return metrics
        except Exception as e:
            logger.error(f"Failed to collect metrics for {resource.id}: {e}")
            return MonitoringMetrics(
                resource_id=resource.id,
                timestamp=datetime.utcnow()
            )
    
    def collect_metrics_batch(
        self,
        resources: List[CloudResource]
    ) -> Dict[str, MonitoringMetrics]:
        """
        Collect metrics for multiple resources.
        
        Args:
            resources: List of resources to monitor
        
        Returns:
            Dictionary mapping resource IDs to metrics
        """
        logger.info(f"Collecting metrics for {len(resources)} resources")
        
        metrics_map = {}
        for resource in resources:
            try:
                metrics = self.collect_metrics(resource)
                metrics_map[resource.id] = metrics
            except Exception as e:
                logger.warning(f"Failed to collect metrics for {resource.id}: {e}")
                continue
        
        return metrics_map
    
    def get_metrics_history(
        self,
        resource_id: str,
        hours: int = 24
    ) -> List[MonitoringMetrics]:
        """
        Get historical metrics for a resource.
        
        Args:
            resource_id: Resource identifier
            hours: Number of hours of history to retrieve
        
        Returns:
            List of historical metrics
        """
        if resource_id not in self.metrics_history:
            return []
        
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        return [
            m for m in self.metrics_history[resource_id]
            if m.timestamp >= cutoff
        ]
    
    def add_alert(self, alert: AlertConfig) -> None:
        """
        Add an alert configuration.
        
        Args:
            alert: Alert configuration
        """
        logger.info(f"Adding alert: {alert.name}")
        self.alerts.append(alert)
    
    def check_alerts(
        self,
        resource: CloudResource,
        metrics: MonitoringMetrics
    ) -> List[Dict[str, Any]]:
        """
        Check if any alerts are triggered for a resource.
        
        Args:
            resource: Cloud resource
            metrics: Current metrics
        
        Returns:
            List of triggered alerts
        """
        triggered_alerts = []
        
        for alert in self.alerts:
            if not alert.enabled:
                continue
            
            if alert.resource_id and alert.resource_id != resource.id:
                continue
            
            # Check metric thresholds
            metric_value = None
            if alert.metric == "cpu":
                metric_value = metrics.cpu_percent
            elif alert.metric == "memory":
                metric_value = metrics.memory_percent
            elif alert.metric == "disk":
                metric_value = metrics.disk_percent
            
            if metric_value is not None and metric_value >= alert.threshold:
                triggered_alerts.append({
                    "alert_name": alert.name,
                    "resource_id": resource.id,
                    "resource_name": resource.name,
                    "metric": alert.metric,
                    "value": metric_value,
                    "threshold": alert.threshold,
                    "timestamp": metrics.timestamp
                })
                logger.warning(
                    f"Alert triggered: {alert.name} - {resource.name} "
                    f"{alert.metric}={metric_value:.2f} >= {alert.threshold}"
                )
        
        return triggered_alerts
    
    def get_resource_health(
        self,
        resource: CloudResource,
        metrics: MonitoringMetrics
    ) -> Dict[str, Any]:
        """
        Assess overall health of a resource.
        
        Args:
            resource: Cloud resource
            metrics: Current metrics
        
        Returns:
            Health assessment
        """
        issues = []
        health_score = 100.0
        
        if metrics.cpu_percent:
            if metrics.cpu_percent > 90:
                issues.append("Critical CPU usage")
                health_score -= 30
            elif metrics.cpu_percent > 80:
                issues.append("High CPU usage")
                health_score -= 15
        
        if metrics.memory_percent:
            if metrics.memory_percent > 90:
                issues.append("Critical memory usage")
                health_score -= 30
            elif metrics.memory_percent > 80:
                issues.append("High memory usage")
                health_score -= 15
        
        if metrics.disk_percent:
            if metrics.disk_percent > 90:
                issues.append("Critical disk usage")
                health_score -= 20
            elif metrics.disk_percent > 80:
                issues.append("High disk usage")
                health_score -= 10
        
        health_status = "healthy"
        if health_score < 50:
            health_status = "critical"
        elif health_score < 70:
            health_status = "warning"
        
        return {
            "resource_id": resource.id,
            "resource_name": resource.name,
            "health_status": health_status,
            "health_score": health_score,
            "issues": issues,
            "timestamp": datetime.utcnow()
        }
