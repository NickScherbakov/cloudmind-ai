"""Command-line interface for CloudMind AI."""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from ..core.config import settings
from ..core.models import CloudProvider
from ..core.logger import logger
from ..providers import ProviderFactory
from ..ai import AIOptimizationService
from ..monitoring import MonitoringService

app = typer.Typer(
    name="cloudmind",
    help="CloudMind AI - Cloud Resource Management and Optimization Platform",
    add_completion=False,
)
console = Console()


def get_provider(provider_name: str):
    """Get provider instance."""
    provider_configs = {
        "aws": {
            "region": settings.aws_region,
            "access_key_id": settings.aws_access_key_id,
            "secret_access_key": settings.aws_secret_access_key,
        },
        "azure": {
            "subscription_id": settings.azure_subscription_id,
            "tenant_id": settings.azure_tenant_id,
            "client_id": settings.azure_client_id,
            "client_secret": settings.azure_client_secret,
        },
        "gcp": {
            "project_id": settings.gcp_project_id,
            "credentials_path": settings.gcp_credentials_path,
        },
        "onprem": {
            "hosts": settings.onprem_hosts,
        },
    }
    
    config = provider_configs.get(provider_name)
    if not config:
        console.print(f"[red]Unknown provider: {provider_name}[/red]")
        raise typer.Exit(1)
    
    provider_type = CloudProvider(provider_name)
    provider = ProviderFactory.create_provider(provider_type, config)
    
    try:
        provider.authenticate()
        return provider
    except Exception as e:
        console.print(f"[red]Authentication failed: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def version():
    """Show version information."""
    rprint(f"[bold green]CloudMind AI[/bold green] v{settings.app_version}")
    rprint(f"Open source cloud resource management and optimization platform")


@app.command()
def info():
    """Show configuration information."""
    table = Table(title="CloudMind AI Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("App Name", settings.app_name)
    table.add_row("Version", settings.app_version)
    table.add_row("Debug Mode", str(settings.debug))
    table.add_row("AWS Enabled", str(settings.aws_enabled))
    table.add_row("Azure Enabled", str(settings.azure_enabled))
    table.add_row("GCP Enabled", str(settings.gcp_enabled))
    table.add_row("On-Prem Enabled", str(settings.onprem_enabled))
    table.add_row("AI Enabled", str(settings.ai_enabled))
    table.add_row("Auto Optimize", str(settings.auto_optimize))
    
    console.print(table)


@app.command()
def list_resources(
    provider: str = typer.Option(..., "--provider", "-p", help="Cloud provider (aws, azure, gcp, onprem)"),
    resource_type: str = typer.Option("compute", "--type", "-t", help="Resource type (compute, storage, database)"),
    region: Optional[str] = typer.Option(None, "--region", "-r", help="Region filter"),
):
    """List cloud resources."""
    console.print(f"[cyan]Listing {resource_type} resources from {provider}...[/cyan]")
    
    prov = get_provider(provider)
    
    try:
        if resource_type == "compute":
            resources = prov.list_compute_resources(region)
        elif resource_type == "storage":
            resources = prov.list_storage_resources(region)
        elif resource_type == "database":
            resources = prov.list_database_resources(region)
        else:
            console.print(f"[red]Unknown resource type: {resource_type}[/red]")
            raise typer.Exit(1)
        
        if not resources:
            console.print("[yellow]No resources found[/yellow]")
            return
        
        table = Table(title=f"{resource_type.capitalize()} Resources")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Region", style="blue")
        
        for resource in resources:
            table.add_row(
                resource.id,
                resource.name,
                resource.status.value,
                resource.region
            )
        
        console.print(table)
        console.print(f"[green]Total: {len(resources)} resources[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def get_metrics(
    provider: str = typer.Option(..., "--provider", "-p", help="Cloud provider"),
    resource_id: str = typer.Option(..., "--resource", "-r", help="Resource ID"),
):
    """Get metrics for a resource."""
    console.print(f"[cyan]Getting metrics for resource {resource_id}...[/cyan]")
    
    prov = get_provider(provider)
    
    try:
        metrics = prov.get_resource_metrics(resource_id)
        
        table = Table(title=f"Metrics for {resource_id}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in metrics.items():
            table.add_row(key, str(value))
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def optimize(
    provider: Optional[str] = typer.Option(None, "--provider", "-p", help="Specific provider to optimize"),
):
    """Get AI-powered optimization recommendations."""
    if not settings.ai_enabled:
        console.print("[red]AI service is not enabled. Set AI_ENABLED=true in .env[/red]")
        raise typer.Exit(1)
    
    console.print("[cyan]Analyzing resources for optimization opportunities...[/cyan]")
    
    # Initialize AI service
    ai_config = {
        "api_key": settings.openai_api_key,
        "model": settings.openai_model,
        "enabled": settings.ai_enabled,
    }
    ai_service = AIOptimizationService(ai_config)
    
    # Collect resources from providers
    providers_to_check = [provider] if provider else ["aws", "azure", "gcp", "onprem"]
    all_resources = []
    
    for prov_name in providers_to_check:
        enabled_setting = getattr(settings, f"{prov_name}_enabled", False)
        if not enabled_setting:
            continue
        
        try:
            prov = get_provider(prov_name)
            resources = prov.list_compute_resources()
            all_resources.extend(resources)
        except Exception as e:
            logger.warning(f"Failed to get resources from {prov_name}: {e}")
            continue
    
    if not all_resources:
        console.print("[yellow]No resources found to optimize[/yellow]")
        return
    
    # Generate recommendations
    try:
        recommendations = ai_service.analyze_resources_batch(all_resources)
        
        if not recommendations:
            console.print("[green]All resources are optimally configured![/green]")
            return
        
        table = Table(title="Optimization Recommendations")
        table.add_column("Resource", style="cyan")
        table.add_column("Provider", style="blue")
        table.add_column("Action", style="yellow")
        table.add_column("Reason", style="white")
        table.add_column("Savings", style="green")
        table.add_column("Confidence", style="magenta")
        
        total_savings = 0.0
        for rec in recommendations:
            if rec.estimated_savings > 0:
                total_savings += rec.estimated_savings
            
            table.add_row(
                rec.resource_name,
                rec.provider.value,
                rec.action.value,
                rec.reason,
                f"${rec.estimated_savings:.2f}/month",
                f"{rec.confidence*100:.0f}%"
            )
        
        console.print(table)
        console.print(f"\n[bold green]Total Estimated Savings: ${total_savings:.2f}/month[/bold green]")
    except Exception as e:
        console.print(f"[red]Error generating recommendations: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def start_api(
    host: str = typer.Option(settings.api_host, "--host", "-h", help="API host"),
    port: int = typer.Option(settings.api_port, "--port", "-p", help="API port"),
    reload: bool = typer.Option(settings.api_reload, "--reload", help="Enable auto-reload"),
):
    """Start the REST API server."""
    import uvicorn
    
    console.print(f"[cyan]Starting CloudMind AI API on {host}:{port}...[/cyan]")
    uvicorn.run(
        "cloudmind.api.main:app",
        host=host,
        port=port,
        reload=reload,
    )


@app.command()
def stop_resource(
    provider: str = typer.Option(..., "--provider", "-p", help="Cloud provider"),
    resource_id: str = typer.Option(..., "--resource", "-r", help="Resource ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Stop a resource."""
    if not confirm:
        confirmed = typer.confirm(f"Are you sure you want to stop resource {resource_id}?")
        if not confirmed:
            console.print("[yellow]Operation cancelled[/yellow]")
            return
    
    console.print(f"[cyan]Stopping resource {resource_id}...[/cyan]")
    
    prov = get_provider(provider)
    
    try:
        success = prov.stop_resource(resource_id)
        if success:
            console.print(f"[green]Resource {resource_id} stopped successfully[/green]")
        else:
            console.print(f"[red]Failed to stop resource {resource_id}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def start_resource(
    provider: str = typer.Option(..., "--provider", "-p", help="Cloud provider"),
    resource_id: str = typer.Option(..., "--resource", "-r", help="Resource ID"),
):
    """Start a resource."""
    console.print(f"[cyan]Starting resource {resource_id}...[/cyan]")
    
    prov = get_provider(provider)
    
    try:
        success = prov.start_resource(resource_id)
        if success:
            console.print(f"[green]Resource {resource_id} started successfully[/green]")
        else:
            console.print(f"[red]Failed to start resource {resource_id}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
