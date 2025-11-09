"""
Example: Multi-cloud resource management.

This example shows how to work with multiple cloud providers simultaneously.
"""

from cloudmind.core.config import settings
from cloudmind.core.models import CloudProvider
from cloudmind.providers import ProviderFactory


def initialize_providers():
    """Initialize all enabled providers."""
    providers = {}
    
    if settings.aws_enabled:
        print("Initializing AWS provider...")
        aws_config = {
            "region": settings.aws_region,
            "access_key_id": settings.aws_access_key_id,
            "secret_access_key": settings.aws_secret_access_key,
        }
        providers["aws"] = ProviderFactory.create_provider(CloudProvider.AWS, aws_config)
        providers["aws"].authenticate()
        print("  ✓ AWS ready")
    
    if settings.azure_enabled:
        print("Initializing Azure provider...")
        azure_config = {
            "subscription_id": settings.azure_subscription_id,
            "tenant_id": settings.azure_tenant_id,
            "client_id": settings.azure_client_id,
            "client_secret": settings.azure_client_secret,
        }
        providers["azure"] = ProviderFactory.create_provider(CloudProvider.AZURE, azure_config)
        providers["azure"].authenticate()
        print("  ✓ Azure ready")
    
    if settings.gcp_enabled:
        print("Initializing GCP provider...")
        gcp_config = {
            "project_id": settings.gcp_project_id,
            "credentials_path": settings.gcp_credentials_path,
        }
        providers["gcp"] = ProviderFactory.create_provider(CloudProvider.GCP, gcp_config)
        providers["gcp"].authenticate()
        print("  ✓ GCP ready")
    
    if settings.onprem_enabled:
        print("Initializing on-premises provider...")
        onprem_config = {
            "hosts": settings.onprem_hosts,
        }
        providers["onprem"] = ProviderFactory.create_provider(CloudProvider.ONPREM, onprem_config)
        providers["onprem"].authenticate()
        print("  ✓ On-premises ready")
    
    return providers


def collect_all_resources(providers):
    """Collect resources from all providers."""
    all_resources = {
        "compute": [],
        "storage": [],
        "database": []
    }
    
    for provider_name, provider in providers.items():
        print(f"\nCollecting resources from {provider_name}...")
        
        compute = provider.list_compute_resources()
        storage = provider.list_storage_resources()
        database = provider.list_database_resources()
        
        all_resources["compute"].extend(compute)
        all_resources["storage"].extend(storage)
        all_resources["database"].extend(database)
        
        print(f"  Compute: {len(compute)}")
        print(f"  Storage: {len(storage)}")
        print(f"  Database: {len(database)}")
    
    return all_resources


def calculate_total_cost(providers):
    """Calculate total cost across all providers."""
    total_monthly_cost = 0.0
    cost_by_provider = {}
    
    for provider_name, provider in providers.items():
        cost_data = provider.get_cost_data()
        provider_cost = sum(c.monthly_cost for c in cost_data)
        cost_by_provider[provider_name] = provider_cost
        total_monthly_cost += provider_cost
    
    return total_monthly_cost, cost_by_provider


def main():
    """Main example function."""
    print("CloudMind AI - Multi-Cloud Management Example\n")
    print("=" * 60)
    
    # Initialize providers
    print("\n1. Initializing cloud providers...\n")
    providers = initialize_providers()
    
    if not providers:
        print("\nNo providers enabled. Please configure at least one provider in .env")
        return
    
    print(f"\n✓ {len(providers)} provider(s) initialized")
    
    # Collect resources
    print("\n" + "=" * 60)
    print("\n2. Collecting resources across all clouds...")
    all_resources = collect_all_resources(providers)
    
    total_resources = sum(len(resources) for resources in all_resources.values())
    print(f"\n✓ Total resources discovered: {total_resources}")
    print(f"  - Compute: {len(all_resources['compute'])}")
    print(f"  - Storage: {len(all_resources['storage'])}")
    print(f"  - Database: {len(all_resources['database'])}")
    
    # Calculate costs
    print("\n" + "=" * 60)
    print("\n3. Calculating costs...")
    total_cost, cost_by_provider = calculate_total_cost(providers)
    
    print(f"\n✓ Total monthly cost: ${total_cost:.2f}")
    for provider_name, cost in cost_by_provider.items():
        print(f"  - {provider_name}: ${cost:.2f}")
    
    print("\n" + "=" * 60)
    print("\nMulti-cloud management example completed!")


if __name__ == "__main__":
    main()
