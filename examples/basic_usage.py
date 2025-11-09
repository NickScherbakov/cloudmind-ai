"""
Example: Basic usage of CloudMind AI programmatically.

This example demonstrates how to use CloudMind AI as a Python library.
"""

from cloudmind.core.config import settings
from cloudmind.core.models import CloudProvider
from cloudmind.providers import ProviderFactory
from cloudmind.ai import AIOptimizationService
from cloudmind.monitoring import MonitoringService


def main():
    """Main example function."""
    print("CloudMind AI - Basic Usage Example\n")
    
    # Initialize AWS provider
    print("1. Initializing AWS provider...")
    aws_config = {
        "region": settings.aws_region,
        "access_key_id": settings.aws_access_key_id,
        "secret_access_key": settings.aws_secret_access_key,
    }
    
    aws_provider = ProviderFactory.create_provider(CloudProvider.AWS, aws_config)
    aws_provider.authenticate()
    print("   ✓ AWS provider authenticated\n")
    
    # List compute resources
    print("2. Listing compute resources...")
    resources = aws_provider.list_compute_resources()
    print(f"   Found {len(resources)} compute resources\n")
    
    # Get metrics for resources
    print("3. Collecting metrics...")
    providers = {"aws": aws_provider}
    monitoring_service = MonitoringService(providers)
    
    if resources:
        metrics_map = monitoring_service.collect_metrics_batch(resources)
        print(f"   Collected metrics for {len(metrics_map)} resources\n")
        
        # Generate optimization recommendations
        print("4. Generating AI-powered recommendations...")
        ai_config = {
            "api_key": settings.openai_api_key,
            "model": settings.openai_model,
            "enabled": settings.ai_enabled,
        }
        ai_service = AIOptimizationService(ai_config)
        
        recommendations = ai_service.analyze_resources_batch(resources, metrics_map)
        print(f"   Generated {len(recommendations)} recommendations\n")
        
        # Display recommendations
        if recommendations:
            print("5. Optimization Recommendations:")
            for rec in recommendations:
                print(f"   - {rec.resource_name}: {rec.action.value}")
                print(f"     Reason: {rec.reason}")
                print(f"     Estimated Savings: ${rec.estimated_savings:.2f}/month")
                print(f"     Confidence: {rec.confidence*100:.0f}%\n")
        else:
            print("5. No optimization opportunities found. All resources are optimal!\n")
    
    # Get cost data
    print("6. Retrieving cost data...")
    cost_data = aws_provider.get_cost_data()
    total_cost = sum(c.monthly_cost for c in cost_data)
    print(f"   Total monthly cost: ${total_cost:.2f}\n")
    
    print("Example completed successfully!")


if __name__ == "__main__":
    main()
