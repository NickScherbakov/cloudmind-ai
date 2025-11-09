"""FastAPI REST API for CloudMind AI."""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime

from ..core.config import settings
from ..core.models import (
    CloudProvider, OptimizationRecommendation, MonitoringMetrics,
    CloudResource, CostData
)
from ..core.logger import logger
from ..providers import ProviderFactory
from ..ai import AIOptimizationService
from ..monitoring import MonitoringService


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Open source platform for automated management and optimization of cloud resources",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
providers = {}
monitoring_service = None
ai_service = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global providers, monitoring_service, ai_service
    
    logger.info("Starting CloudMind AI API...")
    
    # Initialize enabled providers
    if settings.aws_enabled:
        try:
            aws_config = {
                "region": settings.aws_region,
                "access_key_id": settings.aws_access_key_id,
                "secret_access_key": settings.aws_secret_access_key,
            }
            providers["aws"] = ProviderFactory.create_provider(CloudProvider.AWS, aws_config)
            providers["aws"].authenticate()
            logger.info("AWS provider initialized")
        except Exception as e:
            logger.error(f"Failed to initialize AWS provider: {e}")
    
    if settings.azure_enabled:
        try:
            azure_config = {
                "subscription_id": settings.azure_subscription_id,
                "tenant_id": settings.azure_tenant_id,
                "client_id": settings.azure_client_id,
                "client_secret": settings.azure_client_secret,
            }
            providers["azure"] = ProviderFactory.create_provider(CloudProvider.AZURE, azure_config)
            providers["azure"].authenticate()
            logger.info("Azure provider initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Azure provider: {e}")
    
    if settings.gcp_enabled:
        try:
            gcp_config = {
                "project_id": settings.gcp_project_id,
                "credentials_path": settings.gcp_credentials_path,
            }
            providers["gcp"] = ProviderFactory.create_provider(CloudProvider.GCP, gcp_config)
            providers["gcp"].authenticate()
            logger.info("GCP provider initialized")
        except Exception as e:
            logger.error(f"Failed to initialize GCP provider: {e}")
    
    if settings.onprem_enabled:
        try:
            onprem_config = {
                "hosts": settings.onprem_hosts,
            }
            providers["onprem"] = ProviderFactory.create_provider(CloudProvider.ONPREM, onprem_config)
            providers["onprem"].authenticate()
            logger.info("On-premises provider initialized")
        except Exception as e:
            logger.error(f"Failed to initialize on-premises provider: {e}")
    
    # Initialize monitoring service
    monitoring_service = MonitoringService(providers)
    logger.info("Monitoring service initialized")
    
    # Initialize AI service
    if settings.ai_enabled:
        ai_config = {
            "api_key": settings.openai_api_key,
            "model": settings.openai_model,
            "enabled": settings.ai_enabled,
        }
        ai_service = AIOptimizationService(ai_config)
        logger.info("AI optimization service initialized")
    
    logger.info("CloudMind AI API started successfully")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "providers": list(providers.keys()),
        "ai_enabled": settings.ai_enabled,
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "providers": {
            name: "connected" for name in providers.keys()
        }
    }


@app.get("/providers")
async def list_providers():
    """List available cloud providers."""
    return {
        "providers": [
            {
                "name": name,
                "type": name,
                "status": "connected"
            }
            for name in providers.keys()
        ]
    }


@app.get("/resources/compute")
async def list_compute_resources(provider: Optional[str] = None, region: Optional[str] = None):
    """List compute resources across all or specific provider."""
    all_resources = []
    
    target_providers = [provider] if provider else providers.keys()
    
    for prov_name in target_providers:
        if prov_name not in providers:
            continue
        
        try:
            resources = providers[prov_name].list_compute_resources(region)
            all_resources.extend(resources)
        except Exception as e:
            logger.error(f"Failed to list compute resources from {prov_name}: {e}")
    
    return {
        "count": len(all_resources),
        "resources": [r.model_dump() for r in all_resources]
    }


@app.get("/resources/storage")
async def list_storage_resources(provider: Optional[str] = None, region: Optional[str] = None):
    """List storage resources across all or specific provider."""
    all_resources = []
    
    target_providers = [provider] if provider else providers.keys()
    
    for prov_name in target_providers:
        if prov_name not in providers:
            continue
        
        try:
            resources = providers[prov_name].list_storage_resources(region)
            all_resources.extend(resources)
        except Exception as e:
            logger.error(f"Failed to list storage resources from {prov_name}: {e}")
    
    return {
        "count": len(all_resources),
        "resources": [r.model_dump() for r in all_resources]
    }


@app.get("/resources/database")
async def list_database_resources(provider: Optional[str] = None, region: Optional[str] = None):
    """List database resources across all or specific provider."""
    all_resources = []
    
    target_providers = [provider] if provider else providers.keys()
    
    for prov_name in target_providers:
        if prov_name not in providers:
            continue
        
        try:
            resources = providers[prov_name].list_database_resources(region)
            all_resources.extend(resources)
        except Exception as e:
            logger.error(f"Failed to list database resources from {prov_name}: {e}")
    
    return {
        "count": len(all_resources),
        "resources": [r.model_dump() for r in all_resources]
    }


@app.get("/resources/{resource_id}/metrics")
async def get_resource_metrics(resource_id: str, provider: str):
    """Get metrics for a specific resource."""
    if provider not in providers:
        raise HTTPException(status_code=404, detail=f"Provider {provider} not found")
    
    try:
        metrics = providers[provider].get_resource_metrics(resource_id)
        return metrics
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cost")
async def get_cost_data(provider: Optional[str] = None):
    """Get cost data across providers."""
    all_costs = []
    
    target_providers = [provider] if provider else providers.keys()
    
    for prov_name in target_providers:
        if prov_name not in providers:
            continue
        
        try:
            costs = providers[prov_name].get_cost_data()
            all_costs.extend(costs)
        except Exception as e:
            logger.error(f"Failed to get cost data from {prov_name}: {e}")
    
    return {
        "count": len(all_costs),
        "total_daily_cost": sum(c.daily_cost for c in all_costs),
        "total_monthly_cost": sum(c.monthly_cost for c in all_costs),
        "costs": [c.model_dump() for c in all_costs]
    }


@app.get("/optimization/recommendations")
async def get_optimization_recommendations():
    """Get AI-powered optimization recommendations."""
    if not ai_service:
        raise HTTPException(status_code=503, detail="AI service not enabled")
    
    # Collect all resources
    all_resources = []
    for prov_name in providers.keys():
        try:
            compute = providers[prov_name].list_compute_resources()
            all_resources.extend(compute)
        except Exception as e:
            logger.warning(f"Failed to get resources from {prov_name}: {e}")
    
    # Get metrics for all resources
    if monitoring_service:
        metrics_map = monitoring_service.collect_metrics_batch(all_resources)
    else:
        metrics_map = {}
    
    # Generate recommendations
    try:
        recommendations = ai_service.analyze_resources_batch(all_resources, metrics_map)
        report = ai_service.generate_report(recommendations)
        return report
    except Exception as e:
        logger.error(f"Failed to generate recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resources/{resource_id}/stop")
async def stop_resource(resource_id: str, provider: str):
    """Stop a resource."""
    if provider not in providers:
        raise HTTPException(status_code=404, detail=f"Provider {provider} not found")
    
    try:
        success = providers[provider].stop_resource(resource_id)
        return {"success": success, "resource_id": resource_id, "action": "stop"}
    except Exception as e:
        logger.error(f"Failed to stop resource: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resources/{resource_id}/start")
async def start_resource(resource_id: str, provider: str):
    """Start a resource."""
    if provider not in providers:
        raise HTTPException(status_code=404, detail=f"Provider {provider} not found")
    
    try:
        success = providers[provider].start_resource(resource_id)
        return {"success": success, "resource_id": resource_id, "action": "start"}
    except Exception as e:
        logger.error(f"Failed to start resource: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resources/{resource_id}/resize")
async def resize_resource(resource_id: str, provider: str, new_size: str):
    """Resize a resource."""
    if provider not in providers:
        raise HTTPException(status_code=404, detail=f"Provider {provider} not found")
    
    try:
        success = providers[provider].resize_resource(resource_id, new_size)
        return {"success": success, "resource_id": resource_id, "action": "resize", "new_size": new_size}
    except Exception as e:
        logger.error(f"Failed to resize resource: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/resources/{resource_id}")
async def delete_resource(resource_id: str, provider: str):
    """Delete a resource."""
    if provider not in providers:
        raise HTTPException(status_code=404, detail=f"Provider {provider} not found")
    
    try:
        success = providers[provider].delete_resource(resource_id)
        return {"success": success, "resource_id": resource_id, "action": "delete"}
    except Exception as e:
        logger.error(f"Failed to delete resource: {e}")
        raise HTTPException(status_code=500, detail=str(e))
